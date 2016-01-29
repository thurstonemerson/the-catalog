angular.module('MyApp').factory('API', function($http) {
	return {
		getComposers : function() {
			return $http.get('/api/catalog/composers/JSON');
		},
		getMusicItems : function(composerID) {
			return $http.get('/api/catalog/composer/' + composerID + '/musicitems/JSON');
		},
		updateComposer : function(composerData) {
			return $http.post('/api/catalog/updatecomposer', composerData);
		},
		addComposer : function(composerData) {
			return $http.post('/api/catalog/addcomposer', composerData);
		},
		deleteComposer : function(composerData) {
			return $http.post('/api/catalog/deletecomposer', composerData);
		}
	};
});