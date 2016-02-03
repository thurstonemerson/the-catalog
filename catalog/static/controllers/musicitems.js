angular.module('MyApp')
  .controller('MusicItemsCtrl', function($state, $scope, $stateParams, moment, toastr, API) {
	  
	// call the rest service to extract all of the composers
	    $scope.getMusicItems = function(composerID) {
	      API.getMusicItems(composerID)
	        .then(function(response) {
	          console.log(response.data);
	          
	          $scope.response = response.data;
	          
	          musicItems = []
	          
	          // convert the date strings into a date object
	          for(var i = 0; i < $scope.response.musicItems.length; i++){
	             
	            if ($scope.response.musicItems[i].dateAdded.length > 0){
	            	$scope.response.musicItems[i].dateAdded = new Date(moment($scope.response.musicItems[i].dateAdded).startOf('day'));
	            }
	            
	            if ($scope.response.musicItems[i].dateOfComposition.length > 0){
	            	$scope.response.musicItems[i].dateOfComposition = new Date(moment($scope.response.musicItems[i].dateOfComposition).startOf('day'));
	            }
	            
	            musicItems[$scope.response.musicItems[i].id] = $scope.response.musicItems[i];
	          }
	          
	          // save a copy of the original data in case the user presses
				// cancel
	          $scope.originalMusicItems = angular.copy(musicItems);
	          
	          console.log($scope.response.musicItems);
	        })
	        .catch(function(response) {
	          toastr.error(response.data.message, response.status);
	        });
	    };
	    
	    // if cancel button is pressed reset the composer details back to the
		// original
	    $scope.reset = function(musicItemID) {
	      console.log("resetting music item back to original");
		  console.log($scope.originalMusicItems);

		  // reset details provided we can find them
		  if ( $scope.originalMusicItems[musicItemID] != undefined && 
				  $scope.originalMusicItems[musicItemID] != null ) {
			 
	          for(var i = 0; i < $scope.response.musicItems.length; i++){
	        	  if ($scope.response.musicItems[i].id === musicItemID){
	        	     $scope.response.musicItems[i] = angular.copy($scope.originalMusicItems[musicItemID]);
					 console.log("found and reset music item " + musicItemID);
					 return;
	        	  }
			  }
		  }
	    };
	    
	    // reset the add composer form back to a pristine state
	    $scope.resetAddMusicItem = function(musicItemID) {
	        console.log("resetting add music item form back to original");
	  		$scope.reset(musicItemID);
	  	    $scope.addMusicItemForm.$setPristine();
	    };
	    
	    //when delete button is pressed, delete the file from the database
	    $scope.deleteMusicFile = function(musicItem, file) {
	    	console.log("Deleting " + file.path);
	    };
	    
	    // when submit button is pressed, upload the selected file
	    $scope.uploadMusicFile = function(musicItem, uploadfile) {
	    	if (uploadfile != null && uploadfile != undefined){   		
	    		console.log("Uploading " + uploadfile.name);
	    		
	    		//check that the file to upload isn't too big
		    	if (uploadfile != undefined && uploadfile != null){
		    		if (!checkFileSize(uploadfile)){
		    			toastr.error(uploadfile.name + " is larger than 2MB");
		    			return;
		    		}
		    	}
	    		
	    		API.uploadFile(uploadfile, musicItem)
		        .then(function(response) {
		          toastr.success(response.data.message);
		          $state.reload();
		        })
		        .catch(function(response) {
		          toastr.error(response.data.message, response.status);
		        });
	    	} else {
	    		 toastr.error("Enter a file to upload");
	    	}
	    };
	    
	    // when submit button is pressed, update the particular edited music item
	    $scope.updateMusicItem = function(musicItem) {
	    	console.log("Updating " + musicItem.name);
	    	
	    	API.updateMusicItem(musicItem)
	        .then(function(response) {
	          toastr.success(response.data.message);
	        })
	        .catch(function(response) {
	          toastr.error(response.data.message, response.status);
	        });
	    };
	    
	    // when submit button is pressed, update the particular edited composer
	    $scope.addMusicItem = function(musicItem, uploadFile) {
	    	console.log("Adding " + musicItem.name);
	    	
	    	//Set some default values for number and key so that we can
	    	//more easily parse them at the server end
	    	if (musicItem.number == undefined || musicItem.number == null){
	    		musicItem.number = "";
	    	}
	    	
	    	if (musicItem.key == undefined || musicItem.key == null){
	    		musicItem.key = "";
	    	}
	    	
	    	//check that the file to upload isn't too big
	    	if (uploadFile != undefined && uploadFile != null){
	    		if (!checkFileSize(uploadFile)){
	    			toastr.error(uploadFile.name + " is larger than 2MB");
	    			return;
	    		}
	    	}
	    	
	    	API.addMusicItem($state.composerID, musicItem, uploadFile)
	        .then(function(response) {
	          toastr.success(response.data.message);
	          $state.reload();
	        })
	        .catch(function(response) {
	          toastr.error(response.data.message, response.status);
	        });
	    };
	    
	    // when submit button is pressed, delete the music item
	    $scope.deleteMusicItem = function(musicItem) {
	    	console.log("Deleting " + musicItem);
	    	API.deleteMusicItem(musicItem)
	    	.then(function(response) {
	    		toastr.success(response.data.message);
	            $state.reload();
	    	})
	    	.catch(function(response) {
	    		toastr.error(response.data.message, response.status);
	    	});
	    };
	    
	    //check that an input file is not larger than 2 MB
	    function checkFileSize(file){
	    	var fileSize = file.size; // in bytes
	    	var maxSize = ((Math.pow(1024, 2))*2); //maxsize is 2 MB
	    	console.log('max size is  ' + maxSize + ' bytes');
	    	if(fileSize > maxSize){
	    		return false;
	    	}
	    	return true;
        }
	    
	    
	    $state.composerID = $stateParams.composerID;
	    $scope.getMusicItems($state.composerID);
	 
  });
