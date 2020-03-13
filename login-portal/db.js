const mysql = require('mysql');

const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'psswd',
  database: 'user'
});

module.exports = connection;
