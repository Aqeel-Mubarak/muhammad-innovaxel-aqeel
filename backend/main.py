from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL

app = Flask(__name__)
CORS(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_PASSWORD'] = 'CpYPhP27FrP9Dxw'  
app.config['MYSQL_DB'] = 'url_shortener'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

if __name__ == '__main__':
    app.run(debug=True)