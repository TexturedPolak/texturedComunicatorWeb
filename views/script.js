var username = Cookies.get('username');
var passwordHash = Cookies.get('passwordHash');
var input = document.getElementById("input");
var messages = "";
Cookies.set("id",0);
var havedId=-1
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
reloadDF();
var timeout = setInterval(checkNeedToReload, 1000);    
function reloadDF () {
    $.ajax({
        url: "/api",
        type: "PATCH",
        data: JSON.stringify({"username": username,"passwordHash":passwordHash,"lastId":Cookies.get('id')}),
        contentType: "application/json",
        dataType: "json",
        complete: function(data) {
            var json = data.responseJSON;
            messages+=json.messages;
            $('#messages').html(messages);
            var element = document.getElementById("scrool");
            setTimeout(function(){
                element.scrollTop = element.scrollHeight;
                },300)
        }
        });
    
    };
function checkNeedToReload(){
    $.post(
        "/api",
        {"id": Cookies.get('id')},function(data) {
            Cookies.set("reload",data.reload);
            Cookies.set("id",data.id);
            if (data.reload=="true"){
                data.reload=false;
                Cookies.set("reload","false");
                reloadDF();
            }
        }
    );
};
      //post > server > None albo nowy zestaw
      //post > server > baza danych > uzupelnianie zmiennej js > wyświetlanie