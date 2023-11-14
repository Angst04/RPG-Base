# server.py

from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def get_data():
   conn = sqlite3.connect('Base/data/collection.sql', check_same_thread=False)
   cursor = conn.cursor()

   cursor.execute("SELECT * FROM collection")
   data = cursor.fetchall()

   conn.close()

   result = [{'id': row[0], 'id_tg': row[1], 'thunder': row[2], 'chain': row[3], 'fury': row[4]} for row in data]

   return result

@app.route('/data')
def data():
   return jsonify(get_data())

if __name__ == '__main__':
   app.run(debug=True)
