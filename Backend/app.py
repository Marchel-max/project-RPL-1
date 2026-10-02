from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

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

@app.route('/tambah_inventory', methods=['POST'])
def tambah_inventory():
    kode_barang = request.form.get('kode_barang')
    nama_barang = request.form.get('nama_barang')
    tipe = request.form.get('tipe', 'sparepart')
    harga_jual = float(request.form.get('harga_jual', 0))
    harga_beli = float(request.form.get('harga_beli', 0))
    stok = int(request.form.get('stok', 0))

    # Jika tipenya 'jasa', stok di-set default tinggi (misal: 9999) & harga beli = 0
    if tipe == 'jasa':
        stok = 9999
        harga_beli = 0

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO inventory (kode_barang, nama_barang, tipe, stok, harga_beli, harga_jual)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (kode_barang, nama_barang, tipe, stok, harga_beli, harga_jual))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect('/')

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

from datetime import datetime

@app.route('/proses_transaksi', methods=['POST'])
def proses_transaksi():
    # 1. Ambil nama pelanggan
    nama_pelanggan = request.form.get('nama_pelanggan', 'Umum')
    
    # 2. Ambil array data dari hidden inputs kasir.html
    inventory_ids = request.form.getlist('inventory_id[]')
    jumlah_list = request.form.getlist('jumlah[]')
    harga_list = request.form.getlist('harga_satuan[]')

    # Generate nomor nota otomatis
    no_nota_otomatis = "INV-" + datetime.now().strftime("%Y%m%d%H%M%S")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # 3. Simpan transaksi utama
    cursor.execute("""
        INSERT INTO transactions (no_nota, nama_pelanggan, total_harga) 
        VALUES (%s, %s, %s)
    """, (no_nota_otomatis, nama_pelanggan, 0))
    transaction_id = cursor.lastrowid
    
    total_bayar = 0
    
    # 4. Loop setiap item yang dibeli
    for i in range(len(inventory_ids)):
        inv_id = inventory_ids[i]
        jumlah_beli = int(jumlah_list[i]) if i < len(jumlah_list) else 1
        harga_satuan = float(harga_list[i]) if i < len(harga_list) else 0
        
        # Hitung subtotal per item
        subtotal = jumlah_beli * harga_satuan
        total_bayar += subtotal
        
        # Cek tipe item (sparepart vs jasa)
        cursor.execute("SELECT tipe FROM inventory WHERE id = %s", (inv_id,))
        barang = cursor.fetchone()
        
        # 🔥 KUNCI PERUBAHAN: Masukkan kolom 'subtotal' ke query INSERT
        cursor.execute("""
            INSERT INTO transaction_details (transaction_id, inventory_id, jumlah, harga_satuan, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """, (transaction_id, inv_id, jumlah_beli, harga_satuan, subtotal))
        
        # Hanya potong stok jika tipenya 'sparepart'
        if barang and barang.get('tipe') == 'sparepart':
            cursor.execute("""
                UPDATE inventory 
                SET stok = stok - %s 
                WHERE id = %s
            """, (jumlah_beli, inv_id))
            
    # 5. Update total harga transaksi akhir
    cursor.execute("""
        UPDATE transactions SET total_harga = %s WHERE id = %s
    """, (total_bayar, transaction_id))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    # Redirect langsung ke halaman Laporan Penjualan
    return redirect('/laporan')

import json

@app.route('/laporan')
def laporan():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # 1. Ringkasan Omzet & Total Transaksi
    cursor.execute("""
        SELECT 
            COUNT(id) AS total_transaksi,
            IFNULL(SUM(COALESCE(total_harga, total_bayar, 0)), 0) AS total_omzet
        FROM transactions
    """)
    summary = cursor.fetchone()
    
    # 2. Ambil data transaksi
    cursor.execute("""
        SELECT 
            t.id,
            t.no_nota,
            t.nama_pelanggan,
            COALESCE(t.total_harga, t.total_bayar, 0) AS total_harga,
            t.tanggal_transaksi,
            JSON_ARRAYAGG(
                JSON_OBJECT(
                    'nama_barang', COALESCE(i.nama_barang, 'Barang Dihapus'),
                    'jumlah', td.jumlah,
                    'harga_satuan', td.harga_satuan,
                    'subtotal', (td.jumlah * td.harga_satuan)
                )
            ) AS items_json
        FROM transactions t
        LEFT JOIN transaction_details td ON t.id = td.transaction_id
        LEFT JOIN inventory i ON td.inventory_id = i.id
        GROUP BY t.id
        ORDER BY t.id DESC
    """)
    transaksi_raw = cursor.fetchall()
    
    # Kunci perbaikan: Gunakan nama 'detail_items' agar tidak bentrok dengan method dictionary .items()
    transaksi_list = []
    for row in transaksi_raw:
        raw_json = row.get('items_json')
        
        if isinstance(raw_json, str):
            try:
                row['detail_items'] = json.loads(raw_json)
            except:
                row['detail_items'] = []
        elif isinstance(raw_json, list):
            row['detail_items'] = raw_json
        else:
            row['detail_items'] = []
            
        transaksi_list.append(row)

    cursor.close()
    conn.close()
    
    return render_template('laporan.html', summary=summary, transaksi=transaksi_list)
if __name__ == '__main__':
    app.run(debug=True)