# [Feature] Kalkulator Subnet & VLSM

## Deskripsi
Implementasi fitur Kalkulator Subnet IPv4 dan Variable Length Subnet Mask (VLSM) berbasis web menggunakan framework FastAPI di sisi backend (Python 3.12) dan satu berkas antarmuka `index.html` (vanilla HTML, CSS, JavaScript) di sisi frontend. Sistem ini menyediakan perhitungan parameter subnetting (network address, subnet mask, broadcast address, usable hosts range, dan jumlah host) serta alokasi blok VLSM hierarkis yang efisien dan bebas overlap sesuai spesifikasi teknis pada `SPEC.md`.

## Tugas
- [ ] **Backend (FastAPI)**:
  - Implementasi fungsi logika inti `hitung_subnet(ip: str, prefix: int) -> dict` dengan penanganan edge case (/31 point-to-point RFC 3021, /32 host route).
  - Implementasi fungsi logika inti `alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]` dengan sorting kebutuhan descending dan deteksi kapasitas overflow.
  - Validasi ketat format IPv4 (4 oktet, rentang 0-255, tanpa leading zero, tanpa karakter spasi/non-numerik) dan rentang prefix (0-32).
  - Penyediaan endpoint API:
    - `GET /` : Menyajikan halaman web `index.html`.
    - `GET /api/subnet` : Menghitung parameter subnetting berdasarkan query params `ip` dan `prefix`.
    - `POST /api/vlsm` : Melakukan alokasi VLSM berdasarkan request body `{"network": str, "kebutuhan_host": list[int]}`.
  - Error handling: Menangkap `ValueError` dan mengembalikan response HTTP 400 Bad Request dengan format JSON `{"detail": "[pesan error]"}`.
- [ ] **Frontend (`index.html`)**:
  - Navigasi tab / switch antara Kalkulator Subnet dan Kalkulator VLSM.
  - Tampilan input dan tabel 6 baris hasil kalkulasi subnet (Network, Mask, Broadcast, First Host, Last Host, Usable Hosts).
  - Tampilan input dinamis kebutuhan host dan tabel alokasi VLSM (Kebutuhan, Alokasi CIDR, Netmask, Network, Range Host, Broadcast).
  - Feedback visual kontainer alert dengan teks merah jika menerima HTTP 400 dari API.
- [ ] **Testing (pytest)**:
  - Membuat unit test dan API test di `tests/test_main.py` mencakup seluruh test case TC01 hingga TC13.
  - Menjalankan pengukuran code coverage dengan `pytest-cov`.

## Kriteria Penerimaan
Kriteria penerimaan merujuk langsung pada tabel test case di `SPEC.md`:

| ID | Tipe Pengujian | Input Data | Hasil yang Diharapkan |
|---|---|---|---|
| **TC01** | Subnet Normal | IP: `172.16.5.130`, Prefix: `25` | Network: `172.16.5.128`, Broadcast: `172.16.5.255`, Usable: `126` |
| **TC02** | Subnet Minim | IP: `10.0.0.0`, Prefix: `30` | Range: `10.0.0.1 - 10.0.0.2`, Broadcast: `10.0.0.3`, Usable: `2` |
| **TC03** | Subnet RFC 3021 | IP: `192.168.1.0`, Prefix: `31` | Point-to-point, Usable: `2`, Broadcast: `None` |
| **TC04** | Subnet Host Route | IP: `192.168.1.5`, Prefix: `32` | Usable: `1`, First/Last Host: `192.168.1.5`, Broadcast: `None` |
| **TC05** | Validasi Oktet | IP: `256.1.1.1`, Prefix: `24` | `raise ValueError` / HTTP 400 (Ditolak) |
| **TC06** | Validasi Leading Zero | IP: `192.168.01.1`, Prefix: `24` | `raise ValueError` / HTTP 400 (Ditolak) |
| **TC07** | Validasi Format Kurang | IP: `192.168.1`, Prefix: `24` | `raise ValueError` / HTTP 400 (Ditolak) |
| **TC08** | Validasi Tipe Karakter | IP: `abc`, Prefix: `24` | `raise ValueError` / HTTP 400 (Ditolak) |
| **TC09** | Validasi Data Kosong | IP: `""`, Prefix: `""` | `raise ValueError` / HTTP 400 (Ditolak) |
| **TC10** | Validasi Prefix Atas | IP: `192.168.1.1`, Prefix: `33` | `raise ValueError` / HTTP 400 (Ditolak) |
| **TC11** | Validasi Prefix Bawah | IP: `10.0.0.1`, Prefix: `-1` | `raise ValueError` / HTTP 400 (Ditolak) |
| **TC12** | VLSM Normal Berhasil | Net: `192.168.1.0/24`, Kebutuhan: `[100, 50, 20, 2]` | Blok `/25 (.0)`, `/26 (.128)`, `/27 (.192)`, `/30 (.224)` dialokasikan sukses |
| **TC13** | VLSM Kapasitas Gagal | Net: `192.168.1.0/24`, Kebutuhan: `[200, 100]` | `raise ValueError` / HTTP 400 (Ditolak - Tidak muat) |

## Alur Kerja
Alur pengembangan mengikuti siklus berikut:
`issue -> branch -> test dulu -> implementasi -> commit -> pull request -> CI -> merge`

1. **Issue**: Pembuatan GitHub Issue untuk mendokumentasikan spesifikasi, tugas, dan acceptance criteria.
2. **Branch**: Membuat feature branch dari `main` dengan format `feature/issue-<nomor>-subnet-calculator`.
3. **Test Dulu (TDD)**: Menulis test suite di `tests/test_main.py` berdasarkan test case TC01–TC13 sebelum menulis implementasi kode.
4. **Implementasi**: Mengembangkan implementasi backend dan antarmuka web hingga seluruh pengujian test case berstatus lulus (green).
5. **Commit**: Menyimpan perubahan dengan pesan commit yang deskriptif dan terstruktur.
6. **Pull Request**: Mengajukan Pull Request (PR) ke branch `main` dengan merujuk nomor issue terkait.
7. **CI**: Memvalidasi seluruh automated tests dan coverage pada environment Continuous Integration.
8. **Merge**: Menggabungkan PR ke branch `main` setelah review dan seluruh checklist CI berhasil dilewati.
