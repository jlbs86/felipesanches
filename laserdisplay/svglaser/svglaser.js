$(function(){

    var curConfig = {
      canvas_expansion: 3,
      dimensions: [600,600],
      initFill: {
        type: 'none'
      },
      initStroke: {
        width: 2,
        color: 'FFFFFF',
        opacity: 1
      },
      initOpacity: 1,
/*      initTool: 'select',  */
      initTool: 'path',
      wireframe: false
    };

    var svgCanvas = new $.SvgCanvas(document.getElementById("svgcanvas"), curConfig);

});
