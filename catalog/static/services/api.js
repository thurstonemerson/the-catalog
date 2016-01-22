angular.module('MyApp')
  .factory('API', function($http) {
    return {
      getComposers: function() {
        return $http.get('/api/catalog/composers/JSON');
      },
      updateComposer: function(composerData) {
        return $http.post('/api/catalog/updatecomposer', composerData);
      }
    };
  });