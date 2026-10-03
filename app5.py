# ==========================================================
# PRAKTIKUM PEMROGRAMAN KOMPUTER
# PERTEMUAN 6
# TOPIK :
# IMPLEMENTASI CRUD + IMPORT & EXPORT EXCEL
# ==========================================================

# ==========================================================
# IMPORT LIBRARY
# ==========================================================

from flask import Flask, render_template, request, redirect, send_file
import mysql.connector
import openpyxl
from openpyxl import Workbook
import os

# ==========================================================
# MEMBUAT OBJECT FLASK
# ==========================================================

app = Flask(__name__)

# ==========================================================
# KONEKSI DATABASE
# ==========================================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dataset"
)

# ==========================================================
# HALAMAN UTAMA
# MENAMPILKAN SELURUH DATA MAHASASISWA
# ==========================================================

@app.route("/")
def home():

    cursor = conn.cursor()

    sql = "SELECT * FROM pesanan"

    cursor.execute(sql)

    data = cursor.fetchall()

    return render_template(
        "index5.html",
        data=data
    )

# ==========================================================
# SIMPAN DATA
# ==========================================================

@app.route("/simpan", methods=["POST"])
def simpan():

    Resi = request.form["Resi"]
    Customer = request.form["Customer"]
    Pesanan = request.form["Pesanan"]
    Tanggal = request.form["Tanggal"]
    Keterangan = request.form["Keterangan"]

    cursor = conn.cursor()

    sql = """
    INSERT INTO pesanan
    (
        Resi,
        Customer,
        Pesanan,
        Tanggal,
        Keterangan
    )
    VALUES
    (
        %s,
        %s,
        %s,
        %s,
        %s
    )
    """

    value = (
        Resi,
        Customer,
        Pesanan,
        Tanggal,
        Keterangan
    )

    cursor.execute(sql, value)

    conn.commit()

    return redirect("/")
# ==========================================================
# EDIT DATA
# MENAMPILKAN DATA YANG AKAN DIEDIT
# ==========================================================

@app.route("/edit/<Resi>")
def edit(Resi):

    cursor = conn.cursor()

    sql = "SELECT * FROM pesanan WHERE Resi = %s"

    cursor.execute(sql, (Resi,))

    Data = cursor.fetchone()

    return render_template(
        "edit.html",
        Data=Data
    )


# ==========================================================
# UPDATE DATA
# MENYIMPAN HASIL EDIT
# ==========================================================

@app.route("/update", methods=["POST"])
def update():

    Resi = request.form["Resi"]
    Customer = request.form["Customer"]
    Pesanan = request.form["Pesanan"]
    Tanggal = request.form["Tanggal"]
    Keterangan = request.form["Keterangan"]

    cursor = conn.cursor()

    sql = """
    UPDATE pesanan
    SET
        Customer = %s,
        Pesanan = %s,
        Tanggal = %s,
        Keterangan = %s
    WHERE
        Resi = %s
    """

    value = (
        Customer,
        Pesanan,
        Tanggal,
        Keterangan,
        Resi
    )

    cursor.execute(sql, value)

    conn.commit()

    return redirect("/")


# ==========================================================
# HAPUS DATA
# ==========================================================

@app.route("/hapus/<Resi>")
def hapus(Resi):

    cursor = conn.cursor()

    sql = "DELETE FROM pesanan WHERE Resi = %s"

    cursor.execute(sql, (Resi,))

    conn.commit()

    return redirect("/")


# ==========================================================
# BATAL
# ==========================================================

@app.route("/batal")
def batal():

    return redirect("/")
# ==========================================================
# MENJALANKAN APLIKASI
# ==========================================================

if __name__ == "__main__":

    app.run(debug=True)
