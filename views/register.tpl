<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Rejestracja</title>
<style>
  body {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    background-color: #3498db; /* Kolor tła niebieski */
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
  }
  .container {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
    width: 300px;
  }
  .container h2 {
    text-align: center;
    margin-bottom: 20px;
  }
  .input-group {
    margin-bottom: 15px;
    margin-left: auto;
    margin-right: auto;
  }
  .input-group label {
    display: block;
    margin-bottom: 5px;
    margin-left: auto;
    margin-right: auto;
  }
  .input-group input {
    width: 90%;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
    margin-left: auto;
    margin-right: auto;
  }
  .input-group button {
    width: 100%;
    padding: 10px;
    border: none;
    background-color: #3498db;
    color: #fff;
    font-weight: bold;
    border-radius: 5px;
    cursor: pointer;
    margin-left: auto;
    margin-right: auto;
  }
</style>
</head>
<body>
<div class="container">
  <h2>Rejestracja</h2><br>
  Rejestrując się zdajesz sobie sprawę i akceptujesz wykorzystywanie plików cookies na tej witrynie.<br>
  <span style="color: red">{{error}}</span>
  <form method="post">
    <div class="input-group">
      <label for="username">Nazwa użytkownika</label>
      <input type="text" name="username" required>
    </div>
    <div class="input-group">
      <label for="password">Hasło</label>
      <input type="password" name="password" required>
    </div>
    <div class="input-group">
      <label for="confirm_password">Powtórz hasło</label>
      <input type="password" name="confirm_password" required>
    </div>
    <div class="input-group">
      <button type="submit">Zarejestruj się</button>
    </div>
  </form>
</div>
</body>
</html>