var svgCanvas = null;

var template1 = 'm 50.931034,145.74149 0,95.68966 130.172416,0 0,-95.68966 -33.62069,0 0,-33.62069 -68.965518,0 0,-7.75862 74.999998,0 0,34.48276 27.58621,0 0,-96.551726 -62.06897,0 0,27.586208 34.48276,0 0,6.896552 -40.51724,0 0,-34.48276 -62.068966,0 0,27.586208 34.48276,0 0,6.896552 -34.48276,0 0,62.068966 68.103446,0 0,34.48276 34.48276,0 0,6.89655 -34.48276,0 0,27.58621 34.48276,0 0,6.89655 -74.999998,0 0,-41.37931 5.172414,0 0,34.48276 28.448274,0 0,-62.06897 -61.206896,0 z';

$(function(){

    svgCanvas = new SvgCanvas(document.getElementById("svgcanvas"));

    svgCanvas.setMode('fhpath');
    svgCanvas.setStrokeWidth(3);
    svgCanvas.setStrokeColor('#ffffff');
    svgCanvas.setFillColor('none');

    $('#select').click(function(){ svgCanvas.setMode('select'); });
    $('#path').click(function(){ svgCanvas.setMode('fhpath'); });
    $('#line').click(function(){ svgCanvas.setMode('line'); });
    $('#rect').click(function(){ svgCanvas.setMode('rect'); });
    $('#ellipse').click(function(){ svgCanvas.setMode('ellipse'); });

    $('#clear').click(function(){ svgCanvas.clear(); });

    $('#color_white').click(function(){ svgCanvas.setStrokeColor('#ffffff'); });
    $('#color_red').click(function(){ svgCanvas.setStrokeColor('#ff0000'); });
    $('#color_green').click(function(){ svgCanvas.setStrokeColor('#00ff00'); });
    $('#color_blue').click(function(){ svgCanvas.setStrokeColor('#0000ff'); });
    $('#color_cyan').click(function(){ svgCanvas.setStrokeColor('#00ffff'); });
    $('#color_magenta').click(function(){ svgCanvas.setStrokeColor('#ff00ff'); });
    $('#color_yellow').click(function(){ svgCanvas.setStrokeColor('#ffff00'); });

    $('#template1').click(function(){ svgCanvas.insertTemplate(template1); });

});
