(function(){
  angular
    .module("ScrumPokerTable")
    .controller("PlayerController", ["$scope", "$routeParams", "$location", "$timeout", "DeskService", "PlayerService",
    function($scope, $routeParams, $location, $timeout, deskService, playerService){

        $scope.desk_id = $routeParams.desk_id;
        $scope.player_id = $routeParams.player_id;
        $scope.selected_card = null;

        $scope.send = function(card){
            playerService.send($scope.desk_id, $scope.player_id, card);
        }

        $scope.getCardStyle = function(card){
            if(card !== $scope.selected_card){
                return "";
            }
            return { "background-color": "#8f8" };
        }

        $scope.$on("$destroy", function() {
            deskService.leave();
        });

        deskService.join($scope.desk_id);

        $scope.$on("desk", function (event, desk) {
            console.log(event, desk);
            $scope.desk = desk;
            var player = desk.players.filter(function (p) { return p.name === $scope.player_id.toLowerCase() })[0];
            $scope.selected_card = player.card;
        });

        deskService.get($scope.desk_id).then(function (desk) {
            $scope.desk = desk;
            var player = desk.players.filter(function (p) { return p.name === $scope.player_id.toLowerCase() })[0];
            $scope.selected_card = player.card;
        });

    }])
  ;
})();