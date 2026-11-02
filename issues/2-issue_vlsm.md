# [Feature] Variable Length Subnet Mask (VLSM) Designer

## Deskripsi
Implementasi fitur perancangan alokasi Variable Length Subnet Mask (VLSM) berbasis web menggunakan framework FastAPI di sisi backend (Python 3.12) dan integrasi tab "VLSM Designer" pada antarmuka web `index.html`. Sistem ini memecah blok IP besar (induk) menjadi beberapa blok subnet yang lebih kecil berdasarkan daftar kebutuhan host secara hierarkis tanpa terjadi tabrakan (overlap) dan efisien dalam penggunaan ruang alamat IP sesuai spesifikasi teknis `SPEC.md`.

## Tugas
- [ ] **Backend (FastAPI)**:
  - Implementasi fungsi logika inti `alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]`:
    - Validasi format `network_cidr` (format IPv4 dan Prefix valid, serta IP harus merupakan alamat network awal yang sah).
    - Validasi daftar `kebutuhan_host`: tidak boleh kosong (empty list) dan seluruh elemen harus bernilai integer $\ge 1$.
    - Mengurutkan daftar kebutuhan host dari yang terbesar ke terkecil (descending).
    - Menghitung ukuran blok dengan pangkat 2 terkecil yang memenuhi $\ge (\text{kebutuhan} + 2)$, dengan alokasi minimum prefix /30.
    - Mengalokasikan blok subnet secara berurutan mulai dari awal `network_cidr`.
    - Validasi kapasitas: memicu `ValueError` apabila total alokasi melebihi kapasitas blok induk.
  - Endpoint API FastAPI:
    - `POST /api/vlsm` menerima body JSON `{"network": str, "kebutuhan_host": list[int]}`.
    - Mengembalikan HTTP 200 dengan daftar JSON alokasi VLSM lengkap.
    - Error handling: menangkap `ValueError` dan mengembalikan HTTP 400 Bad Request dengan format `{"detail": "[pesan error]"}`.
- [ ] **Frontend (`index.html`)**:
  - Menghubungkan tombol "Calculate VLSM" pada tab VLSM Designer ke endpoint `POST /api/vlsm`.
  - Mengambil input CIDR network induk dan daftar dinamis kebutuhan host.
  - Menampilkan hasil alokasi berupa tabel dengan kolom: Kebutuhan, Alokasi CIDR, Netmask, Network, Range Host, Broadcast.
  - Feedback visual kontainer alert dengan teks berwarna merah jika terjadi kesalahan validasi input atau kapasitas tidak mencukupi (status 400).
- [ ] **Testing (pytest)**:
  - Menulis test suite VLSM di `test_main.py` menggunakan `pytest.mark.parametrize` mencakup TC12, TC13, serta kasus validasi input VLSM (network tidak valid, host list kosong, nilai host < 1, dan POST /api/vlsm).

## Kriteria Penerimaan
Kriteria penerimaan merujuk langsung pada tabel test case di `SPEC.md`:

| ID | Tipe Pengujian | Input Data | Hasil yang Diharapkan |
|---|---|---|---|
| **TC12** | VLSM Normal Berhasil | Net: `192.168.1.0/24`, Kebutuhan: `[100, 50, 20, 2]` | Blok `/25 (.0)`, `/26 (.128)`, `/27 (.192)`, `/30 (.224)` dialokasikan sukses tanpa overlap |
| **TC13** | VLSM Kapasitas Gagal | Net: `192.168.1.0/24`, Kebutuhan: `[200, 100]` | `raise ValueError` / HTTP 400 (Ditolak - Kapasitas tidak muat) |
| **TC-VLSM-01** | Validasi Network Bukan Network ID | Net: `192.168.1.5/24`, Kebutuhan: `[50]` | `raise ValueError` / HTTP 400 (Ditolak - Bukan network address valid) |
| **TC-VLSM-02** | Validasi Kebutuhan Kosong | Net: `192.168.1.0/24`, Kebutuhan: `[]` | `raise ValueError` / HTTP 400 (Ditolak - Kebutuhan kosong) |
| **TC-VLSM-03** | Validasi Kebutuhan < 1 | Net: `192.168.1.0/24`, Kebutuhan: `[50, 0]` | `raise ValueError` / HTTP 400 (Ditolak - Nilai kebutuhan harus >= 1) |

## Alur Kerja
`issue -> branch -> test dulu -> implementasi -> commit -> pull request -> CI -> merge`
