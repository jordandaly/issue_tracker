d3.queue()
    .defer(d3.json, "get_issues_json/")
    .await(makeGraphs);


function makeGraphs(error, issueData) {
    var ndx = crossfilter(issueData);
    console.log(issueData);
    
    show_issue_type_graph(ndx);
    show_upvotes_graph(ndx);
    show_status_graph(ndx);
    show_author_graph(ndx);

    dc.renderAll();
}



function show_issue_type_graph(ndx) {
    var issue_typeDim = ndx.dimension(dc.pluck("issue_type"));
    var issue_typeMix = issue_typeDim.group();

    dc.barChart("#issue-type-graph")
        .width(350)
        .height(250)
        .margins({top: 10, right: 50, bottom: 30, left: 50})
        .dimension(issue_typeDim)
        .group(issue_typeMix)
        .transitionDuration(500)
        .x(d3.scale.ordinal())
        .xUnits(dc.units.ordinal)
        .elasticY(true)
        .xAxisLabel("Issue Type")
        .yAxis().tickFormat(d3.format("d"));

}

function show_upvotes_graph(ndx) {
    var upvotesDim = ndx.dimension(dc.pluck("upvotes"));
    var upvotesMix = upvotesDim.group();

    dc.rowChart("#upvotes-graph")
        .width(350)
        .height(250)
        .margins({top: 10, right: 50, bottom: 30, left: 50})
        .dimension(upvotesDim)
        .group(upvotesMix)
//        .transitionDuration(500)
        .rowsCap(20)
        .elasticX(true)
        .renderLabel(false)
        .renderTitleLabel(true)
        .titleLabelOffsetX(80)
        .xAxis().ticks(8);

}

function show_status_graph(ndx) {
    var statusDim = ndx.dimension(dc.pluck("status"));
    var statusMix = statusDim.group();

    var statusPieChart = dc.pieChart("#status-graph");

    statusPieChart
        .width(350)
        .height(250)
        .dimension(statusDim)
        .group(statusMix)
        .innerRadius(50)
        .transitionDuration(1500)
        .legend(dc.legend());
          // example of formatting the legend via svg
          // http://stackoverflow.com/questions/38430632/how-can-we-add-legends-value-beside-of-legend-with-proper-alignment
          statusPieChart.on('pretransition', function(statusPieChart) {
            statusPieChart.selectAll('.dc-legend-item text')
                  .text('')
                .append('tspan')
                  .text(function(d) { return d.name; })
                .append('tspan')
                  .attr('x', 100)
                  .attr('text-anchor', 'end')
                  .text(function(d) { return d.data; });
          });

}

function show_author_graph(ndx) {
    var authorDim = ndx.dimension(dc.pluck("author"));
    var authorMix = authorDim.group();

    dc.barChart("#author-graph")
        .width(500)
        .height(250)
        .margins({top: 10, right: 50, bottom: 30, left: 50})
        .dimension(authorDim)
        .group(authorMix)
        .transitionDuration(500)
        .x(d3.scale.ordinal())
        .xUnits(dc.units.ordinal)
        .elasticY(true)
        .xAxisLabel("author")
        .yAxis().tickFormat(d3.format("d"));

}