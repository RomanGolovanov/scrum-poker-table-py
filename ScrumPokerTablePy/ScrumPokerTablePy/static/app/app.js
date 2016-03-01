
(function(){
  angular
    .module("ScrumPokerTable", ["ngRoute","ngAnimate","ngAria","ngResource", "ngCookies","ui.bootstrap","monospaced.qrcode", "angular-clipboard"])
    
    .config(["$routeProvider", function($routeProvider){

      $routeProvider
        .when("/desk", { templateUrl: "app/desk/new/template.html", controller: "NewDeskController", reloadOnSearch:false })
        .when("/desk/:desk_id", { templateUrl: "app/desk/play/template.html", controller: "PlayDeskController", reloadOnSearch:false })
        .when("/desk/history/:desk_id", { templateUrl: "app/desk/history/template.html", controller: "PlayDeskHistoryController", reloadOnSearch:false })

        .when("/player/", { templateUrl: "app/player/connect/template.html", controller: "ConnectPlayerController", reloadOnSearch:false })
        .when("/player/:desk_id", { templateUrl: "app/player/connect/template.html", controller: "ConnectPlayerController", reloadOnSearch:false })
        .when("/player/:desk_id/:player_id", { templateUrl: "app/player/play/template.html", controller: "PlayerController", reloadOnSearch:false })

        .when("/master/", { templateUrl: "app/master/connect/template.html", controller: "ConnectMasterController", reloadOnSearch:false })
        .when("/master/:desk_id", { templateUrl: "app/master/play/template.html", controller: "MasterController", reloadOnSearch:false })

        .when("/about", { templateUrl: "app/about/about.html"})
        .otherwise("/desk");
    }])

    .controller("HeaderController", ["$scope", "$location", function($scope, $location){
      $scope.isActive = function (viewLocation) {
          return $location.path().startsWith(viewLocation);
      };
    }])
  ;
})();