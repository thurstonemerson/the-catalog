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
	          
	          // save a copy of the original data in case the user presses cancel
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
		  if ( typeof($scope.originalMusicItems[musicItemID]) !== "undefined" && 
				  $scope.originalMusicItems[musicItemID] !== null ) {
			 
	          for(var i = 0; i < $scope.response.musicItems.length; i++){
	        	  if ($scope.response.musicItems[i].id === musicItemID){
	        	     $scope.response.musicItems[i] = angular.copy($scope.originalMusicItems[musicItemID]);
					 console.log("found and reset music item " + musicItemID);
					 return;
	        	  }
			  }
		  }
	    };
	    
	    // when submit button is pressed, update the particular edited composer
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
	    
	    
	    $state.composerID = $stateParams.composerID;
	    $scope.getMusicItems($state.composerID);
	 
  });
