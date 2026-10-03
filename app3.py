from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Koneksi Database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="data_nilai"
)

@app.route("/")
def home():
    cursor = conn.cursor()
    sql = "SELECT * FROM data_nilai"
    cursor.execute(sql)
    data = cursor.fetchall()

    return render_template(
        "index3.html",
        data=data
    )

if __name__ == "__main__":
    app.run(debug=True)