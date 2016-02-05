//Angular controller to handle user input in the composer screen
angular.module('MyApp')
  .controller('ComposerCtrl', function($state, $scope, moment, toastr, API) {

	// call the rest service to extract all of the composers
    $scope.getComposers = function() {
      API.getComposers()
        .then(function(response) {
          console.log(response.data);
          $scope.response = response.data;
          
          // convert the date strings into a date object
          for(var i = 0; i < $scope.response.composers.length; i++){
        	  
            $scope.response.composers[i].dateOfBirth = new Date(moment($scope.response.composers[i].dateOfBirth).startOf('day'));
            
            if ($scope.response.composers[i].dateOfDeath.length > 0){
            	$scope.response.composers[i].dateOfDeath = new Date(moment($scope.response.composers[i].dateOfDeath).startOf('day'));
            }
          }
          
          // convert data into a 2D array to display in a grid with 2 columns
          // save the composer data into an array, indexed by composer id
          if ($scope.response.composers.length > 0){
        	  $scope.rows = [];
        	  var composers = [];
        	  var maxCols = 2;
        	  var maxRows = Math.ceil($scope.response.composers.length/maxCols);
        	  var count = 0;
        	  for( var i = 0 ; i < maxRows;i++){
        		  $scope.rows.push([]);
        		  for( var j = 0 ; j < maxCols;j++){
        			  if ( $scope.response.composers[count] != undefined && 
        					  $scope.response.composers[count] != null ) {
        				  $scope.rows[i][j] = $scope.response.composers[count];
        				  composers[$scope.response.composers[count].id] = $scope.response.composers[count];
        				  count++;
        			  }
        		  }
          		}
          }
          
          // save a copy of the original data in case the user presses cancel
          $scope.originalComposers = angular.copy(composers);
          
        })
        .catch(function(response) {
          toastr.error(response.data.message, response.status);
        });
    };
    
    // if cancel button is pressed reset the composer details back to the
	// original
    $scope.reset = function(composerID) {
	  // reset details provided we can find them
	  if ( $scope.originalComposers[composerID] != undefined && 
			  $scope.originalComposers[composerID] != null ) {
		 // loop through the grid and find the right composer ID
		 for(var i = 0; i <  $scope.rows.length; i++){
			 for(var k = 0; k < $scope.rows[i].length; k++){
				 console.log("composerID " + $scope.rows[i][k].id);
				 if ($scope.rows[i][k].id === composerID){
					 $scope.rows[i][k] = angular.copy( $scope.originalComposers[composerID]);
					 console.log("found and reset composer " + composerID);
					 return;
				 }
			   }
			}
	  }
    };
    
    //reset the add composer form back to a pristine state
    $scope.resetAddComposer = function(composerID) {
  		$scope.reset(composerID);
  	    $scope.addComposerForm.$setPristine();
    };
    
    
    // when submit button is pressed, update the particular edited composer
    $scope.updateComposer = function(composer) {
    	API.updateComposer(composer)
        .then(function(response) {
          toastr.success(response.data.message);
        })
        .catch(function(response) {
          toastr.error(response.data.message, response.status);
        });
    };
    
    // when submit button is pressed, add the new composer
    $scope.addComposer = function(composer) {
    	console.log("Adding " + composer.name + " " + composer.dateOfBirth + " " + composer.dateOfDeath);
    	
    	API.addComposer(composer)
        .then(function(response) {     
          toastr.success(response.data.message);
          $state.reload();
         })
        .catch(function(response) {
          toastr.error(response.data.message, response.status);
        });
     };
    
    // when submit button is pressed, delete the composer
    $scope.deleteComposer = function(composer) {
    	console.log("Deleting " + composer);
    	API.deleteComposer(composer)
    	.then(function(response) {
    		toastr.success(response.data.message);
            $state.reload();
    	})
    	.catch(function(response) {
    		toastr.error(response.data.message, response.status);
    	});
    };
    
    // call the API function to retrieve all composers
    $scope.getComposers();
    
    
  });
