
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
        scrollbar-color: #424242 #4b4b4b !important;
      }
      .container{
        margin-right:auto;
        margin-left: auto;
        width:90% ;
        height: 100%;
        background-color: dimgray;
        border-radius: 5px;
        margin-bottom: 2vh;
      }
      #messages{
        background-color: dimgray;
        margin-top: 10px;
        margin-bottom: 10px;
        margin-left: auto;
        margin-right: auto;
        height: 100vh;
        width: 95%;
        text-align: left;
        color:white;
        font-size: 18px;
        word-wrap: break-word;
        border-radius: 5px;
      }
      #input{
        background-color: rgb(66, 66, 66);
        margin-left: auto;
        margin-right: auto;
        align-items: center;
        display: flex;
        justify-content: center;
      }
      input {
        background-color: rgb(66, 66, 66);
        width: 99%;
        margin-left: auto;
        margin-right: auto;
        font-size: 18px;
        border-radius: 5px;
        color: white;
      }
      #scrool{
        overflow: hidden;
        overflow-y: scroll;
        word-wrap: break-word;
        border-radius: 5px;
        height: 90vh;
      }
      ::-webkit-scrollbar-track {
        background: rgb(105 105 105);
        border-radius: 6px;
      }
      ::-webkit-scrollbar-thumb {
        background-color: #4b4b4b;
        border-radius: 6px;
        border: 3px solid #424242;
      }
      ::-webkit-scrollbar-corner {
          background-color: #131516;
          border-radius: 5px;
      }
      ::-webkit-scrollbar{
        background: #424242;
        border-radius: 6px;
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
    </div>
    <div class="container"> 
      <div id="input">
        <input type="text" placeholder="Enter text:">
      </div>
    </div>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/js-cookie@3.0.5/dist/js.cookie.min.js"></script>
    <script src="views/script.js"></script>
  </body>
</html>