(function(){

  angular
    .module("ScrumPokerTable")
    .controller("PlayDeskController", ["$scope", "$routeParams", "$location", "$timeout", "DeskService",
    function($scope, $routeParams, $location, $timeout, deskService){

        $scope.desk_id = $routeParams.desk_id;
        $scope.desk_url = $location.absUrl();

        $scope.removeGame = function(){
            deskService.remove($scope.desk_id);
            $location.path("/desk?stopped");
        }

        $scope.connectAsPlayer = function(){
            $location.path("/player/" + $scope.desk_id );
        }

        $scope.connectAsMaster = function(){
            $location.path("/master/" + $scope.desk_id );
        }

        $scope.showHistory = function(){
            $location.path("/desk/history/" + $scope.desk_id );
        }

        var disposed = false;
        $scope.$on("$destroy", function () { disposed = true; });

        function updateDeskAsync() {
            var defaultTimeout = 1000;
            var timeout = $scope.desk ? 10 : null;
            var modified = $scope.desk ? $scope.desk.modified : null;
            deskService.get($scope.desk_id, modified, timeout).then(function(desk){
                $scope.desk = desk;
                if (!disposed) $timeout(updateDeskAsync, defaultTimeout);

            }, function(response){
                if(response.status === 304){
                    if (!disposed) $timeout(updateDeskAsync, defaultTimeout);
                }else{
                    if (!disposed) $timeout(updateDeskAsync, defaultTimeout);
                }
            });
        }
        updateDeskAsync();
    }])
  ;
})();