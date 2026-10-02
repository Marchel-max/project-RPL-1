Buat aplikasi web B2B SaaS Kasir & Inventaris UMKM bernama AutoServis.

Tujuan:
Membantu pemilik UMKM (toko kelontong, minimarket, toko baju, bengkel, dan penyedia jasa) mengelola inventaris produk fisik dan layanan, memproses transaksi kasir (Point of Sale / POS), menghasilkan nomor nota otomatis, memotong stok barang fisik secara otomatis saat checkout tanpa mempengaruhi stok layanan, menyajikan laporan penjualan, serta menerapkan pembatasan fitur untuk paket Freemium dan Pro.

Tech stack yang digunakan:

- Frontend: HTML5 + Jinja2 + Tailwind CSS (via CDN) + Vanilla JavaScript
- Backend: Python 3.x + Flask
- Database: MySQL / MariaDB
- Driver: mysql-connector-python
- Keamanan: Werkzeug.security (Password Hashing) + Flask Session Management
- Manajemen Environment: python-dotenv (.env)
- Konfigurasi Proyek: .env.example

Aturan penulisan kode:

- Jangan tambahkan komentar kecuali benar-benar diperlukan.
- Gunakan snake_case untuk semua variabel Python, kolom database, route, dan nama fungsi.
- Gunakan camelCase atau snake_case secara konsisten untuk ID elemen DOM dan nama field form HTML.
- Usahakan panjang baris kode di bawah 150 karakter.
- Gunakan struktur folder yang bersih dan sederhana.
- Dukung autentikasi berbasis sesi (Flask Session) dan isolasi data multi-tenant (user_id).

Entitas utama:

1. User (Toko / Pelanggan SaaS)

   - id
   - nama_toko
   - email
   - password_hash
   - plan_type (free / pro)
   - expired_date
   - created_at

2. Inventory

   - id
   - user_id
   - kode_barang
   - nama_barang
   - tipe (sparepart / jasa)
   - stok
   - stok_minimal
   - harga_beli
   - harga_jual
   - created_at

3. Transaction

   - id
   - user_id
   - no_nota
   - nama_pelanggan
   - total_harga
   - created_at

4. TransactionDetail

   - id
   - transaction_id
   - inventory_id
   - jumlah
   - harga_satuan
   - subtotal

Aturan database & isolasi data (Multi-Tenant):

- Setiap data di tabel inventory dan transactions wajib terisolasi berdasarkan user_id pemilik toko.
- User hanya dapat membaca, mengubah, dan menghapus data yang memiliki user_id sesuai sesi login.
- Tipe item inventory dapat berupa 'sparepart' (stok fisik) atau 'jasa' (layanan non-stok).
- Kombinasi user_id dan kode_barang harus bersifat unik.
- Nilai no_nota transaksi harus unik dan dibuat otomatis dengan format INV-YYYYMMDDHHMMSS saat checkout.
- Saat transaksi diproses, potong stok HANYA untuk item yang bertipe 'sparepart'.
- JANGAN memotong stok atau menampilkan error saat memproses item yang bertipe 'jasa'.
- Sertakan seluruh item (baik sparepart maupun jasa) dalam kalkulasi total_harga dan subtotal.
- Penghapusan data transaksi akan menghapus data rincian di transaction_details secara otomatis (CASCADE).

Aturan bisnis Freemium & Feature Gate:

1. Akun Free (Gratis):
   - Maksimal 100 jenis item inventaris per user_id.
   - Maksimal 50 transaksi per hari (reset otomatis setiap hari berdasarkan tanggal created_at).
   - Tampilan cetak/print nota transaksi wajib menyertakan watermark (misal: "Printed with AutoServis Free").

2. Akun Pro (Berlangganan):
   - Unlimited jenis item inventaris.
   - Unlimited transaksi harian.
   - Tampilan cetak/print nota transaksi bebas dari watermark.

Fitur backend:

1. Autentikasi & Manajemen Sesi

   - Registrasi toko baru (default plan_type = 'free').
   - Login dan verifikasi password hash.
   - Logout dan penghancuran sesi.

2. CRUD Inventory (dengan Pembatasan Free Tier)

   - Menambah item atau jasa baru menggunakan form modal unified (#addModal).
   - Validasi batas maksimal 100 item inventaris untuk pengguna akun Free.
   - Mengisi nilai stok dummy (misal: 9999) dan harga beli nol (harga_beli = 0) secara otomatis jika tipe item adalah 'jasa'.
   - Mengubah data item milik user_id terkait.
   - Menghapus item dari inventaris milik user_id terkait.

3. POS Checkout (dengan Pembatasan Transaksi Harian)

   - Memproses input array (inventory_id[], jumlah[], harga_satuan[]).
   - Validasi batas maksimal 50 transaksi harian untuk pengguna akun Free.
   - Menghasilkan no_nota unik berformat INV-YYYYMMDDHHMMSS.
   - Menyimpan data utama transaksi ke header nota terikat pada user_id.
   - Menyimpan rincian data transaksi ke detail nota.
   - Memotong stok inventaris untuk item sparepart menggunakan query UPDATE inventory SET stok = stok - %s WHERE id = %s AND user_id = %s.

4. Laporan Penjualan & Print Nota

   - Menghitung total omzet penjualan spesifik user_id.
   - Mengembalikan ringkasan statistik dan tabel riwayat transaksi.
   - Mengambil rincian item per nota untuk modal pop-up dan halaman cetak nota.
   - Mengirim status watermark (True/False) ke template berdasarkan plan_type user.

Halaman frontend:

1. Autentikasi (login.html & register.html)

   - Form pendaftaran akun toko baru.
   - Form masuk akun.

2. Dashboard Inventaris (index.html)

   - Indicator status akun (Free / Pro) dan counter batas item/transaksi.
   - Ringkasan statistik stok barang fisik dan layanan jasa.
   - Form modal unified (#addModal) untuk menambah barang atau jasa.
   - Form modal edit item (#editModal).
   - Tabel daftar inventaris dilengkapi badge peringatan stok minimum.

3. POS / Kasir (kasir.html)

   - Pencarian item dan katalog pilihan.
   - Tabel keranjang belanja interaktif.
   - Form checkout yang mengirimkan field array (inventory_id[], jumlah[], harga_satuan[]).

4. Laporan Penjualan (laporan.html)

   - Card ringkasan total omzet dan total transaksi harian/bulanan.
   - Tabel riwayat penjualan yang menampilkan nomor nota.
   - Modal pop-up rincian transaksi & tombol cetak nota (dengan rendering watermark dinamis).

5. Penawaran Langganan (pricing.html)

   - Komparasi fitur paket Free vs Pro.
   - Tombol pengajuan upgrade akun ke Pro.

Persyaratan UI:

- Gunakan Bahasa Indonesia untuk semua label, tombol, pesan, dan placeholder input.
- Buat antarmuka dashboard yang bersih dan responsif menggunakan Tailwind CSS.
- Gunakan tabel, card, badge, modal pop-up, dan dialog konfirmasi sederhana.
- Tampilkan watermark pada tampilan cetak nota jika plan_type bernilai 'free'.
- Warna badge status:
  * Barang Fisik / Sparepart: biru
  * Layanan / Jasa: ungu
  * Peringatan Stok Minimum: merah
  * Akun Free: abu-abu / kuning
  * Akun Pro: hijau

Route yang dibutuhkan:

- GET /login
- POST /login
- GET /register
- POST /register
- GET /logout
- GET /
- POST /tambah_inventory
- POST /edit/<id>
- POST /delete/<id>
- GET /kasir
- POST /proses_transaksi
- GET /laporan
- GET /nota/<id>
- GET /pricing

Deliverables:

- Kode sumber backend Flask lengkap di app.py.
- File template HTML Jinja2 (login, register, index, kasir, laporan, nota, pricing).
- File konfigurasi environment (.env.example, requirements.txt).
- Script SQL DDL untuk pembuatan tabel database multi-tenant.
- File README berisi panduan instalasi, setup database, konfigurasi environment, dan cara menjalankan aplikasi.

Struktur proyek:

autoservis/
├── ARCHITECTURE.md
├── README.md
├── app.py
├── .env
├── .env.example
├── requirements.txt
├── static/
│   ├── css/
│   └── js/
└── templates/
    ├── login.html
    ├── register.html
    ├── pricing.html
    ├── index.html
    ├── kasir.html
    ├── laporan.html
    └── nota.html