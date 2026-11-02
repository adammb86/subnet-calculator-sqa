from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse

from pydantic import BaseModel

app = FastAPI()


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


def int_to_ip(val: int) -> str:
    return f"{(val >> 24) & 0xFF}.{(val >> 16) & 0xFF}.{(val >> 8) & 0xFF}.{val & 0xFF}"


def hitung_subnet(ip: str, prefix: int) -> dict:
    if not isinstance(ip, str):
        raise ValueError("IP harus berupa string")

    if " " in ip:
        raise ValueError("IP tidak boleh mengandung spasi")

    parts = ip.split(".")
    if len(parts) != 4:
        raise ValueError("Format IPv4 harus terdiri dari tepat 4 oktet")

    octets = []
    for part in parts:
        if not part.isdigit():
            raise ValueError(f"Oktet '{part}' tidak valid (hanya karakter angka yang diizinkan)")
        if len(part) > 1 and part.startswith("0"):
            raise ValueError(f"Oktet '{part}' tidak boleh memiliki leading zero")
        val = int(part)
        if not (0 <= val <= 255):
            raise ValueError(f"Nilai oktet {val} di luar rentang (0-255)")
        octets.append(val)

    if not isinstance(prefix, int) or isinstance(prefix, bool):
        raise ValueError("Prefix harus berupa bilangan bulat (integer)")

    if prefix < 0 or prefix > 32:
        raise ValueError(f"Prefix {prefix} tidak valid (rentang valid: 0-32)")

    ip_int = (octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | octets[3]
    mask_int = ((0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF) if prefix > 0 else 0

    network_int = ip_int & mask_int
    broadcast_int = network_int | (~mask_int & 0xFFFFFFFF)

    mask_str = int_to_ip(mask_int)
    network_str = int_to_ip(network_int)

    if prefix == 32:
        usable_hosts = 1
        broadcast_str = None
        first_host_str = network_str
        last_host_str = network_str
    elif prefix == 31:
        usable_hosts = 2
        broadcast_str = None
        first_host_str = network_str
        last_host_str = int_to_ip(network_int + 1)
    else:
        usable_hosts = (1 << (32 - prefix)) - 2
        broadcast_str = int_to_ip(broadcast_int)
        first_host_str = int_to_ip(network_int + 1)
        last_host_str = int_to_ip(broadcast_int - 1)

    return {
        "mask": mask_str,
        "network": network_str,
        "broadcast": broadcast_str,
        "first_host": first_host_str,
        "last_host": last_host_str,
        "usable_hosts": usable_hosts,
    }


@app.get("/")
def get_root():
    return FileResponse("index.html")


@app.get("/api/subnet")
def get_subnet(ip: str = Query(...), prefix: int = Query(...)):
    return hitung_subnet(ip, prefix)


class VLSMRequest(BaseModel):
    network: str
    kebutuhan_host: list[int]


def alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]:
    if not isinstance(network_cidr, str) or "/" not in network_cidr:
        raise ValueError("Format network_cidr harus berupa string dengan format IP/Prefix (contoh: 192.168.1.0/24)")

    parts = network_cidr.split("/")
    if len(parts) != 2:
        raise ValueError("Format network_cidr tidak valid")

    ip_str, prefix_str = parts[0].strip(), parts[1].strip()
    if not prefix_str.isdigit():
        raise ValueError("Prefix harus berupa bilangan bulat")

    parent_prefix = int(prefix_str)
    # Validasi IP dan Prefix menggunakan hitung_subnet
    parent_subnet = hitung_subnet(ip_str, parent_prefix)

    # Validasi apakah alamat IP yang diberikan memang merupakan alamat network awal
    if ip_str != parent_subnet["network"]:
        raise ValueError(f"Alamat '{ip_str}' bukan alamat network yang valid untuk prefix /{parent_prefix} (seharusnya '{parent_subnet['network']}')")

    if not isinstance(kebutuhan_host, list) or len(kebutuhan_host) == 0:
        raise ValueError("Daftar kebutuhan_host tidak boleh kosong")

    for req in kebutuhan_host:
        if not isinstance(req, int) or isinstance(req, bool) or req < 1:
            raise ValueError("Setiap nilai dalam kebutuhan_host harus berupa integer positif (>= 1)")

    # Urutkan elemen kebutuhan_host secara descending
    sorted_kebutuhan = sorted(kebutuhan_host, reverse=True)

    parent_octets = [int(p) for p in parent_subnet["network"].split(".")]
    parent_ip_int = (parent_octets[0] << 24) | (parent_octets[1] << 16) | (parent_octets[2] << 8) | parent_octets[3]
    parent_capacity = (1 << (32 - parent_prefix)) if parent_prefix < 32 else 1
    parent_end_int = parent_ip_int + parent_capacity

    current_ip_int = parent_ip_int
    allocations = []

    for req in sorted_kebutuhan:
        needed = req + 2
        block_size = 1
        while block_size < needed:
            block_size <<= 1
        # Alokasi minimum untuk VLSM adalah prefix /30 (kapasitas 2 host, block size 4)
        if block_size < 4:
            block_size = 4

        h_bits = block_size.bit_length() - 1
        sub_prefix = 32 - h_bits

        if current_ip_int + block_size > parent_end_int:
            raise ValueError(f"Kapasitas blok IP induk {network_cidr} tidak mencukupi untuk menampung seluruh alokasi kebutuhan host")

        sub_ip_str = int_to_ip(current_ip_int)
        sub_detail = hitung_subnet(sub_ip_str, sub_prefix)

        allocations.append({
            "kebutuhan": req,
            "network_cidr": f"{sub_ip_str}/{sub_prefix}",
            **sub_detail,
        })

        current_ip_int += block_size

    return allocations


@app.post("/api/vlsm")
def post_vlsm(payload: VLSMRequest):
    return alokasi_vlsm(payload.network, payload.kebutuhan_host)
