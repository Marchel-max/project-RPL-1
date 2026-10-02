# AutoServis - Platform B2B SaaS Manajemen Bengkel

AutoServis adalah platform digital B2B SaaS (Software-as-a-Service) yang dirancang untuk membantu pemilik bengkel UMKM mendigitalisasi operasional harian. Sistem ini mengintegrasikan pengelolaan inventaris (sparepart & jasa), kasir (Point of Sale), serta pelaporan omzet dan modal secara real-time.

---

## 🎯 Masalah & Solusi

- Masalah: Banyak bengkel UMKM masih menggunakan pencatatan manual, sering kehabisan stok sparepart, tidak memisahkan pencatatan antara jasa servis dan barang fisik, serta kesulitan melacak riwayat omzet harian.
- Solusi: AutoServis menyediakan dashboard terintegrasi untuk pengelolaan stok sparepart & jasa, kasir POS serbaguna yang otomatis memotong stok barang fisik tanpa mengganggu inventaris jasa, serta laporan penjualan otomatis.

---

## 🚀 Fitur yang Sudah Implementasi (MVP)

1. Dashboard Inventaris Terpadu (Sparepart & Jasa)
   - Pencatatan barang fisik (Sparepart) dan layanan (Jasa).
   - Alert indikator stok minimum.
   - Form modal pop-up unified (+ Tambah Item / Jasa).

2. Point of Sales (POS / Kasir)
   - Dukungan keranjang transaksi campuran (Sparepart + Jasa).
   - Pembuatan Nomor Nota Otomatis (Format: INV-YYYYMMDDHHMMSS).
   - Otomatisasi pemotongan stok khusus item sparepart saat transaksi diproses.

3. Laporan Penjualan & Modal
   - Pencatatan total omzet dan riwayat transaksi.
   - Modal Rincian Nota untuk melihat detail item yang dibeli.

---

## 🛠️ Tech Stack Saat Ini

- Frontend: HTML5, Tailwind CSS (via CDN), Vanilla JavaScript, Jinja2 Template Engine
- Backend: Python 3.x, Flask Framework
- Database: MySQL / MariaDB
- Database Driver: mysql-connector-python
- Environment Management: python-dotenv

---

## 📊 Database Schema Saat Ini

1. inventory (Katalog Sparepart & Jasa)
   - id (INT, Primary Key, Auto Increment)
   - kode_barang (VARCHAR(50), Unique)
   - nama_barang (VARCHAR(150))
   - tipe (ENUM('sparepart', 'jasa'), Default: 'sparepart')
   - stok (INT, Default: 0)
   - stok_minimal (INT, Default: 5)
   - harga_beli (DECIMAL(12, 2), Default: 0.00)
   - harga_jual (DECIMAL(12, 2))
   - created_at (TIMESTAMP, Default: CURRENT_TIMESTAMP)

2. transactions (Header Nota Penjualan)
   - id (INT, Primary Key, Auto Increment)
   - no_nota (VARCHAR(50), Unique, Format: INV-YYYYMMDDHHMMSS)
   - nama_pelanggan (VARCHAR(100), Default: 'Umum')
   - total_harga (DECIMAL(12, 2))
   - created_at (TIMESTAMP, Default: CURRENT_TIMESTAMP)

3. transaction_details (Rincian Item Transaksi)
   - id (INT, Primary Key, Auto Increment)
   - transaction_id (INT, Foreign Key -> transactions.id)
   - inventory_id (INT, Foreign Key -> inventory.id)
   - jumlah (INT)
   - harga_satuan (DECIMAL(12, 2))
   - subtotal (DECIMAL(12, 2))

---

## 🔮 Rencana Pengembangan (Roadmap Fitur Masa Depan)

1. Modul Pelanggan & Booking Online
   - Portal web untuk pelanggan memilih jadwal dan booking servis.
2. Modul Notifikasi & Automasi
   - Integrasi WhatsApp Gateway (Fonnte/Twilio) untuk pengingat servis otomatis.
3. Rekam Medis Kendaraan (Vehicles)
   - Tracking riwayat perbaikan berdasarkan nomor plat kendaraan.
4. Multi-user & Role Management (Users)
   - Autentikasi JWT / Firebase Auth untuk pemisahan hak akses Admin Bengkel, Mekanik, dan Kasir.

---

## 💻 Cara Menjalankan Aplikasi

1. Clone repositori ini dan masuk ke folder proyek:
   cd autoservis

2. Buat database di MySQL / MariaDB:
   CREATE DATABASE autoservis_db;

3. Buat file .env dan atur konfigurasi database:
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=
   DB_NAME=autoservis_db
   DB_PORT=3306

4. Install dependency:
   pip install -r requirements.txt

5. Jalankan aplikasi Flask:
   python app.py

6. Akses aplikasi melalui browser di http://localhost:5000

---

## 📝 Lisensi

Proyek ini dikembangkan untuk tujuan akademis di bawah lisensi MIT License.
