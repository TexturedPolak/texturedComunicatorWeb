
<!DOCTYPE html>
<html lang="pl">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Textured Comunicator</title>
    <style>
      body{
        background-color: rgb(66, 66, 66);
      }
      .container{
        margin-right:auto;
        margin-left: auto;
        width:90% ;
        height: 100%;
        background-color: dimgray;
      }
      #messages{
        margin-top: 10px;
        margin-bottom: 10px;
        margin-left: auto;
        margin-right: auto;
        height: 600px;
        width: 95%;
        text-align: left;
        color:white;
        font-size: 18px;
        word-wrap: break-word;
      }
      #input{
        background-color: darkgray;
      }
      input {
        width: 100%;
        font-size: 18px;
      }
      #scrool{
        overflow: hidden;
        overflow-y: scroll;
        word-wrap: break-word;
      }
    </style>
  </head>
  <body>
    
    <div class="container"> 
      <div id="scrool">
        <div id="messages">
        Włącz javascript :)
        </div>
      </div>
      <div id="input">
        <input type="text" placeholder="Enter text:">
      </div>

    </div>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/js-cookie@3.0.5/dist/js.cookie.min.js"></script>
    <script>
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
    
    
    
    </script>
  </body>
</html>