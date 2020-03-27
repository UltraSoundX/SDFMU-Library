/* ============================================================
 * Charts
 * This files shows how Pages uses Rickshaw, NVD3 and Sparkline
 * to render charts
 * For DEMO purposes only. Extract what you need.
 * ============================================================ */

(function($) {

    'use strict';

    /* ============================================================
     * Rickshaw Charts
     * ============================================================ */

    $(document).ready(function() {

        // Draws a realtime Rickshaw Chart
        (function() {
            var container = '#rickshaw-realtime';

            var seriesData = [
                [],
                [],
                []
            ];
            var random = new Rickshaw.Fixtures.RandomData(50);
            for (var i = 0; i < 50; i++) {
                random.addData(seriesData);
            }
            var graph = new Rickshaw.Graph({
                element: document.querySelector(container),
                height: 500,
                width: $(container).width(),
                renderer: 'area',
                padding: {
                    top: 0.5
                },
                series: [{
                    data: seriesData[0],
                    color: $.Pages.getColor('success-light', .5), // Get Pages contextual color
                    name: 'DB Server'
                }, {
                    data: seriesData[1],
                    color: $.Pages.getColor('master-light'), // Get Pages contextual color
                    name: 'Web Server'
                }]
            });

            var y_axis = new Rickshaw.Graph.Axis.Y({
                graph: graph,
                orientation: 'right',
                tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
                element: document.getElementById('rickshaw-realtime_y_axis'),
            });

            var hoverDetail = new Rickshaw.Graph.HoverDetail({
                graph: graph
            });

            // Update the graph with realtime data. 
            setInterval(function() {
                random.removeData(seriesData);
                random.addData(seriesData);
                graph.update();
            }, 1000);

            d3.selectAll('#rickshaw-realtime_y_axis .tick.major line').attr('x2', '7');
            d3.selectAll('#rickshaw-realtime_y_axis .tick.major text').attr('x', '12');

            $(window).resize(function() {
                graph.configure({
                    width: $(container).width(),
                    height: 500
                });
                graph.render()
            });

            $(container).data('chart', graph);

        })();


        // Draws a stacked bar chart using Rickshaw
        (function() {
            var container = '#rickshaw-stacked-bars';

            var seriesData = [
                [],
                []
            ];
            var random = new Rickshaw.Fixtures.RandomData(40);
            for (var i = 0; i < 40; i++) {
                random.addData(seriesData);
            }

            var graph = new Rickshaw.Graph({
                renderer: 'bar',
                element: document.querySelector(container),
                height: 500,
                width: 700,
                padding: {
                    top: 0.5
                },
                series: [{
                    data: seriesData[0],
                    color: $.Pages.getColor('complete-light'), // Get Pages contextual color
                    name: "New users"
                }, {
                    data: seriesData[1],
                    color: $.Pages.getColor('master-light'), // Get Pages contextual color
                    name: "Returning users"

                }]

            });

            var hoverDetail = new Rickshaw.Graph.HoverDetail({
                graph: graph,
                formatter: function(series, x, y) {
                    var date = '<span class="date">' + new Date(x * 1000).toUTCString() + '</span>';
                    var swatch = '<span class="detail_swatch" style="background-color: ' + series.color + '"></span>';
                    var content = swatch + series.name + ": " + parseInt(y) + '<br>' + date;
                    return content;
                }
            });

            graph.render();


            $(window).resize(function() {
                graph.configure({
                    width: $(container).width(),
                    height: 500
                });
                graph.render()
            });

            $(container).data('chart', graph);

        })();


        // Renders an area chart with a slider option using Rickshaw
        (function() {

            var seriesData = [
                []
            ];
            var random = new Rickshaw.Fixtures.RandomData(50);

            for (var i = 0; i < 75; i++) {
                random.addData(seriesData);
            }

            var graph = new Rickshaw.Graph({
                element: document.querySelector("#rickshaw-slider .chart"),
                renderer: 'multi',
                dotSize: 5,
                height: 500,
                width: 700,
                padding: {
                    left: 0.5
                },
                series: [{
                    name: 'Temperature',
                    data: seriesData.shift(),
                    color: $.Pages.getColor('success-light', .5), // Get Pages contextual color
                    opacity: 0,
                    renderer: 'stack'
                }]
            });

            var y_ticks = new Rickshaw.Graph.Axis.Y({
                graph: graph,
                orientation: 'left',
                pixelsPerTick: 50,
                tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
                element: document.querySelector('#rickshaw-slider .y_axis')
            });

            var x_ticks = new Rickshaw.Graph.Axis.Time({
                graph: graph,
                timeFixture: new Rickshaw.Fixtures.Time()
            });

            var slider = new Rickshaw.Graph.RangeSlider.Preview({
                graph: graph,
                height: 100,
                element: document.querySelector('#rickshaw-slider .slider')
            });

            var hoverDetail = new Rickshaw.Graph.HoverDetail({
                graph: graph,
                formatter: function(series, x, y) {
                    var date = '<span class="date">' + new Date(x * 1000).toUTCString() + '</span>';
                    var swatch = '<span class="detail_swatch" style="background-color: ' + series.color + '"></span>';
                    var content = swatch + series.name + ": " + parseInt(y) + '<br>' + date;
                    return content;
                }
            });

            graph.render();

            $(window).resize(function() {
                graph.configure({
                    width: $('#rickshaw-slider .chart').width(),
                    height: $('#rickshaw-slider .chart').height()
                });

                graph.render()
            });

            $('#rickshaw-slider .rickshaw-chart').data('chart', graph);

        })();



        /* ============================================================
         * NVD3 Charts
         * ============================================================ */

        // Load chart data
        d3.json('http://pages.revox.io/json/charts.json', function(data) {

            (function() {

                // Renders a stacked area chart
                nv.addGraph(function() {
                    var chart = nv.models.stackedAreaChart()
                        // Gets color (rgba) value using Pages util function $.Pages.getColor()
                        .color([
                            $.Pages.getColor('success', .7),
                            $.Pages.getColor('info'),
                            $.Pages.getColor('primary', .87), //south america
                            $.Pages.getColor('warning'),
                            $.Pages.getColor('complete', .67), //europe
                            $.Pages.getColor('success-dark'),
                            $.Pages.getColor('menu', .2) //antarctica
                        ])
                        .margin({
                            left: 15
                        })
                        .x(function(d) {
                            return d[0]
                        }) //We can modify the data accessor functions...
                        .y(function(d) {
                            return d[1]
                        }) //...in case your data is formatted differently.
                        .useInteractiveGuideline(true) //Tooltips which show all data points. Very nice!
                        .rightAlignYAxis(true) //Let's move the y-axis to the right side.
                        .transitionDuration(500)
                        .showControls(true) //Allow user to choose 'Stacked', 'Stream', 'Expanded' mode.
                        .clipEdge(true);

                    //Format x-axis labels with custom function.
                    chart.xAxis
                        .tickFormat(function(d) {
                            return d3.time.format('%a')(new Date(d))
                        });

                    chart.yAxis
                        .tickFormat(d3.format('d'));



                    chart.legend.margin({
                        top: 30
                    });

                    d3.select('#nvd3-area svg')
                        .datum(data.nvd3.stackedArea)
                        .call(chart);

                    var xTicks = d3.select('.nv-y.nv-axis  g').selectAll('g');
                    xTicks
                        .selectAll('text')
                        .attr('transform', function(d, i, j) {
                            return 'translate (8, 0)'
                        });

                    var yTicks = d3.select('.nv-x.nv-axis  g').selectAll('g');
                    yTicks
                        .selectAll('text')
                        .attr('transform', function(d, i, j) {
                            return 'translate (0, 10)'
                        });

                    var minmax = d3.select('.nv-x.nv-axis g');
                    minmax
                        .selectAll('text')
                        .attr('transform', function(d, i, j) {
                            return 'translate (0, 10)'
                        });


                    var legend = d3.select('.nv-legendWrap .nv-legend');
                    legend.attr('transform', function(d, i, j) {
                        return 'translate (0, -20)'
                    });


                    nv.utils.windowResize(function() {

                        chart.update();

                        var xTicks = d3.select('.nv-y.nv-axis  g').selectAll('g');
                        xTicks
                            .selectAll('text')
                            .attr('transform', function(d, i, j) {
                                return 'translate (10, 0)'
                            });

                        var yTicks = d3.select('.nv-x.nv-axis  g').selectAll('g');
                        yTicks
                            .selectAll('text')
                            .attr('transform', function(d, i, j) {
                                return 'translate (0, 10)'
                            });

                        var minmax = d3.select('.nv-x.nv-axis g');
                        minmax
                            .selectAll('text')
                            .attr('transform', function(d, i, j) {
                                return 'translate (0, 10)'
                            });


                        var legend = d3.select('.nv-legendWrap .nv-legend');
                        legend.attr('transform', function(d, i, j) {
                            return 'translate (0, -20)'
                        });

                    });

                    $('#nvd3-area').data('chart', chart);

                    return chart;
                });

            })();

            // Renders a line chart
            (function() {
                nv.addGraph(function() {
                    var chart = nv.models.lineChart()
                        .x(function(d) {
                            return d[0]
                        })
                        .y(function(d) {
                            return d[1] / 100
                        })
                        .color([
                            $.Pages.getColor('success'),
                            $.Pages.getColor('danger'),
                            $.Pages.getColor('primary'), //south america

                            $.Pages.getColor('complete'), //europe

                        ])
                        .useInteractiveGuideline(true);

                    chart.xAxis
                        .tickFormat(function(d) {
                            return d3.time.format('%x')(new Date(d))
                        });

                    chart.yAxis.tickFormat(d3.format(',.2f'));

                    d3.select('#nvd3-line svg')
                        .datum(data.nvd3.line)
                        .transition().duration(500)
                        .call(chart);

                    nv.utils.windowResize(chart.update);

                    $('#nvd3-line').data('chart', chart);

                    return chart;
                });
            })();

            // Renders a line chart
            (function() {
                nv.addGraph(function() {
                    var chart = nv.models.lineChart()
                        .x(function(d) {
                            return d[0]
                        })
                        .y(function(d) {
                            return d[1] / 100
                        })
                        .color([
                            $.Pages.getColor('success')
                        ])
                        .useInteractiveGuideline(true);

                    chart.xAxis
                        .tickFormat(function(d) {
                            return d3.time.format('%x')(new Date(d))
                        });

                    chart.yAxis.tickFormat(d3.format(',.2f'));

                    d3.select('#nvd3-line2 svg')
                        .datum(data.nvd3.monthSales)
                        .transition().duration(500)
                        .call(chart);


                    nv.utils.windowResize(function() {

                        chart.update();
                        setTimeout(function() {
                            d3.selectAll('#nvd3-line2 .nvd3 circle.nv-point').attr("r", "4");
                        }, 300);
                    });


                    $('#nvd3-line2').data('chart', chart);

                    return chart;
                }, function() {

                });
            })();

        });

        /* ============================================================
         * Sparkline Charts
         * ============================================================ */

        // Renders a pie chart
        var drawSparklinePie = function() {
            $("#sparkline-pie").sparkline([4, 3, 2, 1], {
                type: 'pie',
                width: $("#sparkline-pie").width(),
                height: '200',
                sliceColors: [$.Pages.getColor('warning'), $.Pages.getColor('danger'), $.Pages.getColor('master-light'), $.Pages.getColor('master')]

            });

        }

        // Renders a line chart 
        var drawSparklineLine = function() {
            var elemWidth = $("#sparkline-line").width();
            $("#sparkline-line").sparkline([0, 10, 8, 20, 15, 10, 15, 5], {
                type: 'line',
                width: Math.round(elemWidth),
                height: '200',
                chartRangeMax: 40,
                fillColor: $.Pages.getColor('danger', .3), // Get Pages contextual color
                lineColor: 'rgba(0,0,0,0)',
                highlightLineColor: 'rgba(0,0,0,.09)',
                highlightSpotColor: 'rgba(0,0,0,.21)',

            });

            $("#sparkline-line").sparkline([10, 10, 25, 29, 20, 22, 20, 22], {
                type: 'line',
                width: Math.round(elemWidth),
                height: '200',
                fillColor: $.Pages.getColor('warning', .3), // Get Pages contextual color
                lineColor: 'rgba(0,0,0,0)',
                highlightLineColor: 'rgba(0,0,0,.09)',
                highlightSpotColor: 'rgba(0,0,0,.21)',
                composite: true // draws the new chart on top of a previously rendered chart
            });
        }

        drawSparklineLine();
        drawSparklinePie();

        var sparkResize;

        // Make charts to have responsive widths and heights
        $(window).resize(function(e) {
            clearTimeout(sparkResize);
            sparkResize = setTimeout(function() {
                drawSparklineLine();
                drawSparklinePie();
            }, 500);
        });


        // Redraw charts on tab change because charts are drawn when their parent tabs are hidden
        $('#tabs-rickshaw a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
            var chart;
            var target = $(e.target).attr('data-target');
            var tabPane = $(target);
            var chart = tabPane.find('.rickshaw-chart').data('chart');

            chart.configure({
                width: tabPane.width(),
                height: 500
            });

            chart.render()

        });

        $('#tabs-nvd3 a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
            var target = $(e.target).attr('data-target');
            var tabPane = $(target);
            var chart = tabPane.find('.line-chart').data('chart');
            chart.update();

            setTimeout(function() {
                d3.selectAll('#nvd3-line2 .nvd3 circle.nv-point').attr("r", "4");
            }, 300);
        });

        $('#tabs-sparkline a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
            var target = $(e.target).attr('data-target');
            var tabPane = $(target);

            if (tabPane.find('#sparkline-pie').length) {
                drawSparklinePie();
            } else if (tabPane.find('#sparkline-line').length) {
                drawSparklineLine();
            }

        });

    });
})(window.jQuery);