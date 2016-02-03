angular.module('MyApp', ['ngResource', 'ngMessages', 'ngAnimate', 'toastr', 'ui.router', 'satellizer', 'angularMoment', 'bootstrap.fileField'])
.config(function($stateProvider, $urlRouterProvider, $authProvider) {
    $stateProvider
      .state('home', {
        url: '/',
        controller: 'HomeCtrl',
        templateUrl: 'partials/home.html'
      })
      .state('login', {
        url: '/login',
        templateUrl: 'partials/login.html',
        controller: 'LoginCtrl',
        resolve: {
          skipIfLoggedIn: skipIfLoggedIn
        }
      })
      .state('signup', {
        url: '/signup',
        templateUrl: 'partials/signup.html',
        controller: 'SignupCtrl',
        resolve: {
          skipIfLoggedIn: skipIfLoggedIn
        }
      })
      .state('logout', {
        url: '/logout',
        template: null,
        controller: 'LogoutCtrl'
      })
      .state('composers', {
          url: '/composers',
          templateUrl: 'partials/composers.html',
          controller: 'ComposerCtrl',
          resolve: {
            loginRequired: loginRequired
          }
       })
      .state('musicitems', {
          url: '/composers/:composerID',
          templateUrl: 'partials/musicitems.html',
          controller: 'MusicItemsCtrl',
          resolve: {
              loginRequired: loginRequired
            }
        });

    $urlRouterProvider.otherwise('/');

    $authProvider.facebook({
      clientId: '1520182264948988'
    });

    $authProvider.google({
      clientId: '947884877821-gjbld23q7j0mva9u9ohldjr97ctkrdon.apps.googleusercontent.com'
    });

    $authProvider.twitter({
      url: '/auth/twitter'
    });
  	
    function skipIfLoggedIn($q, $auth) {
      var deferred = $q.defer();
      if ($auth.isAuthenticated()) {
        deferred.reject();
      } else {
        deferred.resolve();
      }
      return deferred.promise;
    }

    function loginRequired($q, $location, $auth) {
      var deferred = $q.defer();
      if ($auth.isAuthenticated()) {
        deferred.resolve();
      } else {
        $location.path('/login');
      }
      return deferred.promise;
    }
     
  });
