from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Fungsi untuk koneksi ke database XAMPP
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",      # Default user XAMPP
        password="",      # Default password XAMPP (kosong)
        database="db_kampus"
    )

@app.route('/')
def biodata():
    try:
        # Ambil data dari database XAMPP
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM mahasiswa LIMIT 1")
        mhs_data = cursor.fetchone()
        cursor.close()
        conn.close()

        # Kirim data ke file index.html
        return render_template('index.html', mhs=mhs_data)
        
    except Exception as e:
        return f"Gagal terhubung ke XAMPP: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)