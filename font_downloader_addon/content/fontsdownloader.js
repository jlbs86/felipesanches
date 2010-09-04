/* ***** BEGIN LICENSE BLOCK *****
 * Version: MPL 1.1/GPL 2.0/LGPL 2.1
 *
 * The contents of this file are subject to the Mozilla Public License Version
 * 1.1 (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 * http://www.mozilla.org/MPL/
 *
 * Software distributed under the License is distributed on an "AS IS" basis,
 * WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
 * for the specific language governing rights and limitations under the
 * License.
 *
 * The Initial Developer of the Original Code is Felipe C. da S. Sanches.
 * Portions created by the Initial Developer are Copyright (C) 2010
 * the Initial Developer. All Rights Reserved.
 *
 * Contributor(s):
 *  Felipe C. da S. Sanches <jucablues@users.sourceforge.net>
 *
 * Alternatively, the contents of this file may be used under the terms of
 * either the GNU General Public License Version 2 or later (the "GPL"), or
 * the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
 * in which case the provisions of the GPL or the LGPL are applicable instead
 * of those above. If you wish to allow use of your version of this file only
 * under the terms of either the GPL or the LGPL, and not to allow others to
 * use your version of this file under the terms of the MPL, indicate your
 * decision by deleting the provisions above and replace them with the notice
 * and other provisions required by the GPL or the LGPL. If you do not delete
 * the provisions above, a recipient may use your version of this file under
 * the terms of any one of the MPL, the GPL or the LGPL.
 *
 * ***** END LICENSE BLOCK ***** */

var FontsDownloader = {
  FONTS_DIR: ".fonts", //TODO: support other operating systems  

  init : function () {
    var appcontent = document.getElementById("appcontent");   // browser  
    if(appcontent)  
      appcontent.addEventListener("DOMContentLoaded", FontsDownloader.onPageLoad, true);

      FontsDownloader.create_fonts_dir();
  },

  create_fonts_dir : function (){
    var dirService = Components.classes["@mozilla.org/file/directory_service;1"].
                      getService(Components.interfaces.nsIProperties);
    var fontsDirFile = dirService.get("Home", Components.interfaces.nsIFile);
    fontsDirFile.append(this.FONTS_DIR);

    if( !fontsDirFile.exists() || !fontsDirFile.isDirectory() ) {
        // if it doesn't exist, create
      alert("Creating fonts directory: "+fontsDirFile.path);
      fontsDirFile.create(Components.interfaces.nsIFile.DIRECTORY_TYPE, 0777);  
    }
  },

  download_it: function (url, filename) {

    var dirService = Components.classes["@mozilla.org/file/directory_service;1"].  
                      getService(Components.interfaces.nsIProperties);   
    var homeDirFile = dirService.get("Home", Components.interfaces.nsIFile);

    var file = Components.classes["@mozilla.org/file/local;1"]  
            .createInstance(Components.interfaces.nsILocalFile);  

    file.initWithPath(homeDirFile.path + "/" + this.FONTS_DIR + "/" + filename);

    var wbp = Components.classes['@mozilla.org/embedding/browser/nsWebBrowserPersist;1']  
          .createInstance(Components.interfaces.nsIWebBrowserPersist);  
    var ios = Components.classes['@mozilla.org/network/io-service;1']  
          .getService(Components.interfaces.nsIIOService);  
    var uri = ios.newURI(url, null, null);  
    wbp.persistFlags &= ~Components.interfaces.nsIWebBrowserPersist.PERSIST_FLAGS_NO_CONVERSION; // don't save gzipped  
    wbp.saveURI(uri, null, null, null, null, file);
  },

  onPageLoad: function (aEvent) {
    var doc = aEvent.originalTarget;

    for (var ss in doc.styleSheets){
      var rules = doc.styleSheets[ss].cssRules;
      for (var r in rules){
        var rule = rules[r];
        if (rule instanceof CSSFontFaceRule){
          var fontfamily = rule.style.getPropertyValue("font-family");
          var src = rule.style.getPropertyValue("src");
          try{
            var url = src.split("url(\"")[1].split("\"")[0];
            var filename = fontfamily.split("\"")[1];
            //filename = filename.replace( new RegExp( " ", "g" ), "_" )  //do we need to sanitize?
            //filename += "." + FONT_FORMAT_EXTENSION;

            //alert(filename);
            FontsDownloader.download_it(url, filename);
          } catch(err){/*ignore*/}
        } 
      }
    }
  },
}

window.addEventListener("load", function() { FontsDownloader.init(); }, false);
