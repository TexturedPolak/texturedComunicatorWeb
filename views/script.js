var username = Cookies.get('username');
var passwordHash = Cookies.get('passwordHash');
var input = document.getElementById("input");
//czekanie aż w inpucie pojawi się enter
input.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        //wysylanie danych do pythona
        $.ajax({
            url: "/api",
            type: "POST",
            data: JSON.stringify({"username": username,"passwordHash":passwordHash,"message":document.querySelector('input').value}),
            contentType: "application/json",
            dataType: "json"
            });
        //resetowanie pola tekstowego
        document.querySelector('input').value="";
    
    };
});
//odświeżanie wiadomości 
$('#messages').load('/messages?username='+Cookies.get("username")+'&passwordHash='+Cookies.get("passwordHash"));
var timeout = setInterval(checkNeedToReload, 500);    
function reloadDF () {
    $('#messages').load('/messages?username='+Cookies.get("username")+'&passwordHash='+Cookies.get("passwordHash"));
    var element = document.getElementById("scrool");
    setTimeout(function(){
        element.scrollTop = element.scrollHeight;
    },300)
};
function checkNeedToReload(){
    $.post(
        "/api/messages",
        {"LocalVersion": Cookies.get('LocalVersion')},function(data) {
            Cookies.set("reload",data.reload);
            Cookies.set("LocalVersion",data.LocalVersion);
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