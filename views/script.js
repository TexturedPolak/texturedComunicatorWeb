var username = Cookies.get('username');
var passwordHash = Cookies.get('passwordHash');
var input = document.getElementById("input");
var messages = "";
Cookies.set("id",0);
var havedId=-1
var endedRequest = true
var timeToOffline = 10.0
var tries = 0
//czekanie aż w inpucie pojawi się enter
input.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        //wysylanie danych do pythona
        $.ajax({
            url: "/api",
            type: "PUT",
            data: JSON.stringify({"username": username,"passwordHash":passwordHash,"message":document.querySelector('input').value}),
            contentType: "application/json",
            dataType: "json"
            });
        //resetowanie pola tekstowego
        document.querySelector('input').value="";
    
    };
});
//odświeżanie wiadomości 
var timeout = setInterval(checkNeedToReload, 100);
var timeoutOffline = setInterval(checkIsOnline, 100);
function checkIsOnline () {
    timeToOffline-=0.1;
    if (timeToOffline<=0){
        tries+=1
        if (tries>=3){
            $('#messages').html("Jesteś offline :( <br> Zrestartuj stronę!");
        }
        else{
            endedRequest==true;
        }
    }
};    
function reloadDF () {
    $.ajax({
        url: "/api",
        type: "PATCH",
        data: JSON.stringify({"username": username,"passwordHash":passwordHash,"lastId":Cookies.get('id'),"html":true}),
        contentType: "application/json",
        dataType: "json",
        complete: function(data) {
            var json = data.responseJSON;
            messages+=json.messages;
            $('#messages').html(messages);
            Cookies.set("id",json.lastId);
            var element = document.getElementById("scrool");
            setTimeout(function(){
                element.scrollTop = element.scrollHeight;
                },300);
            endedRequest=true;
            timeToOffline=10.0;
            tries=0;
        }
        });
    
    };
function checkNeedToReload(){
    if (endedRequest==true){
        endedRequest=false;
        $.post(
            "/api",
            {"id": Cookies.get('id')},function(data) {
              Cookies.set("reload",data.reload);
                if (data.reload=="true"){
                    data.reload=false;
                    Cookies.set("reload","false");
                    reloadDF();
                    
                }
                else{
                    endedRequest=true;
                    timeToOffline=10.0;
                    tries=0;
                }
    
        }
        );
    }
};
      //post > server > None albo nowy zestaw
      //post > server > baza danych > uzupelnianie zmiennej js > wyświetlanie