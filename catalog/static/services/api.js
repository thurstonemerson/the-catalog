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
		updateMusicItem : function(musicItemData) {
			return $http.post('/api/catalog/updatemusicitem', musicItemData);
		},
		addComposer : function(composerData) {
			return $http.post('/api/catalog/addcomposer', composerData);
		},
		addMusicItem : function(composerID, musicItemData) {
			return $http.post('/api/catalog/composer/' + composerID + '/addmusicitem', musicItemData);
		},
		deleteComposer : function(composerData) {
			return $http.post('/api/catalog/deletecomposer', composerData);
		},
		deleteMusicItem : function(musicItemData) {
			return $http.post('/api/catalog/deletemusicitem', musicItemData);
		}
	};
});