from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
from flask import request, jsonify
import datetime
import random
import string   

# Generate random short code
def generate_unique_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

        

app = Flask(__name__)
CORS(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_PASSWORD'] = 'CpYPhP27FrP9Dxw'  
app.config['MYSQL_DB'] = 'url_shortener'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/shorten', methods=['POST'])
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.json
    long_url = data.get('url')

    if not long_url:
        return jsonify({"error": "URL is required"}), 400
    if not long_url.startswith(("http://", "https://")):
        return jsonify({"error": "Invalid URL format"}), 400


    short_code = generate_unique_short_code()

    created_at = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    updated_at = created_at  

    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO urls (url, short_code, created_at, updated_at) VALUES (%s, %s, %s, %s)",
                    (long_url, short_code, created_at, updated_at))
        mysql.connection.commit()
        inserted_id = cur.lastrowid  # Get inserted row ID
        cur.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error if DB operation fails

    return jsonify({
        "id": inserted_id,
        "url": long_url,
        "shortCode": short_code,
        "createdAt": created_at,
        "updatedAt": updated_at
    }), 201

if __name__ == '__main__':
    app.run(debug=True)