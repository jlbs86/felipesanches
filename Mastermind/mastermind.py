# -*- coding: utf-8 -*-
import sys
from gettext import gettext as _
import traceback
import gobject
import gtk

# Optionally use OpenGL support
openGLErrors = []
haveGLDepthSupport = True
haveGLAccumSupport = True
try:
    import OpenGL.GL
except:
    # Translators: Error message displayed when 3D mode is not available due to no Python OpenGL libraries
    openGLErrors.append(_('No Python OpenGL support'))
try:
    import gtk.gtkgl
    import gtk.gdkgl
except:
    # Translators: Error message displayed when 3D mode is not available due to no Python GTKGLExt libraries
    openGLErrors.append(_('No Python GTKGLExt support'))
else:
    display_mode = (gtk.gdkgl.MODE_RGB | gtk.gdkgl.MODE_DEPTH | gtk.gdkgl.MODE_DOUBLE | gtk.gdkgl.MODE_ACCUM)
    try:
        glConfig = gtk.gdkgl.Config(mode = display_mode)
    except gtk.gdkgl.NoMatches:
        display_mode &= ~gtk.gdkgl.MODE_DOUBLE
        display_mode &= ~gtk.gdkgl.MODE_ACCUM
        haveGLAccumSupport = False
        haveGLDepthSupport = False
        try:
            glConfig = gtk.gdkgl.Config(mode = display_mode)
        except gtk.gdkgl.NoMatches:
            # Translators: Error message displayed when 3D mode is not available due to their 3D drivers not being able to provide a suitable display mode
            openGLErrors.append(_('OpenGL libraries do not support required display mode'))
haveGLSupport = len(openGLErrors) == 0

__all__ = ['GtkView']

class GtkViewArea(gtk.DrawingArea):
    """Custom widget to render an OpenGL scene"""
    
    def __init__(self, view):
        """
        """
        gtk.DrawingArea.__init__(self)

        # Pixmaps to use for double buffering
        self.pixmap = None
        self.dynamicPixmap = None

        self.renderGL = False # Flag to show if this scene is to be rendered using OpenGL
        self.__glDrawable = None
        self.view = view

        # Allow notification of button presses
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.BUTTON_MOTION_MASK)
        
        # Make openGL drawable
        if haveGLSupport:
            gtk.gtkgl.widget_set_gl_capability(self, glConfig)# FIXME:, share_list=glContext)

        # Connect signals
        self.connect('realize', self.__init)
        self.connect('configure_event', self.__configure)
        self.connect('expose_event', self.__expose)
        self.connect('button_press_event', self.__button_press)
        self.connect('button_release_event', self.__button_release)
        
    # Public methods
        
    def redraw(self):
        """Request this widget is redrawn"""
        # If the window is visible prepare it for redrawing
        area = gtk.gdk.Rectangle(0, 0, self.allocation.width, self.allocation.height)
        if self.window is not None:
            self.window.invalidate_rect(area, False)

    def setRenderGL(self, renderGL):
        """Enable OpenGL rendering"""
        if not haveGLSupport:
            renderGL = False
        
        if self.renderGL == renderGL:
            return
        self.renderGL = renderGL
        self.redraw()
    
    # Private methods

    def __startGL(self):
        """Get the OpenGL context"""
        if not self.renderGL:
            return

        assert(self.__glDrawable is None)
        
        # Obtain a reference to the OpenGL drawable
        # and rendering context.
        glDrawable = gtk.gtkgl.widget_get_gl_drawable(self)
        glContext = gtk.gtkgl.widget_get_gl_context(self)

        # Check were able to get context
        if glDrawable is None or glContext is None:
            return

        # OpenGL begin (can fail)
        if not glDrawable.gl_begin(glContext):
            return
        
        self.__glDrawable = glDrawable
        
    def __endGL(self):
        """Free the OpenGL context"""
        if self.__glDrawable is None or not self.renderGL:
            return
        self.__glDrawable.gl_end()
        self.__glDrawable = None
        
    def __init(self, widget):
        """Gtk+ signal"""
        if self.view.scene is not None:
            self.view.scene.reshape(widget.allocation.width, widget.allocation.height)
        
    def __configure(self, widget, event):
        """Gtk+ signal"""
        self.pixmap = gtk.gdk.Pixmap(widget.window, event.width, event.height)
        self.dynamicPixmap = gtk.gdk.Pixmap(widget.window, event.width, event.height)
        try:
            self.__startGL()
            if self.view.scene is not None:
                self.view.scene.reshape(event.width, event.height)
            self.__endGL()
        except:
            #glchess.config.set('show_3d', False)
            raise

    def __expose(self, widget, event):
        """Gtk+ signal"""
        if self.renderGL:
            try:
                self.__startGL()
                if self.__glDrawable is None:
                    return

                # Get the scene rendered
                try:
                    if self.view.scene is not None:
                        self.view.scene.renderGL()
                except OpenGL.GL.GLerror, e:
                    print 'Rendering Error: ' + str(e)
                    traceback.print_exc(file = sys.stdout)

                # Paint this
                if self.__glDrawable.is_double_buffered():
                    self.__glDrawable.swap_buffers()
                else:
                    OpenGL.GL.glFlush()

                self.__endGL()
            except:
                #glchess.config.set('show_3d', False)
                raise

        else:
            context = self.pixmap.cairo_create()
            if self.view.scene is not None:
                self.view.scene.renderStatic(context)
            
            # Copy the background to render the dynamic elements on top
            self.dynamicPixmap.draw_drawable(widget.get_style().white_gc, self.pixmap, 0, 0, 0, 0, -1, -1)
            context = self.dynamicPixmap.cairo_create()
        
            # Set a clip region for the expose event
            context.rectangle(event.area.x, event.area.y, event.area.width, event.area.height)
            context.clip()
           
            # Render the dynamic elements
            if self.view.scene is not None:
                self.view.scene.renderDynamic(context)
                
            # Draw the window
            widget.window.draw_drawable(widget.get_style().white_gc, self.dynamicPixmap,
                                        event.area.x, event.area.y,
                                        event.area.x, event.area.y, event.area.width, event.area.height)   

    def __button_press(self, widget, event):
        """Gtk+ signal"""
        if event.button != 1:
            return
        try:
            self.__startGL()
            if self.view.scene is not None:
                self.view.scene.mouse_down(event.x, event.y)
            self.__endGL()
        except:
            #glchess.config.set('show_3d', False)
            raise
        
    def __button_release(self, widget, event):
        """Gtk+ signal"""
        if event.button != 1:
            return
        try:
            self.__startGL()
            if self.view.scene is not None:
                self.view.scene.mouse_up(event.x, event.y)
            self.__endGL()
        except:
            #glchess.config.set('show_3d', False)
            raise

from scene import Scene

class Game():
	def __init__(self):

    # The GTK+ elements
		self.window = gtk.Window()
		self.viewWidget = GtkViewArea(self)
		self.window.add(self.viewWidget)
		self.scene = Scene(self.viewWidget)

		self.window.maximize()
		self.window.show_all()
		self.viewWidget.redraw()
		gtk.main()

g = Game()

