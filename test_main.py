import pytest
from fastapi.testclient import TestClient

from main import alokasi_vlsm, app, hitung_subnet

client = TestClient(app)

# ==============================================================================
# Test Data: Subnet Cases (SPEC.md TC01 - TC11)
# ==============================================================================

VALID_SUBNET_CASES = [
    # TC01: Subnet Normal
    (
        "172.16.5.130",
        25,
        {
            "mask": "255.255.255.128",
            "network": "172.16.5.128",
            "broadcast": "172.16.5.255",
            "first_host": "172.16.5.129",
            "last_host": "172.16.5.254",
            "usable_hosts": 126,
        },
    ),
    # TC02: Subnet Minim
    (
        "10.0.0.0",
        30,
        {
            "mask": "255.255.255.252",
            "network": "10.0.0.0",
            "broadcast": "10.0.0.3",
            "first_host": "10.0.0.1",
            "last_host": "10.0.0.2",
            "usable_hosts": 2,
        },
    ),
    # TC03: Subnet RFC 3021
    (
        "192.168.1.0",
        31,
        {
            "mask": "255.255.255.254",
            "network": "192.168.1.0",
            "broadcast": None,
            "first_host": "192.168.1.0",
            "last_host": "192.168.1.1",
            "usable_hosts": 2,
        },
    ),
    # TC04: Subnet Host Route
    (
        "192.168.1.5",
        32,
        {
            "mask": "255.255.255.255",
            "network": "192.168.1.5",
            "broadcast": None,
            "first_host": "192.168.1.5",
            "last_host": "192.168.1.5",
            "usable_hosts": 1,
        },
    ),
]

INVALID_SUBNET_CASES = [
    # TC05: Validasi Oktet
    ("256.1.1.1", 24),
    # TC06: Validasi Leading Zero
    ("192.168.01.1", 24),
    # TC07: Validasi Format Kurang
    ("192.168.1", 24),
    # TC08: Validasi Tipe Karakter
    ("abc", 24),
    # TC09: Validasi Data Kosong
    ("", 24),
    # TC10: Validasi Prefix Atas
    ("192.168.1.1", 33),
    # TC11: Validasi Prefix Bawah
    ("10.0.0.1", -1),
]


# ==============================================================================
# Unit Tests: hitung_subnet
# ==============================================================================


@pytest.mark.parametrize("ip,prefix,expected", VALID_SUBNET_CASES)
def test_hitung_subnet_valid(ip, prefix, expected):
    result = hitung_subnet(ip, prefix)
    assert result == expected


@pytest.mark.parametrize("ip,prefix", INVALID_SUBNET_CASES)
def test_hitung_subnet_invalid(ip, prefix):
    with pytest.raises(ValueError):
        hitung_subnet(ip, prefix)


# ==============================================================================
# Integration Tests: FastAPI Endpoints
# ==============================================================================


def test_get_root():
    """GET / harus mengembalikan status code 200 dan menyajikan index.html."""
    response = client.get("/")
    assert response.status_code == 200
    assert "html" in response.headers.get("content-type", "").lower()


@pytest.mark.parametrize("ip,prefix,expected", VALID_SUBNET_CASES)
def test_api_subnet_success(ip, prefix, expected):
    """GET /api/subnet dengan parameter valid harus mengembalikan 200 dan data kalkulasi."""
    response = client.get(f"/api/subnet?ip={ip}&prefix={prefix}")
    assert response.status_code == 200
    assert response.json() == expected


@pytest.mark.parametrize("ip,prefix", INVALID_SUBNET_CASES)
def test_api_subnet_invalid(ip, prefix):
    """GET /api/subnet dengan parameter tidak valid harus mengembalikan status 400."""
    response = client.get(f"/api/subnet?ip={ip}&prefix={prefix}")
    assert response.status_code == 400
    assert "detail" in response.json()


# ==============================================================================
# Test Data: VLSM Cases (SPEC.md TC12 - TC13 and Validations)
# ==============================================================================

TC12_EXPECTED = [
    {
        "kebutuhan": 100,
        "network_cidr": "192.168.1.0/25",
        "network": "192.168.1.0",
        "mask": "255.255.255.128",
        "broadcast": "192.168.1.127",
        "first_host": "192.168.1.1",
        "last_host": "192.168.1.126",
        "usable_hosts": 126,
    },
    {
        "kebutuhan": 50,
        "network_cidr": "192.168.1.128/26",
        "network": "192.168.1.128",
        "mask": "255.255.255.192",
        "broadcast": "192.168.1.191",
        "first_host": "192.168.1.129",
        "last_host": "192.168.1.190",
        "usable_hosts": 62,
    },
    {
        "kebutuhan": 20,
        "network_cidr": "192.168.1.192/27",
        "network": "192.168.1.192",
        "mask": "255.255.255.224",
        "broadcast": "192.168.1.223",
        "first_host": "192.168.1.193",
        "last_host": "192.168.1.222",
        "usable_hosts": 30,
    },
    {
        "kebutuhan": 2,
        "network_cidr": "192.168.1.224/30",
        "network": "192.168.1.224",
        "mask": "255.255.255.252",
        "broadcast": "192.168.1.227",
        "first_host": "192.168.1.225",
        "last_host": "192.168.1.226",
        "usable_hosts": 2,
    },
]

INVALID_VLSM_CASES = [
    # TC13: Kapasitas Gagal
    ("192.168.1.0/24", [200, 100]),
    # Network bukan alamat network yang valid (host bit bukan 0)
    ("192.168.1.5/24", [50]),
    # Format network_cidr salah (tanpa prefix)
    ("192.168.1.0", [50]),
    # Kebutuhan host kosong
    ("192.168.1.0/24", []),
    # Nilai kebutuhan host < 1 (nol)
    ("192.168.1.0/24", [50, 0]),
    # Nilai kebutuhan host < 1 (negatif)
    ("192.168.1.0/24", [50, -5]),
]


# ==============================================================================
# Unit Tests: alokasi_vlsm
# ==============================================================================


def test_alokasi_vlsm_success():
    """TC12: Alokasi VLSM berhasil secara berurutan dan terurut descending."""
    result = alokasi_vlsm("192.168.1.0/24", [100, 50, 20, 2])
    assert result == TC12_EXPECTED


def test_alokasi_vlsm_auto_sort_descending():
    """TC12: Input tidak berurutan harus otomatis diurutkan descending."""
    result = alokasi_vlsm("192.168.1.0/24", [20, 100, 2, 50])
    assert result == TC12_EXPECTED


@pytest.mark.parametrize("network_cidr,kebutuhan", INVALID_VLSM_CASES)
def test_alokasi_vlsm_invalid(network_cidr, kebutuhan):
    """TC13 dan validasi input VLSM harus memicu ValueError."""
    with pytest.raises(ValueError):
        alokasi_vlsm(network_cidr, kebutuhan)


# ==============================================================================
# Integration Tests: POST /api/vlsm
# ==============================================================================


def test_api_vlsm_success():
    """POST /api/vlsm dengan payload valid harus mengembalikan status 200 dan daftar alokasi."""
    response = client.post(
        "/api/vlsm",
        json={"network": "192.168.1.0/24", "kebutuhan_host": [100, 50, 20, 2]},
    )
    assert response.status_code == 200
    assert response.json() == TC12_EXPECTED


@pytest.mark.parametrize("network_cidr,kebutuhan", INVALID_VLSM_CASES)
def test_api_vlsm_invalid(network_cidr, kebutuhan):
    """POST /api/vlsm dengan payload tidak valid / overload harus mengembalikan status 400."""
    response = client.post(
        "/api/vlsm", json={"network": network_cidr, "kebutuhan_host": kebutuhan}
    )
    assert response.status_code == 400
    assert "detail" in response.json()
