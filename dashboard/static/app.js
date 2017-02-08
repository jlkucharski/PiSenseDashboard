"use strict";

function RenderChart(elementId, source, dateFormat){
	if($(elementId).children('.loader-big').length === 0){
		$(elementId).html('<div class="loader-big"></div>');
	}

	return c3.generate({
		bindto: elementId,
		data: {
			x: 'date',
			//2016-11-09 21:23:55
			xFormat: dateFormat,
			url: source
		},
		axis: {
			x: {
				type: 'timeseries',
				tick: {
					format: '%H:%M',
				}
			}
		}
	});
}


function RenderCharts(timespan = '7', sampling = '1H', dateFormat='%Y-%m-%d %H:%M:%S'){
	// temp chart
	RenderChart('#temperatureChart', '/api/temperature/' + timespan + '/' + sampling, dateFormat);

	// pressure chart
	RenderChart('#humidityChart', '/api/humidity/' + timespan + '/' + sampling, dateFormat);

	// humidity chart
	RenderChart('#pressureChart', '/api/pressure/' + timespan + '/' + sampling, dateFormat);
}


angular.module('piSenseApp', [])
  .controller('DashboardController', ['$scope','$http', function($scope, $http) {
 	var controller = {};

 	$scope.controller = controller;
 	controller.showSpinner = true;
 	controller.temperature = -1;
 	controller.sampling = '1H';
 	controller.daysRange = '7';

 	$http.get("/api/currentTemperature").then(function(response){
 		var temperature = Number(response.data);
 		controller.temperature = temperature.toFixed(2);
 		controller.showSpinner = false;
 	});

 	controller.Init = function(){

 		controller.RenderCharts();
 	};


    controller.RenderCharts = function() {
		switch(controller.sampling){
			case '1D':
				RenderCharts(controller.daysRange, controller.sampling, '%Y-%m-%d');
				break;
			default:
				RenderCharts(controller.daysRange, controller.sampling, '%Y-%m-%d %H:%M:%S');
				break;
		};
    };

    controller.UpdateResolution = function(newResolution){
    	if(typeof newResolution === 'string' && newResolution.length > 0){
    		// update the sampling
    		controller.sampling = newResolution;

    		// render charts
    		controller.RenderCharts();
    	}
    };

	controller.UpdateDaysRange = function(newRange){
    	if(typeof newRange === 'string' && newRange.length > 0){
    		// update the sampling
    		controller.daysRange = newRange;

    		// render charts
    		controller.RenderCharts();
    	}
    };
  }]);