angular.module('MyApp')
  .directive('fileChange', function() {
	  return {
	        require:"ngModel",
	        restrict: 'A',
	        link: function($scope, el, attrs, ngModel){
	            el.bind('change', function(event){
	                var files = event.target.files;
	                var file = files[0];
	                console.log(file);
	                ngModel.$setViewValue(file);
	                $scope.$apply();
	            });
	        }
	    };
	});
