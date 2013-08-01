var globalColors = [];
var plotdata = [];
var legend = [];
var seriesOptions = [];

function init()
{
    //loading = "<img src=\"" + siteRoot + "/images/spinner.gif\" class=\"spinner\"> Loading...<br/>";
    //hookSearchForm();

    globalColors[globalColors.length] = "#a8d599"; // green even lighter: dcebd6
    globalColors[globalColors.length] = "#99c0e5"; // blue even lighter: d6e3f4
    globalColors[globalColors.length] = "#EF1D2A"; // red
    
    buildGraphs();
}

function buildGraphs()
{
    var data = $("div#data-mpg");
    if( data.length != 0 )
    {
        parseData($(data[0]).text(), plotdata, legend);

        console.log("plotdata", JSON.stringify(plotdata));
        console.log("legend", JSON.stringify(legend));

        plot = setupPlot($("#graph-mpg")[0], plotdata, legend, null, null, false);
    }
    
    data = $("div#data-cpg");
    if( data.length != 0 )
    {
        parseData($(data[0]).text(), plotdata, legend);

        console.log("plotdata", JSON.stringify(plotdata));
        console.log("legend", JSON.stringify(legend));

        plot = setupPlot($("#graph-cpg")[0], plotdata, legend, null, null, false);
    }
    
    data = $("div#data-miles");
    if( data.length != 0 )
    {
        parseData($(data[0]).text(), plotdata, legend);

        console.log("plotdata", JSON.stringify(plotdata));
        console.log("legend", JSON.stringify(legend));

        plot = setupPlot($("#graph-miles")[0], plotdata, legend, null, null, false);
    }

}