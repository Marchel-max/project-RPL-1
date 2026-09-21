from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import datetime
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("MYSQL_PASSWORD", ""),
        database="autoservis"
    )

# -------------------------------
# ROUTE INVENTARIS (STOK BARANG)
# -------------------------------

@app.route('/')
def home():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM inventory")
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', items=items)
    except Exception as e:
        return f"Error Koneksi Database: {e}"

@app.route('/add', methods=['POST'])
def add_item():
    kode_barang = request.form['kode_barang']
    nama_barang = request.form['nama_barang']
    stok = request.form['stok']
    stok_minimal = request.form['stok_minimal']
    harga_beli = request.form['harga_beli']
    harga_jual = request.form['harga_jual']

    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO inventory (kode_barang, nama_barang, stok, stok_minimal, harga_beli, harga_jual)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (kode_barang, nama_barang, stok, stok_minimal, harga_beli, harga_jual))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('home'))

@app.route('/edit/<int:id>', methods=['POST'])
def edit_item(id):
    kode_barang = request.form['kode_barang']
    nama_barang = request.form['nama_barang']
    stok = request.form['stok']
    stok_minimal = request.form['stok_minimal']
    harga_beli = request.form['harga_beli']
    harga_jual = request.form['harga_jual']

    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        UPDATE inventory 
        SET kode_barang=%s, nama_barang=%s, stok=%s, stok_minimal=%s, harga_beli=%s, harga_jual=%s
        WHERE id=%s
    """
    cursor.execute(query, (kode_barang, nama_barang, stok, stok_minimal, harga_beli, harga_jual, id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('home'))

@app.route('/delete/<int:id>')
def delete_item(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('home'))

# -------------------------------
# ROUTE KASIR / TRANSAKSI (POS)
# -------------------------------

@app.route('/kasir')
def kasir():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # Ambil hanya barang yang stoknya masih ada (> 0)
    cursor.execute("SELECT * FROM inventory WHERE stok > 0")
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('kasir.html', items=items)

@app.route('/proses_transaksi', methods=['POST'])
def proses_transaksi():
    nama_pelanggan = request.form.get('nama_pelanggan', 'Pelanggan Umum')
    inventory_ids = request.form.getlist('inventory_id[]')
    jumlah_list = request.form.getlist('jumlah[]')
    harga_list = request.form.getlist('harga_satuan[]')

    if not inventory_ids:
        return redirect(url_for('kasir'))

    # Buat Nomor Nota Otomatis (Contoh: INV-20260918111500)
    no_nota = f"INV-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Hitung total belanjaan
    total_harga = sum(int(qty) * int(hrg) for qty, hrg in zip(jumlah_list, harga_list))

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Simpan Header Transaksi
    query_header = "INSERT INTO transactions (no_nota, nama_pelanggan, total_harga) VALUES (%s, %s, %s)"
    cursor.execute(query_header, (no_nota, nama_pelanggan, total_harga))
    transaction_id = cursor.lastrowid

    # 2. Simpan Detail Transaksi & Potong Stok Barang di Database
    for inv_id, qty, hrg in zip(inventory_ids, jumlah_list, harga_list):
        subtotal = int(qty) * int(hrg)
        
        query_detail = """
            INSERT INTO transaction_details (transaction_id, inventory_id, jumlah, harga_satuan, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query_detail, (transaction_id, inv_id, qty, hrg, subtotal))

        # Pengurangan Stok
        query_stok = "UPDATE inventory SET stok = stok - %s WHERE id = %s"
        cursor.execute(query_stok, (qty, inv_id))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)