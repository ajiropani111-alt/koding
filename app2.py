from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Koneksi ke Database XAMPP
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_kampus"
)

@app.route("/")
def data_mahasiswa():
    cursor = conn.cursor()
    sql = "SELECT * FROM mahasiswa"
    cursor.execute(sql)
    data = cursor.fetchall()  # Mengambil SEMUA data mahasiswa
    
    return render_template("index2.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)