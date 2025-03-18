from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
from flask import request, jsonify
import datetime
import random
import string   

# Generate random short code
def generate_unique_short_code():
    while True:
        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        cur = mysql.connection.cursor()
        cur.execute("SELECT short_code FROM urls WHERE short_code = %s", (short_code,))
        existing_code = cur.fetchone()
        cur.close()
        if not existing_code:
            return short_code

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

# 3. Update existing short URL
@app.route('/shorten/<short_code>', methods=['PUT'])
def update_url(short_code):
    data = request.json
    new_url = data.get('url')

    if not new_url:
        return jsonify({"error": "URL is required"}), 400
    if not new_url.startswith(("http://", "https://")):
        return jsonify({"error": "Invalid URL format"}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, url, short_code, created_at FROM urls WHERE short_code = %s", (short_code,))
    url_entry = cur.fetchone()  # Returns tuple or None

    if url_entry is None:
        return jsonify({"error": "Short URL not found"}), 404

    # Extract values correctly from tuple
    url_data = {
        "id": url_entry['id'], 
        "url": url_entry['url'],  
        "shortCode": url_entry['short_code'],  
        "createdAt": url_entry['created_at'].isoformat(),  
    }

    # Update the URL in DB
    updated_at = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute("UPDATE urls SET url = %s, updated_at = %s WHERE short_code = %s", (new_url, updated_at, url_data['shortCode']))    
    mysql.connection.commit()
    print(f"Rows affected: {cur.rowcount}")
    cur.close()

    return jsonify({
        "id": url_data['id'],
        "url": new_url,
        "shortCode": url_data['shortCode'],
        "createdAt": url_data['createdAt'],
        "updatedAt": updated_at
    }), 200

# 4. Delete a short URL
@app.route('/shorten/<short_code>', methods=['DELETE'])
def delete_url(short_code):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM urls WHERE short_code = %s", (short_code,))
    url_entry = cur.fetchone()

    if not url_entry:
        return jsonify({"error": "Short URL not found"}), 404

    cur.execute("DELETE FROM urls WHERE short_code = %s", (short_code,))
    mysql.connection.commit()
    cur.close()

    return '', 204

# 5. Get URL Statistics
@app.route('/shorten/<short_code>/stats', methods=['GET'])
def get_url_stats(short_code):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM urls WHERE short_code = %s", (short_code,))
    url_entry = cur.fetchone()

    if not url_entry:
        return jsonify({"error": "Short URL not found"}), 404

    return jsonify({
        "id": url_entry['id'],
        "url": url_entry['url'],
        "shortCode": url_entry['short_code'],
        "createdAt": url_entry['created_at'].isoformat(),
        "updatedAt": url_entry['updated_at'].isoformat(),
        "accessCount": url_entry['access_count']
    }), 200

@app.route('/shorten/all', methods=['GET'])
def get_all_short_urls():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, url, short_code, created_at, updated_at, access_count FROM urls")
    urls = cur.fetchall()
    cur.close()

    if not urls:
        return jsonify({"message": "No shortened URLs found"}), 404

    url_list = [
        {
            "id": url['id'],
            "url": url['url'],
            "shortCode": url['short_code'],
            "createdAt": url['created_at'].isoformat(),
            "updatedAt": url['updated_at'].isoformat(),
            "accessCount": url['access_count']
        }
        for url in urls
    ]

    return jsonify(url_list), 200

if __name__ == '__main__':
    app.run(debug=True)