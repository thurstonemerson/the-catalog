
//Angular service calling the python rest API to perform CRUD operations
angular.module('MyApp')
		.factory('API',
				function($http) {
					return {
						//get composers for currently logged in user
						getComposers : function() {
							return $http.get('/api/catalog/composers/JSON');
						},
						//get music items for currently logged in user
						getMusicItems : function(composerID) {
							return $http.get('/api/catalog/composer/'
									+ composerID + '/musicitems/JSON');
						},
						//update a composer given an id
						updateComposer : function(composerData) {
							return $http.post('/api/catalog/updatecomposer',
									composerData);
						},
						//upload file to server
						uploadFile : function(uploadfile, musicItemData) {
							//using formdata objects to send JSON parameters
							//and file objects to the server
							var formData = new FormData();
							formData.append('id', musicItemData.id);
							formData.append('file', uploadfile);
							console.log(musicItemData.id);
							
							return $http.post('/api/catalog/uploadfile', formData, {
								transformRequest : angular.identity,
								headers : {
									'Content-Type' : undefined
								}
							});
						},
						//update a music item given an id
						updateMusicItem : function(musicItemData) {
							return $http.post('/api/catalog/updatemusicitem',
									musicItemData);
						},
						//add a composer for currently logged in user
						addComposer : function(composerData) {
							return $http.post('/api/catalog/addcomposer',
									composerData);
						},
						//add a music item for currently logged in user
						addMusicItem : function(composerID, musicItemData,
								uploadfile) {
							//using formdata objects to send JSON parameters
							//and file objects to the server
							var formData = new FormData();
							formData.append('composer_id', composerID);
							formData.append('music_item', angular.toJson(musicItemData));
							
							if (uploadfile != undefined && uploadfile != null){
								formData.append('file', uploadfile);
							} 
			
							return $http.post('/api/catalog/addmusicitem', formData, {
								transformRequest : angular.identity,
								headers : {
									'Content-Type' : undefined
								}
							});
						},
						//delete a composer given an id
						deleteComposer : function(composerData) {
							return $http.post('/api/catalog/deletecomposer',
									composerData);
						},
						//delete a music item given an id
						deleteMusicItem : function(musicItemData) {
							return $http.post('/api/catalog/deletemusicitem',
									musicItemData);
						},
						//delete a music file given an id
						deleteMusicFile : function(musicFileData) {
							return $http.post('/api/catalog/deletemusicfile',
									musicFileData);
						}
					};
				});