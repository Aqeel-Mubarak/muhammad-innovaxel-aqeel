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


# 2. Retrieve original URL
@app.route('/shorten/<short_code>', methods=['GET'])
def get_original_url(short_code):
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT id, url, short_code, created_at, updated_at FROM urls WHERE short_code = %s", (short_code,))
    url_entry = cur.fetchone()

    if not url_entry:
        return jsonify({"error": "Short URL not found"}), 404
    print(url_entry)
    # Extract fields safely
    url_data = {
        "id": url_entry['id'], 
        "url": url_entry['url'],  
        "shortCode": url_entry['short_code'],  
        "createdAt": url_entry['created_at'].isoformat(),  
        "updatedAt": url_entry['updated_at'].isoformat()   
    }

    # Increment access count
    cur.execute("UPDATE urls SET access_count = access_count + 1 WHERE short_code = %s", (short_code,))
    mysql.connection.commit()
    cur.close()

    return jsonify(url_data), 200

if __name__ == '__main__':
    app.run(debug=True)