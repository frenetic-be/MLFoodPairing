// project: web
// author: Julien Spronck
// email: github@frenetic.be
// website: https://frenetic.be

// Define the svg element
var svgWidth = $('.main-container').width();
var svgHeight = $(window).innerHeight() - $('header').innerHeight() - $('footer').innerHeight();

var svg = d3
    .select('#svg-area')
    .append('svg')
    .attr("width", svgWidth)
    .attr("height", svgHeight);

function nRows(nCol, nTot){
    // Calculates the number of rows based on the number of columns and the total number of hexs
    var out = 0;
    var tot = nTot;
    out += 2 * Math.floor(tot/(2 * nCol - 1));
    tot -= Math.floor(tot/(2 * nCol - 1)) * (2 * nCol - 1);
    if (tot > 0){
        if (tot > nCol){
            return out + 2;
        }
        return out + 1;
    }
    return out;
}

// function calculateGeometry(r){
//     nCol = Math.floor((svgWidth - 4 * r)/(3 * r) + 1);
//     nRow = Math.floor((svgHeight - 2 * r)/r + 1);
//     if (nRow % 2 == 0) {
//         nTot = (2 * nCol - 1) * (nRow / 2);
//     } else {
//         nTot = (2 * nCol - 1) * ((nRow - 1) / 2) + 5;
//     }
//     return [nCol, nRow, nTot];
// }

// function optimalRadius(nHex){
//     var r = 1;
//     [nCol, nRow, nTot] = calculateGeometry(r);
//     while (nTot >= nHex) {
//         r += 1;
//         [nCol, nRow, nTot] = calculateGeometry(r);
//     }
//     r -= 1;
//     [nCol, nRow, nTot] = calculateGeometry(r);
//     nRow = nRows(nCol, nHex);
//     var newWidth = 2 * r + 3 * r * (nCol - 1);
//     var newHeight = r * (nRow + 1) / 2 * Math.sqrt(3);
//     var leftMargin = Math.floor((svgWidth - newWidth)/2);
//     var topMargin = Math.floor((svgHeight - newHeight)/2);
//     return [r, nRow, nCol, leftMargin, topMargin];
// }

function calculateGeometry(r, nTot){
    // Calculates the number of rows and columns based on the radius and the total number of hexs
    var nCol = Math.floor((svgWidth - 4 * r)/(3 * r) + 1);
    var nRow = nRows(nCol, nTot);
    var newWidth = 2 * r + 3 * r * (nCol - 1);
    var newHeight = r * (nRow + 1) / 2 * Math.sqrt(3);
    return [nCol, nRow, newWidth, newHeight];
}

function optimalRadius(nHex){
    // Calculates the best hexagon radius (radius of the circle containing the hexagon) that will
    // fill up the page
    var r = 1;
    [nCol, nRow, newWidth, newHeight] = calculateGeometry(r, nHex);
    while (newHeight < svgHeight - 2 * r) {
        r += 1;
        [nCol, nRow, newWidth, newHeight] = calculateGeometry(r, nHex);
    }
    r -= 1;
    [nCol, nRow, newWidth, newHeight] = calculateGeometry(r, nHex);
    var leftMargin = Math.floor((svgWidth - newWidth)/2);
    var topMargin = Math.floor((svgHeight - newHeight)/2);
    return [r, nRow, nCol, leftMargin, topMargin];
}
    
function text2id(text){
    // Creates an id from an ingredient name
    return "hex_" + text.toLowerCase().split(" ").join("_");
}

function toTitleCase(str){
    // Transforms a string to title case
    return str.replace(/\w\S*/g, function(txt){
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}

function wrap(text, width) {
    text.each(function() {
        var text = d3.select(this),
            words = text.text().split(/\s+/).reverse(),
            word,
            line = [],
            lineNumber = 0,
            lineHeight = 1.1, // ems
            y = text.attr("y"),
            dy = 0,
            tspan = text.text(null)
                .append("tspan")
                .attr("x", 0)
                .attr("y", y)
                .attr("dy", dy + "em")
                .attr("alignment-baseline", "middle");
        while (word = words.pop()) {
            line.push(word);
            tspan.text(line.join(" "));
            if (tspan.node().getComputedTextLength() > width) {
                line.pop();
                if (line.join(" ") === ""){
                    tspan.remove();
                    lineNumber --;
                } else {
                    tspan.text(line.join(" "));
                }
                line = [word];
                tspan = text
                    .append("tspan")
                    .attr("x", 0)
                    .attr("y", y)
                    .attr("alignment-baseline", "middle")
                    .text(word);
                lineNumber ++;
            }
        }
        d3.selectAll('#detail > text > tspan').each(function(d, i){
            // alert(""+i+", "+lineNumber+", "+lineHeight+", "+((i-lineNumber/2.) * lineHeight) + "em")
            d3.select(this).attr("dy", ((i-lineNumber/2) * lineHeight) + "em");
        });
    });
}
    
var nHex = Object.keys(data).length;
var [radius, nRow, nCol, leftMargin, topMargin] = optimalRadius(nHex);

function makeGenHex(radius, xp, yp, text, clss, detail) {

    var h = (Math.sqrt(3)/2);
    var hexagonData = [
        { "x": (radius-1) + xp, "y": yp}, 
        { "x": (radius-1) / 2 + xp, "y": (radius-1) * h + yp},
        { "x": -(radius-1) / 2 + xp, "y": (radius-1) * h + yp},
        { "x": -(radius-1) + xp, "y": yp},
        { "x": -(radius-1) / 2 + xp, "y": -(radius-1) * h + yp},
        { "x": (radius-1) / 2 + xp, "y": -(radius-1) * h + yp},
        { "x": (radius-1) + xp, "y": yp}
    ];

    var displayedText;
    if (text.length <= 6) {
        displayedText = toTitleCase(text);
    } else {
        displayedText = text.toUpperCase().split(' ').map(d => d[0]).join('');
    }


    var drawHexagon = d3.line()
        .x(d => d.x)
        .y(d => d.y);
    var group = svg.append('g')
        .attr("class", "hexgroup")
    if (detail === true){
        group.attr("id", "detail");
    } else {
        group.attr("id", text2id(text));
    }
    group.append("path")
        .attr("d", drawHexagon(hexagonData))
        .attr("class", "hex "+clss);
    group.append("text")
        .attr("x", xp)
        .attr("y", yp)
        .text(displayedText)
        .attr("text-anchor", "middle")
        .attr("alignment-baseline", "middle");
    if (detail !== true){
        group.on("mouseover", function(d) {		
            d3.select('#detail')
                .attr("transform", "translate(" + xp + "," + yp + ")")
                .attr('data-ingredient', text);
            d3.select('#detail > text')
                .text(toTitleCase(text))
                .call(wrap, 2.1*radius)
                .attr("text-anchor", "middle")
                // .attr("alignment-baseline", "middle");
            if (!$('#detail > path').hasClass(clss)){
                $('#detail > path').removeClass("meat spice produce nut herb dairy")
                    .addClass(clss);
            }
            $('#detail').show();
        });
    } else {
        group.on('click', function(event){
            var text =  d3.select('#detail').attr('data-ingredient');
            pairings = data[text].slice(0, 10);
            $('.highlight').removeClass('highlight');
            $('.selected').removeClass('selected');
            pairings.forEach(function(ing){
                $('#'+text2id(ing)).addClass('highlight');
            });
            $('#'+text2id(text)).addClass('selected');
        });
        group.on("mouseout", function(d) {
            $('#detail').hide();
        });
    }
}

function makeHex(radius, row, col, leftMargin, topMargin, text, clss) {

    var h = (Math.sqrt(3)/2);
    var xp = leftMargin + radius * (3 * col + 1);
    if ((row % 2) == 1){
        xp += 1.5 * radius;
    }
    var yp = topMargin + h * radius * (row + 1);

    makeGenHex(radius, xp, yp, text, clss)

}

function makeDetailHex(radius, mag, row, col, leftMargin, topMargin) {

    var newRadius = radius * mag;
    var newRow = (row + 1) / mag - 1;
    var newCol = ((3 * col + 1) / mag - 1) / 3;
    var h = (Math.sqrt(3)/2);
    var xp = leftMargin + newRadius * (3 * newCol + 1);
    if ((row % 2) == 1){
        xp += 1.5 * radius;
    }
    var yp = topMargin + h * newRadius * (newRow + 1);

    makeGenHex(newRadius, 0, 0, "", "detail", true);
}

var row = 0;
var col = 0;
Object.keys(data).forEach(function(key){
    var cat = categories[key];
    if (cat === 'meat/fish') cat = 'meat';

    // Create hex
    makeHex(radius, row, col, leftMargin, topMargin, key, cat);

    // $('#' + text2id(key) + ' > .hex').css('fill', 'url(#img_' + key.toLowerCase().split(" ").join("_") + ')');

    // Calculate new row and column number
    if (row % 2 == 0){
        if (col == nCol - 1) {
            col = 0;
            row ++;
        } else {
            col ++;
        }
    } else {
        if (col == nCol - 2) {
            col = 0;
            row ++;
        } else {
            col ++;
        }  
    }
});

makeDetailHex(radius, 1.8, 2, 5, leftMargin, topMargin)