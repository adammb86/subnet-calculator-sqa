from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse

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
