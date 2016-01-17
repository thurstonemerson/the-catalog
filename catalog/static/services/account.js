angular.module('MyApp')
  .factory('Account', function($http) {
    return {
      getProfile: function() {
        return $http.get('/auth/me/JSON');
      },
      updateProfile: function(profileData) {
        return $http.put('/auth/me/JSON', profileData);
      }
    };
  });