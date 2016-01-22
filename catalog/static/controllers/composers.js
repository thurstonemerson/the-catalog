angular.module('MyApp')
  .controller('ComposerCtrl', function($scope, $auth, toastr, API) {


	//call the rest service to extract all of the composers
    $scope.getComposers = function() {
      API.getComposers()
        .then(function(response) {
          console.log(response.data);
          $scope.response = response.data;
          
          // convert the date strings into a date object
          for(var i = 0; i < $scope.response.composers.length; i++){
            console.log($scope.response.composers[i].dateOfBirth);
            $scope.response.composers[i].dateOfBirth = new Date($scope.response.composers[i].dateOfBirth); 
            $scope.response.composers[i].dateOfDeath = new Date($scope.response.composers[i].dateOfDeath); 
          }
          
          $scope.originalComposers = angular.copy($scope.response);
          
        })
        .catch(function(response) {
          toastr.error(response.data.message, response.status);
        });
    };
    
    //if cancel button is pressed reset the composer details back to the original
    $scope.reset = function(composerID) {
      console.log("resetting composer back to original");
	  console.log($scope.originalComposers);
	  
	  //brute force find of composers, lets pray the composer list isn't too long
      for(var i = 0; i < $scope.originalComposers.composers.length; i++){
    	  if ($scope.originalComposers.composers[i].id == composerID){
    		  console.log("matching result " + composerID);
    		  for(var k = 0; k < $scope.response.composers.length; k++){
    	    	  if ($scope.response.composers[k].id == composerID){
    	    	      console.log("found and reset composer " + composerID);
    	    		  $scope.response.composers[k] = angular.copy($scope.originalComposers.composers[i])
    	      }
    	    }
    	  }
        }
      
      console.log($scope.response);
    };
    
    //when submit button is pressed, update the particular edited composer
    $scope.updateComposer = function(composer) {
    	console.log(composer);
    	API.updateComposer(composer)
        .then(function(response) {
          toastr.success(response.data.message);
        })
        .catch(function(response) {
          toastr.error(response.data.message, response.status);
        });
    };
    
    //call the API function to retrieve all composers
    $scope.getComposers();
  });
