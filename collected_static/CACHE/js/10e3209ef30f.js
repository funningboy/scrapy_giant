
			AmCharts.ready(function () {
				generateChartData();
				createStockChart();
			});

			var chart;
			var chartData = [];
			var newPanel;
			var stockPanel;

			function generateChartData() {
                
                    
					    chartData.push({
                            date: new Date("2014-11-11T00:00:00"),
                            open: 98.6,
                            close: 97.7,
                            high: 98.6,
                            low: 97.5,
                            volume: 22857
                        });
                    
					    chartData.push({
                            date: new Date("2014-11-10T00:00:00"),
                            open: 95.2,
                            close: 98.3,
                            high: 98.4,
                            low: 95.2,
                            volume: 35347
                        });
                    
					    chartData.push({
                            date: new Date("2014-11-07T00:00:00"),
                            open: 95.2,
                            close: 96.3,
                            high: 96.5,
                            low: 95.1,
                            volume: 18107
                        });
                    
					    chartData.push({
                            date: new Date("2014-11-06T00:00:00"),
                            open: 97.2,
                            close: 95.9,
                            high: 97.9,
                            low: 95.8,
                            volume: 26712
                        });
                    
					    chartData.push({
                            date: new Date("2014-11-05T00:00:00"),
                            open: 98.5,
                            close: 98.2,
                            high: 98.5,
                            low: 97.4,
                            volume: 16066
                        });
                    
					    chartData.push({
                            date: new Date("2014-11-04T00:00:00"),
                            open: 98.7,
                            close: 97.5,
                            high: 98.7,
                            low: 97.4,
                            volume: 19243
                        });
                    
					    chartData.push({
                            date: new Date("2014-11-03T00:00:00"),
                            open: 97.0,
                            close: 98.1,
                            high: 98.7,
                            low: 96.5,
                            volume: 38018
                        });
                    
					    chartData.push({
                            date: new Date("2014-10-31T00:00:00"),
                            open: 95.4,
                            close: 96.0,
                            high: 96.2,
                            low: 95.0,
                            volume: 28039
                        });
                    
					    chartData.push({
                            date: new Date("2014-10-30T00:00:00"),
                            open: 95.0,
                            close: 95.2,
                            high: 95.5,
                            low: 94.7,
                            volume: 15900
                        });
                    
					    chartData.push({
                            date: new Date("2014-10-29T00:00:00"),
                            open: 96.0,
                            close: 95.0,
                            high: 96.2,
                            low: 94.8,
                            volume: 28653
                        });
                    
					    chartData.push({
                            date: new Date("2014-10-28T00:00:00"),
                            open: 95.0,
                            close: 95.5,
                            high: 95.8,
                            low: 95.0,
                            volume: 32009
                        });
                    
					    chartData.push({
                            date: new Date("2014-10-27T00:00:00"),
                            open: 93.5,
                            close: 94.0,
                            high: 94.5,
                            low: 93.3,
                            volume: 20843
                        });
                    
					    chartData.push({
                            date: new Date("2014-10-24T00:00:00"),
                            open: 95.0,
                            close: 93.2,
                            high: 95.3,
                            low: 93.1,
                            volume: 22843
                        });
                    
					    chartData.push({
                            date: new Date("2014-10-23T00:00:00"),
                            open: 95.0,
                            close: 95.0,
                            high: 95.0,
                            low: 94.2,
                            volume: 22871
                        });
                    
					    chartData.push({
                            date: new Date("2014-10-22T00:00:00"),
                            open: 95.0,
                            close: 94.0,
                            high: 95.5,
                            low: 94.0,
                            volume: 33940
                        });
                    
					    chartData.push({
                            date: new Date("2014-10-21T00:00:00"),
                            open: 94.0,
                            close: 93.5,
                            high: 94.6,
                            low: 93.0,
                            volume: 36618
                        });
                    
					    chartData.push({
                            date: new Date("2014-10-20T00:00:00"),
                            open: 91.0,
                            close: 93.2,
                            high: 93.4,
                            low: 90.8,
                            volume: 34994
                        });
                    
					    chartData.push({
                            date: new Date("2014-10-17T00:00:00"),
                            open: 92.5,
                            close: 89.0,
                            high: 92.8,
                            low: 89.0,
                            volume: 66228
                        });
                    
					    chartData.push({
                            date: new Date("2014-10-16T00:00:00"),
                            open: 93.0,
                            close: 92.2,
                            high: 93.4,
                            low: 90.6,
                            volume: 52554
                        });
                    
					    chartData.push({
                            date: new Date("2014-10-15T00:00:00"),
                            open: 95.5,
                            close: 93.5,
                            high: 95.7,
                            low: 92.4,
                            volume: 90024
                        });
                    
					    chartData.push({
                            date: new Date("2014-10-14T00:00:00"),
                            open: 95.6,
                            close: 96.0,
                            high: 96.1,
                            low: 95.0,
                            volume: 32867
                        });
                    
					    chartData.push({
                            date: new Date("2014-10-13T00:00:00"),
                            open: 95.0,
                            close: 95.8,
                            high: 96.7,
                            low: 95.0,
                            volume: 35801
                        });
                    
					    chartData.push({
                            date: new Date("2014-10-09T00:00:00"),
                            open: 98.2,
                            close: 97.6,
                            high: 98.3,
                            low: 96.7,
                            volume: 27512
                        });
                    
					    chartData.push({
                            date: new Date("2014-10-08T00:00:00"),
                            open: 96.5,
                            close: 96.7,
                            high: 97.6,
                            low: 96.5,
                            volume: 22228
                        });
                    
					    chartData.push({
                            date: new Date("2014-10-07T00:00:00"),
                            open: 98.6,
                            close: 97.6,
                            high: 99.0,
                            low: 97.0,
                            volume: 27137
                        });
                    
					    chartData.push({
                            date: new Date("2014-10-06T00:00:00"),
                            open: 99.7,
                            close: 98.5,
                            high: 99.7,
                            low: 98.5,
                            volume: 22887
                        });
                    
					    chartData.push({
                            date: new Date("2014-10-03T00:00:00"),
                            open: 98.0,
                            close: 99.3,
                            high: 99.7,
                            low: 97.9,
                            volume: 24011
                        });
                    
					    chartData.push({
                            date: new Date("2014-10-02T00:00:00"),
                            open: 97.8,
                            close: 97.5,
                            high: 98.4,
                            low: 97.1,
                            volume: 23725
                        });
                    
					    chartData.push({
                            date: new Date("2014-10-01T00:00:00"),
                            open: 96.5,
                            close: 98.4,
                            high: 98.6,
                            low: 95.5,
                            volume: 30242
                        });
                    
					    chartData.push({
                            date: new Date("2014-09-30T00:00:00"),
                            open: 97.5,
                            close: 96.0,
                            high: 97.5,
                            low: 94.8,
                            volume: 53444
                        });
                    
					    chartData.push({
                            date: new Date("2014-09-29T00:00:00"),
                            open: 97.8,
                            close: 97.6,
                            high: 98.2,
                            low: 97.1,
                            volume: 38784
                        });
                    
					    chartData.push({
                            date: new Date("2014-09-26T00:00:00"),
                            open: 99.0,
                            close: 97.1,
                            high: 99.0,
                            low: 97.1,
                            volume: 58713
                        });
                    
					    chartData.push({
                            date: new Date("2014-09-25T00:00:00"),
                            open: 101.0,
                            close: 100.0,
                            high: 102.5,
                            low: 99.6,
                            volume: 35162
                        });
                    
					    chartData.push({
                            date: new Date("2014-09-24T00:00:00"),
                            open: 100.0,
                            close: 100.5,
                            high: 101.0,
                            low: 100.0,
                            volume: 16931
                        });
                    
					    chartData.push({
                            date: new Date("2014-09-23T00:00:00"),
                            open: 100.5,
                            close: 100.5,
                            high: 101.0,
                            low: 99.8,
                            volume: 16015
                        });
                    
					    chartData.push({
                            date: new Date("2014-09-22T00:00:00"),
                            open: 100.5,
                            close: 100.5,
                            high: 100.5,
                            low: 99.6,
                            volume: 24844
                        });
                    
					    chartData.push({
                            date: new Date("2014-09-19T00:00:00"),
                            open: 102.5,
                            close: 101.0,
                            high: 103.0,
                            low: 101.0,
                            volume: 32404
                        });
                    
					    chartData.push({
                            date: new Date("2014-09-18T00:00:00"),
                            open: 100.5,
                            close: 102.0,
                            high: 102.0,
                            low: 100.5,
                            volume: 22083
                        });
                    
					    chartData.push({
                            date: new Date("2014-09-17T00:00:00"),
                            open: 100.0,
                            close: 101.0,
                            high: 101.5,
                            low: 100.0,
                            volume: 27850
                        });
                    
					    chartData.push({
                            date: new Date("2014-09-16T00:00:00"),
                            open: 101.0,
                            close: 99.5,
                            high: 101.0,
                            low: 99.5,
                            volume: 15858
                        });
                    
					    chartData.push({
                            date: new Date("2014-09-15T00:00:00"),
                            open: 99.4,
                            close: 101.0,
                            high: 101.0,
                            low: 99.2,
                            volume: 17076
                        });
                    
					    chartData.push({
                            date: new Date("2014-09-12T00:00:00"),
                            open: 100.5,
                            close: 99.4,
                            high: 100.5,
                            low: 99.1,
                            volume: 23455
                        });
                    
					    chartData.push({
                            date: new Date("2014-09-11T00:00:00"),
                            open: 100.5,
                            close: 100.0,
                            high: 101.5,
                            low: 100.0,
                            volume: 18011
                        });
                    
					    chartData.push({
                            date: new Date("2014-09-10T00:00:00"),
                            open: 101.0,
                            close: 101.0,
                            high: 101.5,
                            low: 99.6,
                            volume: 30085
                        });
                    
					    chartData.push({
                            date: new Date("2014-09-09T00:00:00"),
                            open: 101.0,
                            close: 102.0,
                            high: 102.0,
                            low: 100.5,
                            volume: 25181
                        });
                    
					    chartData.push({
                            date: new Date("2014-09-05T00:00:00"),
                            open: 99.5,
                            close: 100.5,
                            high: 100.5,
                            low: 98.6,
                            volume: 37775
                        });
                    
					    chartData.push({
                            date: new Date("2014-09-04T00:00:00"),
                            open: 100.5,
                            close: 99.9,
                            high: 100.5,
                            low: 99.5,
                            volume: 42401
                        });
                    
					    chartData.push({
                            date: new Date("2014-09-03T00:00:00"),
                            open: 101.0,
                            close: 101.0,
                            high: 101.5,
                            low: 100.0,
                            volume: 29980
                        });
                    
					    chartData.push({
                            date: new Date("2014-09-02T00:00:00"),
                            open: 101.5,
                            close: 100.5,
                            high: 102.0,
                            low: 100.5,
                            volume: 22070
                        });
                    
					    chartData.push({
                            date: new Date("2014-09-01T00:00:00"),
                            open: 103.0,
                            close: 101.5,
                            high: 103.5,
                            low: 101.5,
                            volume: 29167
                        });
                    
					    chartData.push({
                            date: new Date("2014-08-29T00:00:00"),
                            open: 102.0,
                            close: 102.0,
                            high: 103.0,
                            low: 101.0,
                            volume: 40542
                        });
                    
					    chartData.push({
                            date: new Date("2014-08-28T00:00:00"),
                            open: 100.5,
                            close: 102.0,
                            high: 104.0,
                            low: 100.5,
                            volume: 105054
                        });
                    
					    chartData.push({
                            date: new Date("2014-08-27T00:00:00"),
                            open: 110.0,
                            close: 112.0,
                            high: 112.0,
                            low: 110.0,
                            volume: 87045
                        });
                    
					    chartData.push({
                            date: new Date("2014-08-26T00:00:00"),
                            open: 110.5,
                            close: 110.0,
                            high: 111.0,
                            low: 109.5,
                            volume: 40265
                        });
                    
					    chartData.push({
                            date: new Date("2014-08-25T00:00:00"),
                            open: 110.0,
                            close: 110.5,
                            high: 111.0,
                            low: 109.5,
                            volume: 25906
                        });
                    
					    chartData.push({
                            date: new Date("2014-08-22T00:00:00"),
                            open: 109.0,
                            close: 110.0,
                            high: 110.0,
                            low: 108.5,
                            volume: 35790
                        });
                    
					    chartData.push({
                            date: new Date("2014-08-21T00:00:00"),
                            open: 108.5,
                            close: 108.5,
                            high: 108.5,
                            low: 107.5,
                            volume: 15557
                        });
                    
					    chartData.push({
                            date: new Date("2014-08-20T00:00:00"),
                            open: 109.5,
                            close: 108.5,
                            high: 109.5,
                            low: 107.0,
                            volume: 27207
                        });
                    
					    chartData.push({
                            date: new Date("2014-08-19T00:00:00"),
                            open: 108.5,
                            close: 108.5,
                            high: 109.5,
                            low: 107.5,
                            volume: 21745
                        });
                    
					    chartData.push({
                            date: new Date("2014-08-18T00:00:00"),
                            open: 108.0,
                            close: 107.5,
                            high: 108.5,
                            low: 107.5,
                            volume: 18848
                        });
                    
					    chartData.push({
                            date: new Date("2014-08-15T00:00:00"),
                            open: 109.0,
                            close: 107.5,
                            high: 109.5,
                            low: 107.0,
                            volume: 28562
                        });
                    
					    chartData.push({
                            date: new Date("2014-08-14T00:00:00"),
                            open: 109.5,
                            close: 109.0,
                            high: 111.0,
                            low: 108.0,
                            volume: 38756
                        });
                    
					    chartData.push({
                            date: new Date("2014-08-13T00:00:00"),
                            open: 104.5,
                            close: 106.0,
                            high: 106.5,
                            low: 104.5,
                            volume: 26383
                        });
                    
					    chartData.push({
                            date: new Date("2014-08-12T00:00:00"),
                            open: 104.0,
                            close: 104.5,
                            high: 105.5,
                            low: 103.5,
                            volume: 22237
                        });
                    
					    chartData.push({
                            date: new Date("2014-08-11T00:00:00"),
                            open: 101.0,
                            close: 104.0,
                            high: 105.0,
                            low: 100.5,
                            volume: 35057
                        });
                    
					    chartData.push({
                            date: new Date("2014-08-08T00:00:00"),
                            open: 103.5,
                            close: 102.5,
                            high: 103.5,
                            low: 101.5,
                            volume: 19775
                        });
                    
                
			}

			function createStockChart() {
				chart = new AmCharts.AmStockChart();
                chart.pathToImages ="/static/amcharts/images/";
				chart.balloon.horizontalPadding = 13;

				// DATASET //////////////////////////////////////////
				var dataSet = new AmCharts.DataSet();
				dataSet.fieldMappings = [{
					fromField: "open",
					toField: "open"
				}, {
					fromField: "close",
					toField: "close"
				}, {
					fromField: "high",
					toField: "high"
				}, {
					fromField: "low",
					toField: "low"
				}, {
					fromField: "volume",
					toField: "volume"
				}, {
					fromField: "value",
					toField: "value"
				}];
				dataSet.color = "#7f8da9";
				dataSet.dataProvider = chartData;
				dataSet.categoryField = "date";

				chart.dataSets = [dataSet];

				// PANELS ///////////////////////////////////////////
				stockPanel = new AmCharts.StockPanel();
				stockPanel.title = "Value";

				// graph of first stock panel
				var graph = new AmCharts.StockGraph();
				graph.type = "candlestick";
				graph.openField = "open";
				graph.closeField = "close";
				graph.highField = "high";
				graph.lowField = "low";
				graph.valueField = "close";
				graph.lineColor = "#7f8da9";
				graph.fillColors = "#7f8da9";
				graph.negativeLineColor = "#db4c3c";
				graph.negativeFillColors = "#db4c3c";
				graph.fillAlphas = 1;
				graph.balloonText = "open:<b>[[open]]</b><br>close:<b>[[close]]</b><br>low:<b>[[low]]</b><br>high:<b>[[high]]</b>";
				graph.useDataSetColors = false;
				stockPanel.addStockGraph(graph);

				var stockLegend = new AmCharts.StockLegend();
				stockLegend.markerType = "none";
				stockLegend.markerSize = 0;
				stockLegend.valueTextRegular = undefined;
				stockLegend.valueWidth = 250;
				stockPanel.stockLegend = stockLegend;

				chart.panels = [stockPanel];


				// OTHER SETTINGS ////////////////////////////////////
				var sbsettings = new AmCharts.ChartScrollbarSettings();
				sbsettings.graph = graph;
				sbsettings.graphType = "line";
				sbsettings.usePeriod = "WW";
				chart.chartScrollbarSettings = sbsettings;

				// Enable pan events
				var panelsSettings = new AmCharts.PanelsSettings();
				panelsSettings.panEventsEnabled = true;
				chart.panelsSettings = panelsSettings;

				// CURSOR
				var cursorSettings = new AmCharts.ChartCursorSettings();
				cursorSettings.valueBalloonsEnabled = true;
				cursorSettings.fullWidth = true;
				cursorSettings.cursorAlpha = 0.1;
				chart.chartCursorSettings = cursorSettings;

				// PERIOD SELECTOR ///////////////////////////////////
				var periodSelector = new AmCharts.PeriodSelector();
				periodSelector.position = "bottom";
				periodSelector.periods = [{
					period: "DD",
					count: 10,
					label: "10 days"
				}, {
					period: "MM",
					selected: true,
					count: 1,
					label: "1 month"
				}, {
					period: "YYYY",
					count: 1,
					label: "1 year"
				}, {
					period: "YTD",
					label: "YTD"
				}, {
					period: "MAX",
					label: "MAX"
				}];
				chart.periodSelector = periodSelector;


				chart.write('chartdiv');
			}



			function addPanel() {
				newPanel = new AmCharts.StockPanel();
				newPanel.allowTurningOff = true;
				newPanel.title = "Volume";
				newPanel.showCategoryAxis = false;

				var graph = new AmCharts.StockGraph();
				graph.valueField = "volume";
				graph.fillAlphas = 0.15;
				newPanel.addStockGraph(graph);

				var legend = new AmCharts.StockLegend();
				legend.markerType = "none";
				legend.markerSize = 0;
				newPanel.stockLegend = legend;

				chart.addPanelAt(newPanel, 1);
				chart.validateNow();

				document.getElementById("addPanelButton").disabled = true;
				document.getElementById("removePanelButton").disabled = false;
			}

			function removePanel() {
				chart.removePanel(newPanel);
				chart.validateNow();

				document.getElementById("addPanelButton").disabled = false;
				document.getElementById("removePanelButton").disabled = true;
			}

        