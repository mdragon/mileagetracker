var ymax = null;
var options;

function setupPlot(container, plotdata, legend, time, timeformat, points, xaxis, yaxis)
{	
	var series = [];
	var colors = [];
	var plot;
	
	if( points == undefined || points == null )
	{
		points = false;
	}
	
	container = $(container);
	console.log("container", container);
	
	series = buildSeries(plotdata, legend);
	
	if( ! points )
	{
		if( container[0].id.indexOf("-stack") > 0 || container.hasClass("stack") )
		{
			lines = { show: true, fill: true, lineWidth: 1 };
		}
		else
		{
			lines = { show: true, lineWidth: 2 };
		}
	} else
	{
		lines = { show: false };
	}

	if( globalColors !== undefined && globalColors !== null )
	{
		colors = globalColors;
	} else
	{
		colors[colors.length] = "#269F00"; // green
		colors[colors.length] = "#0069BF"; // blue
		colors[colors.length] = "#EF1D2A"; // red
		colors[colors.length] = "#EF8100"; // orange
		colors[colors.length] = "#100099"; // dark blue/purple
		colors[colors.length] = "#DCFF4F"; // light yellow
		colors[colors.length] = "#000000"; // black
	}
		
	if( time == undefined || time == null )
	{ 
		time = true;
	}
	
	if( xaxis === undefined || xaxis === null )
	{
		if( time )
		{
			xaxis = {mode: "time", timeformat: timeformat };
		} else
		{
			xaxis = {ticks: plotdata[0], noticks: 5 };
		}
	}
	
	if( yaxis === undefined || yaxis === null )
	{
		yaxis = {};
	}
	
	options = {
        lines: lines,
        points: { show: points, lineWidth: 0, radius: 0.5, fill: 0.5},
		bars: {show: false, fill: true},
        grid: {
            backgroundColor: "#fffaff"
        },
		legend: { position: "nw", margin: 35 },
		shadowSize: 0,
		selection: {mode: "xy"},
		colors: colors,
		xaxis: xaxis,
		yaxis: yaxis
    };
	
    plot = redraw(container, options, series, false);
	
	return plot;
}

function buildSeries(plotdata, legend)
{
	console.group("buildSeries");
	var series = [];
	for(var x=0; x < plotdata.length; x++)
	{
		series[x] = { label: legend[x],	data: plotdata[x] };
	}
	
	if( seriesOptions !== undefined && seriesOptions !== null )
	{
		console.log(series);
		console.log("extending series with options", seriesOptions);
		for(var x = 0; x < seriesOptions.length; x++)
		{
			series[x] = $.extend(true, {}, series[x], seriesOptions[x]);
		}
		//series = $.merge(series, seriesOptions);
		console.log(series);
		console.log(series[0]);
	}
	
	console.groupEnd();
	return series;
}

function parseData(data, plotdata, legend)
{
	var pointnum = 0;
	var lines = data.split("\n");

	// empty out data from prior charts
	plotdata.length = 0;
	legend.length = 0;

	console.log('after reset', JSON.stringify(plotdata));
	
	for(var linenum = 0; linenum < lines.length; linenum++)
	{
		var line = $.trim(lines[linenum]);

		if( line.charAt(0) == "!" )
		{
			console.log('header', line);
			var cols = line.split(",");

			for(var x = 1; x < cols.length; x++)
			{
				var series = x-1;
				legend[series] = cols[x];
			}

			console.log(JSON.stringify(legend));
		} 
		else if( line.charAt(0) != "#" && $.trim(line).length != 0)
		{
			console.log('line', line);
	
			// not a comment
			var cols = line.split(",");

			console.log('cols', JSON.stringify(cols));
			
			// start with the second col cause the first is the x component
			for(var x = 1; x < cols.length; x++)
			{
				var series = x-1;
				if(plotdata[series] == undefined || plotdata[series] == null)
				{
					plotdata[series] = [];
				}

				if(  $.trim(cols[x]) == "" )
				{
					console.log('x, val, cols[0]', x, null, cols[0]);
					plotdata[series][pointnum] = [$.trim(cols[0]), null];
				} else
				{
					console.log('x, val, cols[0]', x, cols[x], cols[0]);
					plotdata[series][pointnum] = [$.trim(cols[0]), $.trim(cols[x])];
				}
			}

			console.log('plotdata', plotdata, JSON.stringify(plotdata));

			pointnum++;
		}
	}
}

function zoomEvent(event, ranges, plot)
{
	var axes, target;
	group("zoomEvent");
	console.log("plot", plot);
	axes = plot.getAxes()
	console.log("axes", axes);
	target = $(event.target)
	console.log("target", target);
	console.log("event", event);
	console.log("ranges", ranges);
	
	if( ranges == undefined || ranges == null || ranges.xaxis == undefined || ranges.xaxis == null )
	{
		console.log("bad ranges, not redrawing");
	} else
	{
		var myOptions = $.extend(true, {}, options, 
			{
				xaxis: 
				{ 
					min: ranges.xaxis.from < axes.xaxis.datamin ? axes.xaxis.datamin : ranges.xaxis.from, 
					max: ranges.xaxis.to > axes.xaxis.datamax ? axes.xaxis.datamax : ranges.xaxis.to
				},
				yaxis: 
				{ 
					min: ranges.yaxis.from < axes.yaxis.datamin ? axes.yaxis.datamin : ranges.yaxis.from, 
					max: ranges.yaxis.to > axes.yaxis.datamax ? axes.yaxis.datamax : ranges.yaxis.to 
				}
			}
		);

		redraw(target, myOptions);
	}
	groupEnd();
}

function redraw(target, myOptions, series, limitYAxis)
{
	var series;
	var plotdata = [], legend = [];
	target = $(target);
	if( limitYAxis === undefined || limitYAxis === null )
	{
		limitYAxis = true;
	}
	
	group("redraw");
	console.log("target", target);
	console.log("myOptions", myOptions);

		
	if( series === undefined || series === null ) 
	{
		parseData($(target.parents(".graph-wrapper").find(".graph-data")[0]).text(), plotdata, legend);
		series = buildSeries(plotdata, legend);
	}
	
	if( limitYAxis )
	{
		console.log("y", myOptions["yaxis"], myOptions["yaxis"].length);
		if( myOptions["yaxis"] === null || myOptions["yaxis"]["max"] === undefined )
		{
			var max = findSecondBiggest(series, 2); // this rules #'s are in the last series
			if( max == 0 )
			{
				console.log("bad max found, not using");
			} else
			{
				myOptions["yaxis"] = {max: max};
			}
		}
	}
	
	//myOptions.legend["container"] = target.parents(".graph-wrapper").find(".graph-legend");
	
	//target.unbind("plotselected");
	plot = $.plot(target,series, myOptions);
	//plot.clearSelection();
	//target.bind("plotselected", function(event, ranges) { zoom(event, ranges, plot); });
	
	groupEnd();
	return plot;
}

function findSecondBiggest(series, idx)
{
	var biggest, second, point;
	biggest = 0;
	second = 0;

	if (series[idx] === undefined)
	{
	    // where's my data ie?
	} else
	{
	    group("findSecondBiggest", series[idx].data.length, "entries to check");
	    log("series", series[idx]);
	    for (var x = 0; x < series[idx].data.length; x++)
	    {
	        point = 0;
	        try
	        {
	            point = parseFloat(series[idx].data[x][1]);
	        } catch (ex)
	        {
	            log("couldn't parse", series[idx].data[x][1], "to float");
	        }

	        if (point > second)
	        {
	            log("new point", point, "greater than", second, "maybe bigger than", biggest);
	            if (point > biggest)
	            {
	                log(point, "greter than both", biggest, second);
	                second = biggest;
	                biggest = point;
	            } else
	            {
	                second = point;
	            }
	        } else
	        {
	            //log("new point", point, series[idx].data[x][1], series[idx].data[x], "smaller than", biggest, second);
	        }
	    }
	}	
    log("second", second);
	
	groupEnd();
	return second;
}
