// project: web
// author: Julien Spronck
// email: github@frenetic.be
// website: https://frenetic.be

// Define the svg element

var width = $(window).width();
var height = $(window).height();
var margins = {
    top: 20,
    left: 20,
    bottom: 20,
    right: 20
}

var svg = d3
    .select('#svg-area')
    .append('svg')
    .attr("width", width)
    .attr("height", height);

// Define the div for the tooltip
var div = d3.select("body").append("div")	
    .attr("class", "tooltip")				
    .style("opacity", 0);

d3.json('static/js/clusters.json', function(data){
    [minX, maxX] = d3.extent(data, d => d.x);
    [minY, maxY] = d3.extent(data, d => d.y);

    var xScale = d3.scaleLinear()
        .domain([minX, maxX])
        .range([margins.left, width - margins.right]);

    var yScale = d3.scaleLinear()
        .domain([minY, maxY])
        .range([height-margins.bottom, margins.top]);
    
    var colors = ['tomato', 'orange', 'limegreen', 'steelblue'];

    d3.json('static/js/cluster_links.json', function(links){

        var dataMap = {};
        for (var j=0; j<data.length; j++){
            dataMap[data[j].ingredient] = [xScale(data[j].x), yScale(data[j].y)];
        }

        svg.selectAll('.edge')
            .data(links)
        .enter()
            .append('path')
            .attr('d', d => d3.line()([dataMap[d[0]], dataMap[d[1]]]))
            .attr('stroke', 'black')
            .attr('stroke-opacity', 0.2)
            .attr('class', 'edge');
        
        svg.selectAll('.node')
            .data(data)
        .enter()
            .append('circle')
            .attr('cx', d => xScale(d.x))
            .attr('cy', d => yScale(d.y))
            .attr('r', 7)
            .attr('fill', d => colors[d.cluster])
            .attr('class', 'node')
            .on("mouseover", function(d) {		
                div.html(d.ingredient)	
                    .style("left", (d3.event.pageX+20) + "px")		
                    .style("top", (d3.event.pageY) + "px");
                div.style("opacity", .9);
                div.classed('cluster0', false);
                div.classed('cluster1', false);
                div.classed('cluster2', false);
                div.classed('cluster3', false);
                div.classed('cluster'+d.cluster, true);
            })
            .on("mouseout", function(d) {		
                div.style("opacity", 0);	
            });

            var ingstoshow = [
                'coconut', 'turmeric', 'ginger', 'coriander seeds', 'mustard seeds', 'green cardamom', 'red chili pepper',
                'apricot', 'banana', 'blueberry', 'strawberry', 'blackberry', 'raspberry', 'pear', 'cherry', 'pomegranate',
                'pepperoni', 'provolone cheese', 'pancetta', 'prosciutto', 'pecorino', 'italian sausage', 'black olives',
                'queso fresco', 'cilantro', 'black beans', 'pinto beans', 'black-eyed peas', 'tomatillo', 'chipotle pepper'
            ];

            svg.selectAll('.labels')
                .data(data.filter(function(x){return ingstoshow.indexOf(x.ingredient) != -1}))
            .enter()
                .append('text')
                .attr('x', d => xScale(d.x)+10)
                .attr('y', d => yScale(d.y))
                .attr('fill', d => colors[d.cluster])
                .attr('class', 'labels')
                .text(d => d.ingredient)
                .style('font-weight', 600);
    });

});