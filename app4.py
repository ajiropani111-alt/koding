from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask (__name__) 
# koneksi ke database mysql
conn = mysql.connector.connect (host="localhost",user="root",password="",database="db_penjualan")
@app.route("/")
def home():
    cursor = conn.cursor()
    sql = "SELECT no_resi, nama_pembeli, jenis_pisang, jumlah_sisir,harga from cavendish"
    cursor.execute(sql)
    data = cursor.fetchall()

    return render_template("index4.html", data=data)

@app.route("/simpan", methods=["POST"])
def simpan():
    no_resi = request.form["no_resi"]
    nama_pembeli = request.form["nama_pembeli"]
    jenis_pisang = request.form["jenis_pisang"]
    jumlah_sisir = request.form["jumlah_sisir"]
    harga = request.form["harga"]

    cursor = conn.cursor()

    sql = """
    INSERT INTO cavendish (no_resi, nama_pembeli, jenis_pisang, jumlah_sisir, harga)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (no_resi, nama_pembeli, jenis_pisang, jumlah_sisir, harga)

    cursor.execute(sql, values)
    conn.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)