# AutoServis - SaaS Manajemen Bengkel & Booking Online

**AutoServis** adalah platform digital berbasis B2B SaaS (*Software-as-a-Service*) yang dirancang untuk membantu pemilik bengkel UMKM mendigitalisasi operasional harian. Sistem ini menggabungkan manajemen inventaris, kasir (POS), rekam medis kendaraan, serta sistem antrean dan pengingat servis otomatis untuk meningkatkan efisiensi bisnis dan retensi pelanggan.

---

## 🎯 Masalah & Solusi

* **Masalah:** Banyak bengkel UMKM masih menggunakan pencatatan manual, sering kehabisan atau kehilangan stok *sparepart*, tidak memiliki riwayat servis kendaraan pelanggan, serta kesulitan mempertahankan pelanggan agar kembali melakukan servis berkala.
* **Solusi:** AutoServis menyediakan *dashboard* terintegrasi untuk pengelolaan stok dan kasir, portal *booking online* bagi pelanggan, rekam medis kendaraan berbasis plat nomor, serta pengingat servis otomatis via WhatsApp Gateway.

---

## ✨ Fitur Utama

### 🛠️ Modul Bengkel (Web Admin & Dashboard POS)
* **Point of Sales (POS) & Kasir:** Transaksi cepat dan pencetakan nota/invoice digital.
* **Manajemen Inventaris *Sparepart*:** Pencatatan stok keluar-masuk otomatis yang memotong jumlah barang secara *real-time* saat terjadi transaksi.
* **Alert Stok Minimum:** Notifikasi otomatis jika persediaan suku cadang tertentu mulai menipis.
* **Rekam Medis Kendaraan (Service History):** Pencatatan riwayat perbaikan dan penggantian *part* berdasarkan nomor plat kendaraan.
* **Manajemen Antrean & Booking:** Konfirmasi dan alokasi jadwal servis masuk dari pelanggan.

### 📱 Modul Pelanggan (Web Portal / App)
* **Booking Servis Online:** Pilihan jadwal dan konsultasi keluhan awal secara *online*.
* **Status Servis Real-Time:** Memantau proses pengerjaan kendaraan dari jarak jauh.
* **Riwayat Servis Digital:** Mengakses histori perbaikan kendaraan kapan saja.

### 🔔 Modul Notifikasi & Automasi
* **WhatsApp Gateway:** Pengiriman notifikasi pengingat otomatis untuk servis berkala (misal: 3 bulan setelah servis terakhir).

---

## 💼 Model Bisnis (Monetisasi)

1. **B2B Subscription (SaaS):** 
   * **Freemium:** Gratis hingga 50 transaksi pertama/bulan.
   * **Pro Plan:** Biaya langganan bulanan/tahunan untuk akses transaksi *unlimited* dan fitur pengingat WhatsApp.
2. **Affiliate Supplier Commissions:** Komisi dari distributor *sparepart* saat bengkel melakukan *restock* bahan baku melalui platform.

---

## 🛠️ Tech Stack (Rencana Pengembangan)

* **Frontend:** React.js / Vue.js / Tailwind CSS
* **Backend:** Node.js (Express) / Laravel
* **Database:** PostgreSQL / MySQL
* **Authentication:** JWT / Firebase Auth
* **Third-Party API:** WhatsApp Gateway API (Fonnte / Twilio)

---

## 📊 Structure Database Utama (ERD Preview)

* `Users` (Admin Bengkel, Mekanik, Pelanggan)
* `Vehicles` (Plat Nomor, Merek, Tipe, Tahun)
* `Services` (Jenis Servis, Biaya Jasa)
* `Inventory` (Kode Barang, Nama Sparepart, Stok, Harga Beli, Harga Jual)
* `Bookings` (Tanggal, Jam, Status, Keluhan)
* `Transactions` (Detail Nota, Total Bayar, Metode Pembayaran)

---

## 📝 Lisensi

Proyek ini dikembangkan untuk tujuan akademis dan pengembangan open-source di bawah lisensi [MIT License](LICENSE).# AutoServis - SaaS Manajemen Bengkel & Booking Online

**AutoServis** adalah platform digital berbasis B2B SaaS (*Software-as-a-Service*) yang dirancang untuk membantu pemilik bengkel UMKM mendigitalisasi operasional harian. Sistem ini menggabungkan manajemen inventaris, kasir (POS), rekam medis kendaraan, serta sistem antrean dan pengingat servis otomatis untuk meningkatkan efisiensi bisnis dan retensi pelanggan.

---

## 🎯 Masalah & Solusi

* **Masalah:** Banyak bengkel UMKM masih menggunakan pencatatan manual, sering kehabisan atau kehilangan stok *sparepart*, tidak memiliki riwayat servis kendaraan pelanggan, serta kesulitan mempertahankan pelanggan agar kembali melakukan servis berkala.
* **Solusi:** AutoServis menyediakan *dashboard* terintegrasi untuk pengelolaan stok dan kasir, portal *booking online* bagi pelanggan, rekam medis kendaraan berbasis plat nomor, serta pengingat servis otomatis via WhatsApp Gateway.

---

## ✨ Fitur Utama

### 🛠️ Modul Bengkel (Web Admin & Dashboard POS)
* **Point of Sales (POS) & Kasir:** Transaksi cepat dan pencetakan nota/invoice digital.
* **Manajemen Inventaris *Sparepart*:** Pencatatan stok keluar-masuk otomatis yang memotong jumlah barang secara *real-time* saat terjadi transaksi.
* **Alert Stok Minimum:** Notifikasi otomatis jika persediaan suku cadang tertentu mulai menipis.
* **Rekam Medis Kendaraan (Service History):** Pencatatan riwayat perbaikan dan penggantian *part* berdasarkan nomor plat kendaraan.
* **Manajemen Antrean & Booking:** Konfirmasi dan alokasi jadwal servis masuk dari pelanggan.

### 📱 Modul Pelanggan (Web Portal / App)
* **Booking Servis Online:** Pilihan jadwal dan konsultasi keluhan awal secara *online*.
* **Status Servis Real-Time:** Memantau proses pengerjaan kendaraan dari jarak jauh.
* **Riwayat Servis Digital:** Mengakses histori perbaikan kendaraan kapan saja.

### 🔔 Modul Notifikasi & Automasi
* **WhatsApp Gateway:** Pengiriman notifikasi pengingat otomatis untuk servis berkala (misal: 3 bulan setelah servis terakhir).

---

## 💼 Model Bisnis (Monetisasi)

1. **B2B Subscription (SaaS):** 
   * **Freemium:** Gratis hingga 50 transaksi pertama/bulan.
   * **Pro Plan:** Biaya langganan bulanan/tahunan untuk akses transaksi *unlimited* dan fitur pengingat WhatsApp.
2. **Affiliate Supplier Commissions:** Komisi dari distributor *sparepart* saat bengkel melakukan *restock* bahan baku melalui platform.

---

## 🛠️ Tech Stack (Rencana Pengembangan)

* **Frontend:** React.js / Vue.js / Tailwind CSS
* **Backend:** Node.js (Express) / Laravel
* **Database:** PostgreSQL / MySQL
* **Authentication:** JWT / Firebase Auth
* **Third-Party API:** WhatsApp Gateway API (Fonnte / Twilio)

---

## 📊 Structure Database Utama (ERD Preview)

* `Users` (Admin Bengkel, Mekanik, Pelanggan)
* `Vehicles` (Plat Nomor, Merek, Tipe, Tahun)
* `Services` (Jenis Servis, Biaya Jasa)
* `Inventory` (Kode Barang, Nama Sparepart, Stok, Harga Beli, Harga Jual)
* `Bookings` (Tanggal, Jam, Status, Keluhan)
* `Transactions` (Detail Nota, Total Bayar, Metode Pembayaran)

---

## 📝 Lisensi

Proyek ini dikembangkan untuk tujuan akademis dan pengembangan open-source di bawah lisensi [MIT License](LICENSE).
