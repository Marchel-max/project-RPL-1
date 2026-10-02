# AutoServis - SaaS Manajemen Stok & Kasir UMKM (Freemium POS)

**AutoServis** adalah platform digital berbasis B2B SaaS (*Software-as-a-Service*) yang dirancang untuk membantu pemilik UMKM (toko kelontong, minimarket, toko baju, bengkel, hingga penyedia jasa) mendigitalisasi operasional harian. 

Aplikasi ini menggunakan model bisnis **Freemium** untuk mengelola inventaris produk fisik dan layanan, memproses transaksi kasir (Point of Sale / POS), menghasilkan nota otomatis, serta menyajikan laporan omzet secara *real-time*.

---

## 🎯 Model Bisnis Freemium & Monetisasi

Aplikasi ini dirancang dengan sistem berlangganan (*Subscription Model*) berbasis multi-tenant dengan perbedaan fitur yang jelas antara Paket Gratis dan Paket Pro:

1. **Paket Free (Gratis Seumur Hidup):**
   - Ideal untuk usaha mikro/baru merintis.
   - Maksimal **100 jenis item inventaris**.
   - Batas transaksi maksimal **50 transaksi / hari** (reset otomatis setiap hari).
   - Cetak nota/struk belanja **disertai watermark** (misal: *"Printed with AutoServis Free"*).

2. **Paket Pro (Berlangganan Bulanan / Tahunan):**
   - Ideal untuk bisnis yang sedang berkembang pesat.
   - **Unlimited** jenis item inventaris (tanpa batas).
   - **Unlimited** transaksi harian (tanpa batas harian/bulanan).
   - Cetak nota/struk belanja **tanpa watermark** (bebas kustomisasi nama & logo toko sendiri).
   - Akses penuh ke laporan penjualan lanjutan dan ekspor data.

---

## ✨ Fitur Utama

- **Authentication & Multi-Tenant:** Isolasi data aman antar toko berbasis `user_id` dan manajemen sesi login/register.
- **Manajemen Produk & Layanan (Unified Inventory):** Pembedaan otomatis antara barang fisik (potong stok) dan layanan/jasa (non-stok).
- **POS / Kasir Interaktif:** Keranjang belanja cepat, pencarian barang, dan checkout dengan otomatisasi pemotongan stok.
- **Generasi Nota Otomatis & Dynamic Watermark:** Pembuatan nomor transaksi unik berformat `INV-YYYYMMDDHHMMSS` dengan rendering watermark otomatis khusus akun Free.
- **Laporan Omzet & Ringkasan Penjualan:** Dashboard riwayat transaksi beserta detail nota belanja.
- **Freemium Feature Gate:** Validasi otomatis batas limit penggunaan item, transaksi harian, dan fitur cetak nota.

---

## 🛠️ Tech Stack

- **Frontend:** HTML5, Tailwind CSS (via CDN), Vanilla JavaScript, Jinja2 Template Engine
- **Backend:** Python 3.x, Flask Framework
- **Database:** MySQL / MariaDB
- **Database Driver:** `mysql-connector-python`
- **Security:** `Werkzeug.security` (Password Hashing), Flask Session Management
- **Environment Management:** `python-dotenv`

---

## 🗄️ Database Schema (Multi-Tenant)

Aplikasi ini menggunakan 4 tabel utama di MySQL (`autoservis_db`):

1. **`users`** (Data Toko & Langganan SaaS)
   - `id` (INT, Primary Key, Auto Increment)
   - `nama_toko` (VARCHAR(100))
   - `email` (VARCHAR(100), Unique)
   - `password_hash` (VARCHAR(255))
   - `plan_type` (ENUM('free', 'pro'), Default: 'free')
   - `expired_date` (DATE, Nullable)
   - `created_at` (TIMESTAMP, Default: CURRENT_TIMESTAMP)

2. **`inventory`** (Katalog Barang & Layanan per Toko)
   - `id` (INT, Primary Key, Auto Increment)
   - `user_id` (INT, Foreign Key -> `users.id`)
   - `kode_barang` (VARCHAR(50))
   - `nama_barang` (VARCHAR(150))
   - `tipe` (ENUM('sparepart', 'jasa'), Default: 'sparepart')
   - `stok` (INT, Default: 0)
   - `stok_minimal` (INT, Default: 5)
   - `harga_beli` (DECIMAL(12, 2), Default: 0.00)
   - `harga_jual` (DECIMAL(12, 2))
   - `created_at` (TIMESTAMP, Default: CURRENT_TIMESTAMP)

3. **`transactions`** (Header Nota Transaksi)
   - `id` (INT, Primary Key, Auto Increment)
   - `user_id` (INT, Foreign Key -> `users.id`)
   - `no_nota` (VARCHAR(50), Unique, Format: `INV-YYYYMMDDHHMMSS`)
   - `nama_pelanggan` (VARCHAR(100), Default: 'Umum')
   - `total_harga` (DECIMAL(12, 2))
   - `created_at` (TIMESTAMP, Default: CURRENT_TIMESTAMP)

4. **`transaction_details`** (Rincian Item Transaksi)
   - `id` (INT, Primary Key, Auto Increment)
   - `transaction_id` (INT, Foreign Key -> `transactions.id`)
   - `inventory_id` (INT, Foreign Key -> `inventory.id`)
   - `jumlah` (INT)
   - `harga_satuan` (DECIMAL(12, 2))
   - `subtotal` (DECIMAL(12, 2))

---

## 🚀 Cara Memulai (Setup & Instalasi)

### 1. Prasyarat
- Python 3.8 atau lebih baru
- MySQL Server / MariaDB (XAMPP / Laragon / Standalone)

### 2. Persiapan Database
1. Buka MySQL client / phpMyAdmin.
2. Buat database baru:
   ```sql
   CREATE DATABASE autoservis_db;