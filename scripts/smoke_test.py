"""Smoke test (smoke test) untuk Kalkulator Subnet & VLSM yang sudah berjalan.

Pemakaian:
    uv run python scripts/smoke_test.py <URL dasar>
Contoh:
    uv run python scripts/smoke_test.py http://127.0.0.1:8000

Keluar dengan kode 0 bila semua pemeriksaan lulus, 1 bila ada yang gagal.
Kesalahan sementara (server belum siap atau cold start) dicoba ulang beberapa kali.
"""

import http.client
import json
import os
import sys
import time
import urllib.error
import urllib.request

PERCOBAAN = int(os.environ.get("SMOKE_PERCOBAAN", "6"))
JEDA_DETIK = int(os.environ.get("SMOKE_JEDA", "15"))


def minta(base, path, metode="GET", isi=None):
    url = base.rstrip("/") + path
    data = None
    header = {}
    if isi is not None:
        data = json.dumps(isi).encode("utf-8")
        header["Content-Type"] = "application/json"
    terakhir = (0, "")
    for percobaan in range(1, PERCOBAAN + 1):
        try:
            req = urllib.request.Request(url, data=data, headers=header, method=metode)
            with urllib.request.urlopen(req, timeout=10) as resp:
                isi_resp = resp.read().decode("utf-8")
                return resp.status, isi_resp
        except urllib.error.HTTPError as exc:
            isi_resp = exc.read().decode("utf-8") if exc.fp else ""
            terakhir = (exc.code, isi_resp)
            if exc.code < 500:
                return exc.code, isi_resp
            print(f"  [percobaan {percobaan}/{PERCOBAAN}] HTTP {exc.code} — coba lagi …", file=sys.stderr)
        except (urllib.error.URLError, http.client.RemoteDisconnected, ConnectionResetError) as exc:
            terakhir = (0, str(exc))
            print(f"  [percobaan {percobaan}/{PERCOBAAN}] {exc} — coba lagi dalam {JEDA_DETIK}d …", file=sys.stderr)
        time.sleep(JEDA_DETIK)
    return terakhir


def periksa(nama, status_aktual, status_harapan, tubuh="", cek_kunci=None):
    ok = status_aktual == status_harapan
    if ok and cek_kunci:
        try:
            data = json.loads(tubuh)
            for k, v in cek_kunci.items():
                if data.get(k) != v:
                    ok = False
                    break
        except (json.JSONDecodeError, AttributeError):
            ok = False
    simbol = "✓" if ok else "✗"
    print(f"  {simbol} {nama}  [HTTP {status_aktual}]")
    return ok


def main():
    if len(sys.argv) < 2:
        print("Pemakaian: smoke_test.py <URL dasar>", file=sys.stderr)
        sys.exit(1)

    base = sys.argv[1]
    print(f"\nSmoke test → {base}\n")
    hasil = []

    # 1. Halaman utama
    status, tubuh = minta(base, "/")
    hasil.append(periksa("GET /  → 200", status, 200))

    # 2. API subnet normal
    status, tubuh = minta(base, "/api/subnet?ip=192.168.1.0&prefix=24")
    hasil.append(periksa(
        "GET /api/subnet?ip=192.168.1.0&prefix=24  → 200",
        status, 200, tubuh,
        cek_kunci={"network": "192.168.1.0", "broadcast": "192.168.1.255"},
    ))

    # 3. API subnet — input tidak valid
    status, tubuh = minta(base, "/api/subnet?ip=999.999.999.999&prefix=24")
    hasil.append(periksa("GET /api/subnet (IP tidak valid) → 400", status, 400))

    # 4. API VLSM
    status, tubuh = minta(
        base, "/api/vlsm",
        metode="POST",
        isi={"network": "192.168.1.0/24", "kebutuhan_host": [50]},
    )
    hasil.append(periksa("POST /api/vlsm  → 200", status, 200))

    gagal = hasil.count(False)
    total = len(hasil)
    print(f"\n{total - gagal}/{total} pemeriksaan lulus.\n")
    sys.exit(0 if gagal == 0 else 1)


if __name__ == "__main__":
    main()

