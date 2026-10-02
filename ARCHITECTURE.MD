Buat aplikasi web B2B SaaS bernama AutoServis.

Tujuan:
Membantu pemilik bengkel mengelola inventaris barang fisik (sparepart) dan tarif jasa, memproses transaksi kasir (Point of Sale / POS), menghasilkan nomor nota otomatis, memotong stok barang fisik secara otomatis saat checkout tanpa mempengaruhi stok jasa, serta menampilkan laporan kinerja penjualan.

Tech stack yang digunakan:

- Frontend: HTML5 + Jinja2 + Tailwind CSS (via CDN) + Vanilla JavaScript
- Backend: Python 3.x + Flask
- Database: MySQL / MariaDB
- Driver: mysql-connector-python
- Manajemen Environment: python-dotenv (.env)
- Konfigurasi Proyek: .env.example

Aturan penulisan kode:

- Jangan tambahkan komentar kecuali benar-benar diperlukan.
- Gunakan snake_case untuk semua variabel Python, kolom database, route, dan nama fungsi.
- Gunakan camelCase atau snake_case secara konsisten untuk ID elemen DOM dan nama field form HTML.
- Usahakan panjang baris kode di bawah 150 karakter.
- Gunakan struktur folder yang bersih dan sederhana.
- Tetap dukung fallback pengiriman form HTML standar (application/x-www-form-urlencoded) serta format JSON.

Entitas utama:

1. Inventory

   - id
   - kode_barang
   - nama_barang
   - tipe
   - stok
   - stok_minimal
   - harga_beli
   - harga_jual
   - created_at

2. Transaction

   - id
   - no_nota
   - nama_pelanggan
   - total_harga
   - created_at

3. TransactionDetail

   - id
   - transaction_id
   - inventory_id
   - jumlah
   - harga_satuan
   - subtotal

Aturan database:

- Tipe item dapat berupa 'sparepart' (stok fisik) atau 'jasa' (layanan servis).
- Nilai kode_barang harus bersifat unik.
- Nilai no_nota transaksi harus unik dan dibuat otomatis dengan format INV-YYYYMMDDHHMMSS saat checkout.
- Saat transaksi diproses, potong stok HANYA untuk item yang bertipe 'sparepart'.
- JANGAN memotong stok atau menampilkan error saat memproses item yang bertipe 'jasa'.
- Sertakan seluruh item (baik sparepart maupun jasa) dalam kalkulasi total_harga dan subtotal.
- Penghapusan data transaksi akan menghapus data rincian di transaction_details secara otomatis (CASCADE).

Fitur backend:

1. CRUD Inventory

   - Menambah item atau jasa baru menggunakan form modal unified (#addModal).
   - Mengisi nilai stok dummy (misal: 9999) dan harga beli nol (harga_beli = 0) secara otomatis jika tipe item adalah 'jasa'.
   - Mengubah data item yang sudah ada.
   - Menghapus item dari inventaris.

2. POS Checkout

   - Memproses input array (inventory_id[], jumlah[], harga_satuan[]).
   - Menghasilkan no_nota unik berformat INV-YYYYMMDDHHMMSS.
   - Menyimpan data utama transaksi ke header nota.
   - Menyimpan rincian data transaksi ke detail nota.
   - Memotong stok inventaris untuk item sparepart menggunakan query UPDATE inventory SET stok = stok - %s.

3. Laporan Penjualan

   - Menghitung total omzet penjualan.
   - Mengembalikan ringkasan statistik dan tabel riwayat transaksi.
   - Mengambil rincian item per nota untuk ditampilkan pada modal pop-up.

Halaman frontend:

1. Dashboard Inventaris (index.html)

   - Ringkasan statistik stok sparepart dan layanan jasa.
   - Form modal unified (#addModal) untuk menambah sparepart atau jasa.
   - Form modal edit item (#editModal).
   - Tabel daftar inventaris dilengkapi badge peringatan stok minimum.

2. POS / Kasir (kasir.html)

   - Pencarian item dan katalog pilihan.
   - Tabel keranjang belanja interaktif.
   - Form checkout yang mengirimkan field array (inventory_id[], jumlah[], harga_satuan[]).

3. Laporan Penjualan (laporan.html)

   - Card ringkasan total omzet dan total transaksi.
   - Tabel riwayat penjualan yang menampilkan nomor nota.
   - Modal pop-up rincian transaksi.

Persyaratan UI:

- Gunakan Bahasa Indonesia untuk semua label, tombol, pesan, dan placeholder input.
- Buat antarmuka dashboard yang bersih dan responsif menggunakan Tailwind CSS.
- Gunakan tabel, card, badge, modal pop-up, dan dialog konfirmasi sederhana.
- Warna badge status:
  * Sparepart: biru
  * Jasa: ungu
  * Peringatan Stok Minimum: merah

Route yang dibutuhkan:

- GET /
- POST /tambah_inventory
- POST /edit/<id>
- POST /delete/<id>
- GET /kasir
- POST /proses_transaksi
- GET /laporan

Deliverables:

- Kode sumber backend Flask lengkap di app.py.
- File template HTML Jinja2.
- File konfigurasi environment (.env.example, requirements.txt).
- Script SQL DDL untuk pembuatan tabel database.
- File README berisi panduan instalasi, setup database, konfigurasi environment, dan cara menjalankan aplikasi.

Struktur proyek:

autoservis/
├── app.py
├── .env
├── .env.example
├── requirements.txt
├── README.md
├── static/
│   ├── css/
│   └── js/
└── templates/
    ├── index.html
    ├── kasir.html
    └── laporan.html