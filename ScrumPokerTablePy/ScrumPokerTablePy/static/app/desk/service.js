(function(){
  angular
    .module("ScrumPokerTable")

    .factory("DeskService", ["$http", "$rootScope", function ($http, $rootScope) {
        var socket = null;
        return {
            join: function (desk_id) {
                if (socket) {
                    socket.disconnect();
                }

                socket = io.connect(location.protocol + "//" + document.domain + ":" + location.port + "/desks/" + desk_id);
                socket.on("connect", function () {
                    console.log("Connected to " + desk_id);
                });
                socket.on("message", function (msg) {
                    console.log(msg);
                    $http.get("api/desk/" + desk_id + "?rnd" + (new Date().getTime()))
                        .then(function (response) {
                            console.log(response.data);
                            $rootScope.$broadcast("desk", response.data);
                        });
                });
            },

            leave: function () {
                if (socket) {
                    socket.disconnect();
                    socket = null;
                }
            },

            get: function(desk_id){
                return $http
                    .get("api/desk/" + desk_id + "?rnd" + (new Date().getTime()))
                    .then(function(response){
                        return response.data;
                    });
            },

            connect: function(desk_id){
                return $http.get("api/desk/" + desk_id).then(function(response){
                    return response.data.desk_id;
                });
            },

            create: function(desk_cards){
                return $http.post("api/desk", {cards: desk_cards}).then(function(response){
                    return response.data.desk_id;
                });
            },

            start: function(desk_id){
                return $http.post("api/desk/start/" + desk_id, {});
            },

            finish: function(desk_id){
                return $http.post("api/desk/finish/" + desk_id, {});
            },

            remove: function(desk_id){
                return $http.delete("api/desk/" + desk_id).then(function(response){
                    return response.data.desk_id;
                });
            },

            get_history: function(desk_id){
                return $http
                    .get("api/desk/history/" + desk_id + "?rnd" + new Date().getTime())
                    .then(function(response){
                        return response.data;
                    });
            }
        };
    }])
  ;
})();