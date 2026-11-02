Spesifikasi Teknis: Kalkulator Subnet & VLSM Berbasis Web
Tujuan
Dokumen spesifikasi ini mendefinisikan arsitektur, aturan logika bisnis, dan antarmuka untuk aplikasi Kalkulator Subnet dan Variable Length Subnet Mask (VLSM). Sistem ini dirancang menggunakan Python 3.12 dengan framework FastAPI di sisi backend, dan satu halaman antarmuka HTML murni di sisi frontend. Spesifikasi ini menjadi panduan absolut bagi pengembang untuk mengimplementasikan kode aplikasi dan pengujian (pytest).
Aturan Validasi
Seluruh input dari antarmuka maupun request API langsung harus tunduk pada aturan ketat berikut sebelum diproses oleh fungsi inti:
Format IPv4:
Harus terdiri dari tepat 4 oktet yang dipisahkan oleh tanda titik (.).
Nilai setiap oktet berada pada rentang numerik 0 hingga 255.
Ketat: Tidak diizinkan ada angka nol di depan (leading zeros), contoh 192.168.01.1 wajib ditolak.
Ketat: Tidak diizinkan ada karakter spasi atau karakter non-numerik lainnya.
Format Prefix:
Harus berupa bilangan bulat (integer).
Rentang nilai yang valid adalah 0 hingga 32.
Penyimpangan Input:
Semua input yang melanggar aturan di atas wajib memicu exception (tingkat fungsi) atau HTTP response kesalahan (tingkat API).
Kontrak Fungsi
Logika utama aplikasi harus dienkapsulasi dalam modul main.py menggunakan fungsi berikut:
1. hitung_subnet(ip: str, prefix: int) -> dict
Fungsi dasar untuk menghitung parameter subnetting IPv4.
Logika Perhitungan:
network: Dihitung menggunakan operasi bitwise AND antara IP address dan subnet mask.
usable_hosts: Dihitung dengan rumus 2(32-prefix)-2 untuk prefix 0 hingga 30.
Penanganan Edge Case:
/31 (RFC 3021 Point-to-Point): Jumlah host = 2, broadcast = None. IP pertama dan kedua dalam blok merupakan host yang valid.
/32 (Host Route): Jumlah host = 1, broadcast = None, first_host dan last_host bernilai sama dengan IP yang diinput.
Output (Dictionary Keys):
mask (str): Subnet mask format desimal bertitik (contoh: 255.255.255.0).
network (str): Alamat network.
broadcast (str | None): Alamat broadcast.
first_host (str): Alamat IP host pertama yang dapat digunakan.
last_host (str): Alamat IP host terakhir yang dapat digunakan.
usable_hosts (int): Jumlah host yang tersedia.
Error Handling: Melakukan raise ValueError("Pesan detail") jika input tidak valid.
2. alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]
Fungsi untuk memecah blok IP besar menjadi blok-blok subnet yang lebih kecil berdasarkan kebutuhan tanpa overlap.
Logika Proses:
Validasi format network_cidr (harus memenuhi aturan IP dan Prefix, serta valid sebagai alamat network awal).
Urutkan elemen di dalam kebutuhan_host dari nilai terbesar ke terkecil (descending).
Alokasikan subnet secara berurutan, dimulai persis dari alamat network_cidr awal.
Penentuan Blok: Gunakan pangkat 2 terkecil di mana nilainya  (kebutuhan + 2). Alokasi minimum yang diizinkan untuk VLSM adalah prefix /30 (kapasitas 2 host).
Output:
Mengembalikan list of dictionaries. Setiap dictionary mengandung:
kebutuhan (int): Jumlah host yang direkues.
network_cidr (str): Hasil blok yang didapat (contoh: 192.168.1.0/25).
Plus seluruh kunci output dari fungsi hitung_subnet.
Error Handling: Melakukan raise ValueError("Pesan detail") apabila:
network_cidr bukan alamat network yang valid.
kebutuhan_host kosong (empty list).
Terdapat nilai <1 di dalam kebutuhan_host.
Kapasitas blok IP induk tidak mencukupi untuk menampung seluruh total akumulasi kebutuhan_host.
Kontrak API
Mengekspos logika internal ke frontend dengan spesifikasi routing FastAPI:
GET /
Mengembalikan berkas index.html (antarmuka web).
GET /api/subnet
Query Parameters: ip (string), prefix (integer).
Response Berhasil (200 OK): Objek JSON yang memuat seluruh key dari output hitung_subnet.
POST /api/vlsm
Body Request (JSON): Memuat dua field, yaitu network (string) dan kebutuhan_host (array of integers).
Response Berhasil (200 OK): JSON Array yang memuat daftar alokasi VLSM dari output alokasi_vlsm.
Standar Penanganan Error:
Semua exception ValueError yang terpicu dari fungsi inti akan ditangkap oleh FastAPI dan dikembalikan dengan HTTP Status 400 Bad Request.
Format Error JSON: {"detail": "[Pesan spesifik terkait kesalahan validasi/kapasitas]"}
Halaman Web (Frontend)
Hanya menggunakan satu berkas HTML (index.html) terpadu yang memuat kerangka struktur, styling dasar, dan vanilla JavaScript.
Navigasi Mode: Terdapat UI toggle atau tab untuk berpindah antara fungsi "Kalkulator Subnet" dan "Kalkulator VLSM".
Kalkulator Subnet: Memiliki dua input (IP Address dan Prefix). Menampilkan hasil berupa tabel 6 baris (Network, Mask, Broadcast, First Host, Last Host, Usable Hosts).
Kalkulator VLSM: Memiliki input Network Induk (CIDR) dan area input dinamis untuk menambahkan daftar kebutuhan host. Menampilkan hasil berupa tabel dengan baris sejumlah blok kebutuhan, memuat kolom: Kebutuhan, Alokasi CIDR, Netmask, Network, Range Host, Broadcast.
Feedback Visual: Menyediakan kontainer alert khusus. Jika API mengembalikan status 400, pesan dari properti detail wajib dirender dengan gaya teks berwarna merah untuk memudahkan debugging input pengguna.
Tabel Test Case (pytest: test_main.py)
Skema di bawah ini wajib menjadi landasan unit pengujian (Unit Test) untuk Continuous Integration.
ID
Tipe Pengujian
Input Data
Hasil yang Diharapkan
TC01
Subnet Normal
IP: 172.16.5.130, Prefix: 25
Network: 172.16.5.128, Broadcast: 172.16.5.255, Usable: 126
TC02
Subnet Minim
IP: 10.0.0.0, Prefix: 30
Range: 10.0.0.1 - 10.0.0.2, Broadcast: 10.0.0.3, Usable: 2
TC03
Subnet RFC 3021
IP: 192.168.1.0, Prefix: 31
Point-to-point, Usable: 2, Broadcast: None
TC04
Subnet Host Route
IP: 192.168.1.5, Prefix: 32
Usable: 1, First/Last Host: 192.168.1.5, Broadcast: None
TC05
Validasi Oktet
IP: 256.1.1.1, Prefix: 24
raise ValueError / HTTP 400 (Ditolak)
TC06
Validasi Leading Zero
IP: 192.168.01.1, Prefix: 24
raise ValueError / HTTP 400 (Ditolak)
TC07
Validasi Format Kurang
IP: 192.168.1, Prefix: 24
raise ValueError / HTTP 400 (Ditolak)
TC08
Validasi Tipe Karakter
IP: abc, Prefix: 24
raise ValueError / HTTP 400 (Ditolak)
TC09
Validasi Data Kosong
IP: , Prefix:
raise ValueError / HTTP 400 (Ditolak)
TC10
Validasi Prefix Atas
IP: 192.168.1.1, Prefix: 33
raise ValueError / HTTP 400 (Ditolak)
TC11
Validasi Prefix Bawah
IP: 10.0.0.1, Prefix: -1
raise ValueError / HTTP 400 (Ditolak)
TC12
VLSM Normal Berhasil
Net: 192.168.1.0/24

Kebutuhan: 100, 50, 20, 2
Blok /25 (.0), /26 (.128), /27 (.192), /30 (.224) dialokasikan sukses
TC13
VLSM Kapasitas Gagal
Net: 192.168.1.0/24

Kebutuhan: 200, 100
raise ValueError / HTTP 400 (Ditolak - Tidak muat)

Di Luar Cakupan (Out of Scope)
Fungsi-fungsi berikut ini tidak termasuk dalam rilis pengembangan saat ini dan tidak perlu diimplementasikan:
Dukungan dan perhitungan untuk protokol IPv6.
Integrasi Database (sistem sepenuhnya stateless dan tidak menyimpan rekam jejak kalkulasi).
Autentikasi dan Autorisasi pengguna (API bersifat publik/lokal).
Penggunaan framework frontend kompleks (seperti React, Vue, atau Angular); cukup menggunakan vanilla HTML/JS/CSS.
Mode cetak atau ekspor dokumen hasil (PDF, CSV).
