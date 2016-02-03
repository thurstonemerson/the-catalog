angular.module('MyApp')
		.factory('API',
				function($http) {
					return {
						getComposers : function() {
							return $http.get('/api/catalog/composers/JSON');
						},
						getMusicItems : function(composerID) {
							return $http.get('/api/catalog/composer/'
									+ composerID + '/musicitems/JSON');
						},
						updateComposer : function(composerData) {
							return $http.post('/api/catalog/updatecomposer',
									composerData);
						},
						uploadFile : function(uploadfile, musicItemData) {
							console.log("calling upload file");

							// create form data object
							var formData = new FormData();
							formData.append('id', musicItemData.id);
							formData.append('file', uploadfile);
							
							console.log(musicItemData.id);
							
							// send the file / data to your server
							return $http.post('/api/catalog/uploadfile', formData, {
								transformRequest : angular.identity,
								headers : {
									'Content-Type' : undefined
								}
							});
						},
						updateMusicItem : function(musicItemData) {
							console.log("calling update music item");

							return $http.post('/api/catalog/updatemusicitem',
									musicItemData);
						},
						addComposer : function(composerData) {
							return $http.post('/api/catalog/addcomposer',
									composerData);
						},
						addMusicItem : function(composerID, musicItemData,
								uploadfile) {
							
							// create form data object
							var formData = new FormData();
							formData.append('composer_id', composerID);
							formData.append('music_item', angular.toJson(musicItemData));
							
							if (uploadfile != undefined && uploadfile != null){
								formData.append('file', uploadfile);
							} 
							
							console.log(angular.toJson(musicItemData));
							// send the file / data to your server
							return $http.post('/api/catalog/addmusicitem', formData, {
								transformRequest : angular.identity,
								headers : {
									'Content-Type' : undefined
								}
							});
						},
						deleteComposer : function(composerData) {
							return $http.post('/api/catalog/deletecomposer',
									composerData);
						},
						deleteMusicItem : function(musicItemData) {
							return $http.post('/api/catalog/deletemusicitem',
									musicItemData);
						},
						deleteMusicFile : function(musicFileData) {
							
							return $http.post('/api/catalog/deletemusicfile',
									musicFileData);
						}
					};
				});