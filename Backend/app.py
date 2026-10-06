import json
import datetime
from datetime import datetime
from pathlib import Path
from flask import Flask, flash, redirect, render_template, request, session, url_for
import mysql.connector

# Wajib tambahkan baris ini untuk enkripsi password:
from werkzeug.security import generate_password_hash, check_password_hash

# Konfigurasi Path Folder Frontend
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "Frontend"

app = Flask(__name__, template_folder=str(FRONTEND_DIR), static_folder=str(FRONTEND_DIR))
app.secret_key = "autoservis-saas-secret-key-123"

# Konfigurasi Koneksi Database MySQL
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Marchel123?",  # Sesuaikan jika MySQL kamu ada passwordnya
    "database": "autoservis"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Helper Pengecekan Limit Freemium
def check_free_limit(user_id, feature_type):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT plan_type FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    
    if not user or user.get('plan_type') == 'pro':
        cursor.close()
        conn.close()
        return True, "Akses Pro"
        
    if feature_type == 'add_item':
        cursor.execute("SELECT COUNT(*) AS total FROM inventory WHERE user_id = %s", (user_id,))
        if cursor.fetchone()['total'] >= 100:
            cursor.close()
            conn.close()
            return False, "Batas maksimal 100 jenis barang untuk akun Gratis telah tercapai!"
            
    elif feature_type == 'checkout':
        cursor.execute("""
            SELECT COUNT(*) AS total FROM transactions 
            WHERE user_id = %s AND DATE(created_at) = CURRENT_DATE()
        """, (user_id,))
        if cursor.fetchone()['total'] >= 50:
            cursor.close()
            conn.close()
            return False, "Batas maksimal 50 transaksi harian untuk akun Gratis telah tercapai!"
            
    cursor.close()
    conn.close()
    return True, "OK"

# -------------------------------
# ROUTE AUTH & NAVIGASI
# -------------------------------

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["nama_toko"] = user["nama_toko"]
            session["plan_type"] = user["plan_type"]
            return redirect(url_for("dashboard"))

        flash("Email atau password salah. Silakan coba lagi.")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nama_toko = request.form.get("nama_toko")
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        hashed_pw = generate_password_hash(password)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (nama_toko, email, password_hash) VALUES (%s, %s, %s)",
                (nama_toko, email, hashed_pw)
            )
            conn.commit()
            cursor.close()
            conn.close()

            flash("Pendaftaran berhasil! Silakan login.")
            return redirect(url_for("login"))
        except mysql.connector.Error:
            flash("Email sudah terdaftar atau terjadi kesalahan.")

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# -------------------------------
# ROUTE INVENTARIS / DASHBOARD
# -------------------------------

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user_id = session["user_id"]
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM inventory WHERE user_id = %s ORDER BY id DESC", (user_id,))
    items = cursor.fetchall()

    cursor.execute("""
        SELECT 
            COUNT(*) as total_item,
            SUM(CASE WHEN tipe = 'barang' THEN 1 ELSE 0 END) as total_barang,
            SUM(CASE WHEN tipe = 'layanan' THEN 1 ELSE 0 END) as total_layanan,
            SUM(CASE WHEN tipe = 'barang' AND stok <= stok_minimal THEN 1 ELSE 0 END) as stok_kritis
        FROM inventory WHERE user_id = %s
    """, (user_id,))
    summary = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("index.html", items=items, summary=summary)

@app.route("/tambah_inventory", methods=["POST"])
def tambah_inventory():
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    user_id = session["user_id"]
    
    is_allowed, msg = check_free_limit(user_id, 'add_item')
    if not is_allowed:
        flash(msg)
        return redirect(url_for("dashboard"))

    kode_barang = request.form.get("kode_barang")
    nama_barang = request.form.get("nama_barang")
    tipe = request.form.get("tipe", "barang")
    harga_jual = float(request.form.get("harga_jual", 0))
    harga_beli = float(request.form.get("harga_beli", 0))
    stok = int(request.form.get("stok", 0))

    if tipe == "layanan":
        stok = 9999
        harga_beli = 0

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO inventory (user_id, kode_barang, nama_barang, tipe, stok, harga_beli, harga_jual)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (user_id, kode_barang, nama_barang, tipe, stok, harga_beli, harga_jual))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for("dashboard"))

@app.route("/edit/<int:id>", methods=["POST"])
def edit_item(id):
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    user_id = session["user_id"]
    kode_barang = request.form["kode_barang"]
    nama_barang = request.form["nama_barang"]
    stok = request.form["stok"]
    stok_minimal = request.form["stok_minimal"]
    harga_beli = request.form["harga_beli"]
    harga_jual = request.form["harga_jual"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE inventory 
        SET kode_barang=%s, nama_barang=%s, stok=%s, stok_minimal=%s, harga_beli=%s, harga_jual=%s
        WHERE id=%s AND user_id=%s
    """, (kode_barang, nama_barang, stok, stok_minimal, harga_beli, harga_jual, id, user_id))
    
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("dashboard"))

@app.route("/delete/<int:id>")
def delete_item(id):
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    user_id = session["user_id"]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE id = %s AND user_id = %s", (id, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("dashboard"))

# -------------------------------
# ROUTE POS KASIR & TRANSAKSI
# -------------------------------

@app.route("/kasir")
def kasir():
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    user_id = session["user_id"]
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventory WHERE user_id = %s AND stok > 0", (user_id,))
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("kasir.html", items=items)

@app.route("/proses_transaksi", methods=["POST"])
def proses_transaksi():
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    user_id = session["user_id"]
    
    is_allowed, msg = check_free_limit(user_id, 'checkout')
    if not is_allowed:
        flash(msg)
        return redirect(url_for("kasir"))

    nama_pelanggan = request.form.get("nama_pelanggan", "Umum")
    inventory_ids = request.form.getlist("inventory_id[]")
    jumlah_list = request.form.getlist("jumlah[]")
    harga_list = request.form.getlist("harga_satuan[]")

    no_nota_otomatis = "INV-" + datetime.now().strftime("%Y%m%d%H%M%S")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        INSERT INTO transactions (user_id, no_nota, nama_pelanggan, total_harga) 
        VALUES (%s, %s, %s, %s)
    """, (user_id, no_nota_otomatis, nama_pelanggan, 0))
    transaction_id = cursor.lastrowid
    
    total_bayar = 0
    for i in range(len(inventory_ids)):
        inv_id = inventory_ids[i]
        jumlah_beli = int(jumlah_list[i]) if i < len(jumlah_list) else 1
        harga_satuan = float(harga_list[i]) if i < len(harga_list) else 0
        
        subtotal = jumlah_beli * harga_satuan
        total_bayar += subtotal
        
        cursor.execute("SELECT tipe FROM inventory WHERE id = %s AND user_id = %s", (inv_id, user_id))
        barang = cursor.fetchone()
        
        cursor.execute("""
            INSERT INTO transaction_details (transaction_id, inventory_id, jumlah, harga_satuan, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """, (transaction_id, inv_id, jumlah_beli, harga_satuan, subtotal))
        
        if barang and barang.get('tipe') == 'barang':
            cursor.execute("""
                UPDATE inventory SET stok = stok - %s WHERE id = %s AND user_id = %s
            """, (jumlah_beli, inv_id, user_id))
            
    cursor.execute("UPDATE transactions SET total_harga = %s WHERE id = %s AND user_id = %s", (total_bayar, transaction_id, user_id))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for("laporan"))

@app.route("/laporan")
def laporan():
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    user_id = session["user_id"]
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT COUNT(id) AS total_transaksi, IFNULL(SUM(total_harga), 0) AS total_omzet
        FROM transactions WHERE user_id = %s
    """, (user_id,))
    summary = cursor.fetchone()
    
    cursor.execute("""
        SELECT t.id, t.no_nota, t.nama_pelanggan, t.total_harga, t.created_at AS tanggal_transaksi,
            JSON_ARRAYAGG(
                JSON_OBJECT(
                    'nama_barang', COALESCE(i.nama_barang, 'Barang Dihapus'),
                    'jumlah', td.jumlah, 'harga_satuan', td.harga_satuan, 'subtotal', td.subtotal
                )
            ) AS items_json
        FROM transactions t
        LEFT JOIN transaction_details td ON t.id = td.transaction_id
        LEFT JOIN inventory i ON td.inventory_id = i.id
        WHERE t.user_id = %s GROUP BY t.id ORDER BY t.id DESC
    """, (user_id,))
    transaksi_raw = cursor.fetchall()
    
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
    return render_template("laporan.html", summary=summary, transaksi=transaksi_list)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)