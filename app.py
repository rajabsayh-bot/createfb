# ==============================================
# 🚀 GENERATE FB + PROXY FORMAT IP:PORT
# ✅ Baca proxy cuma angka:port
# ✅ Otomatis tambah http://
# ✅ Pilih yang paling cepat
# ✅ Email Otomatis/Manual + Input OTP
# ✅ Siap Vercel
# ==============================================
import time
import random
import requests
from flask import Flask, render_template_string, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# ==============================================
# ⚙️ KONFIGURASI
# ==============================================
URL_DAFTAR_FB = "https://m.facebook.com/r.php"
URL_TES = "https://m.facebook.com"  # Tes kecepatan

# ✅ DAFTAR USER AGENT ACAK
DAFTAR_UA = [
    "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-A525F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; POCO X3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Realme 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36"
]

# ✅ DAFTAR NAMA
DAFTAR_NAMA = [
    "Budi", "Andi", "Rizky", "Dika", "Joko", "Agus", "Hendra", "Fajar",
    "Rian", "Deni", "Eko", "Wahyu", "Bagus", "Sari", "Dewi", "Rina",
    "Lina", "Putri", "Maya", "Nina", "Ayu", "Intan", "Ratna"
]

s = requests.Session()

# ==============================================
# 📂 BACA PROXY DARI TXT + OLAH FORMAT
# ==============================================
def baca_proxy_dari_txt(nama_file="proxy.txt"):
    try:
        with open(nama_file, "r", encoding="utf-8") as f:
            baris = [b.strip() for b in f if b.strip() and not b.startswith("#")]
        
        # Otomatis tambah http:// kalau cuma ip:port
        daftar_proxy = []
        for p in baris:
            if "://" not in p:
                daftar_proxy.append(f"http://{p}")
            else:
                daftar_proxy.append(p)
        return daftar_proxy if daftar_proxy else []
    except:
        return []

# ==============================================
# ⚡ PILIH PROXY PALING CEPAT
# ==============================================
def pilih_proxy_tercepat(daftar_proxy, batas_waktu=3):
    if not daftar_proxy:
        return None, "❌ Tidak ada proxy di file"
    
    proxy_terbaik = None
    waktu_tercepat = float("inf")

    for proxy in daftar_proxy:
        try:
            mulai = time.time()
            tes = requests.get(URL_TES,
                               proxies={"http": proxy, "https": proxy},
                               timeout=batas_waktu,
                               headers={"User-Agent": random.choice(DAFTAR_UA)})
            if tes.status_code == 200:
                lama = time.time() - mulai
                if lama < waktu_tercepat:
                    waktu_tercepat = lama
                    proxy_terbaik = proxy
        except:
            continue

    if proxy_terbaik:
        return proxy_terbaik, f"✅ Pakai: {proxy_terbaik.replace('http://','')} | ⚡ {waktu_tercepat:.2f} detik"
    else:
        return None, "❌ Semua proxy mati/lelet"

# ==============================================
# 📝 BUAT DATA AKUN
# ==============================================
def buat_data(nomor, mode_email, email_manual=""):
    nama_depan = random.choice(DAFTAR_NAMA)
    nama_belakang = f"{random.choice(DAFTAR_NAMA)}{nomor:02d}"

    if mode_email == "manual" and email_manual:
        email = email_manual
    else:
        awalan = f"{random.choice(DAFTAR_NAMA).lower()}{random.randint(100,999)}{nomor}"
        domain = random.choice(["gmail.com", "outlook.com", "ymail.com", "mail.com"])
        email = f"{awalan}@{domain}"

    sandi = f"Fb{nomor:03d}{random.randint(1000,9999)}"
    hari = str(random.randint(1, 28))
    bulan = str(random.randint(1, 12))
    tahun = str(random.randint(1990, 2004))
    jk = random.choice(["M", "F"])

    return {
        "nama_depan": nama_depan,
        "nama_belakang": nama_belakang,
        "email": email,
        "sandi": sandi,
        "hari": hari,
        "bulan": bulan,
        "tahun": tahun,
        "jk": jk
    }

# ==============================================
# 📌 PROSES DAFTAR FB
# ==============================================
def daftar_fb(data, proxy=None):
    try:
        ua = random.choice(DAFTAR_UA)
        headers = {
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://m.facebook.com/",
            "Upgrade-Insecure-Requests": "1"
        }

        proxies = {"http": proxy, "https": proxy} if proxy else None

        res_awal = s.get(URL_DAFTAR_FB, headers=headers, proxies=proxies, timeout=20)
        if res_awal.status_code != 200:
            return False, "❌ Gagal akses halaman", None

        soup = BeautifulSoup(res_awal.text, "html.parser")
        lsd = soup.find("input", {"name": "lsd"})
        jazoest = soup.find("input", {"name": "jazoest"})

        form_data = {
            "lsd": lsd["value"] if lsd else "",
            "jazoest": jazoest["value"] if jazoest else "",
            "firstname": data["nama_depan"],
            "lastname": data["nama_belakang"],
            "reg_email__": data["email"],
            "reg_passwd__": data["sandi"],
            "birthday_day": data["hari"],
            "birthday_month": data["bulan"],
            "birthday_year": data["tahun"],
            "sex": data["jk"],
            "did_submit": "1",
            "locale": "id_ID",
            "nocr": "0"
        }

        res = s.post(URL_DAFTAR_FB, data=form_data, headers=headers, proxies=proxies, timeout=25, allow_redirects=True)

        if "checkpoint" in res.url or "confirm" in res.url or "verification" in res.url:
            return True, "⚠️ Terkirim → Perlu verifikasi OTP", res.url
        elif "home.php" in res.url or "profile.php" in res.url:
            return True, "✅ BERHASIL LANGSUNG AKTIF", None
        elif "reg_error" in res.text:
            return False, "❌ Gagal: Data ditolak FB", None
        else:
            return True, "✅ Data terkirim → Siap verifikasi", res.url

    except Exception as e:
        return False, f"❌ Error: {str(e)[:40]}", None

# ==============================================
# 🔐 VERIFIKASI OTP
# ==============================================
def verifikasi_otp(url_verif, kode_otp, proxy=None):
    try:
        if not url_verif or not kode_otp:
            return False, "❌ URL atau kode OTP kosong"

        ua = random.choice(DAFTAR_UA)
        headers = {"User-Agent": ua}
        proxies = {"http": proxy, "https": proxy} if proxy else None

        res = s.get(url_verif, headers=headers, proxies=proxies, timeout=20)
        soup = BeautifulSoup(res.text, "html.parser")
        lsd = soup.find("input", {"name": "lsd"})
        jazoest = soup.find("input", {"name": "jazoest"})

        verif_data = {
            "lsd": lsd["value"] if lsd else "",
            "jazoest": jazoest["value"] if jazoest else "",
            "code": kode_otp,
            "did_submit": "1"
        }

        res_verif = s.post(url_verif, data=verif_data, headers=headers, proxies=proxies, timeout=25, allow_redirects=True)

        if "home.php" in res_verif.url or "profile.php" in res_verif.url:
            return True, "✅ VERIFIKASI BERHASIL → AKUN AKTIF"
        elif "wrong" in res_verif.text.lower() or "invalid" in res_verif.text.lower():
            return False, "❌ Kode OTP salah/kadaluarsa"
        else:
            return True, "⚠️ Verifikasi diproses"

    except Exception as e:
        return False, f"❌ Error: {str(e)[:40]}"

# ==============================================
# 🌐 TAMPILAN WEB
# ==============================================
HALAMAN = """
<!DOCTYPE html><html lang="id"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FB Generator + Proxy IP:Port</title><style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial,sans-serif;}
body{background:#0f172a;color:#e2e8f0;padding:20px;}
.wadah{max-width:520px;margin:0 auto;background:#1e293b;padding:25px;border-radius:12px;box-shadow:0 0 25px rgba(0,0,0,0.3);}
h1{text-align:center;color:#1877f2;margin-bottom:25px;}
.blok{margin-bottom:22px;padding:18px;border-radius:8px;background:#334155;}
h3{margin-bottom:12px;color:#7dd3fc;}
label{display:block;margin-bottom:6px;font-weight:500;}
input, select{width:100%;padding:10px;border:0;border-radius:6px;background:#475569;color:white;margin-bottom:12px;}
button{width:100%;padding:12px;border:0;border-radius:6px;background:#1877f2;color:white;font-weight:bold;cursor:pointer;font-size:16px;}
button:hover{background:#166fe5;}
.hasil{margin-top:15px;padding:12px;border-radius:6px;background:#1e293b;min-height:80px;white-space:pre-wrap;word-break:break-all;}
</style></head><body><div class="wadah"><h1>🚀 Generator FB + Proxy</h1>

<div class="blok"><h3>⚙️ Pengaturan</h3>
<label>Jumlah Akun:</label>
<input type="number" id="jml" value="1" min="1" max="5">

<label>Pakai Email:</label>
<select id="mode_email" onchange="cekMode()">
    <option value="otomatis">Buat Otomatis</option>
    <option value="manual">Masukkan Sendiri</option>
</select>

<div id="kolom_email" style="display:none;">
    <label>Email Kamu:</label>
    <input type="email" id="email_manual" placeholder="contoh: aku@gmail.com">
</div>

<button onclick="prosesDaftar()">Mulai Buat Akun</button>
<div id="hasilDaftar" class="hasil"></div>
</div>

<div class="blok"><h3>🔐 Verifikasi OTP</h3>
<label>URL Verifikasi:</label>
<input type="text" id="url_verif" placeholder="Muncul setelah daftar">
<label>Kode OTP:</label>
<input type="text" id="kode_otp" placeholder="Masukkan kode dari email">
<button onclick="prosesVerif()">Kirim Kode OTP</button>
<div id="hasilVerif" class="hasil"></div>
</div>

</div><script>
function cekMode(){
    document.getElementById('kolom_email').style.display = document.getElementById('mode_email').value === "manual" ? "block" : "none";
}

async function prosesDaftar(){
    document.getElementById('hasilDaftar').textContent = '⏳ Membaca proxy & pilih yang tercepat...';
    let jml = document.getElementById('jml').value;
    let mode = document.getElementById('mode_email').value;
    let email = document.getElementById('email_manual').value;

    let res = await fetch('/api/daftar-fb', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({jumlah:jml, mode_email:mode, email:email})
    });
    let data = await res.json();
    document.getElementById('hasilDaftar').textContent = data.pesan;
    if(data.url_verif) document.getElementById('url_verif').value = data.url_verif;
}

async function prosesVerif(){
    let url = document.getElementById('url_verif').value;
    let kode = document.getElementById('kode_otp').value;
    if(!url || !kode) {
        document.getElementById('hasilVerif').textContent = '❌ Isi dulu URL dan OTP';
        return;
    }
    document.getElementById('hasilVerif').textContent = '⏳ Memverifikasi...';
    let res = await fetch('/api/verifikasi-otp', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({url_verif:url, kode_otp:kode})
    });
    let data = await res.json();
    document.getElementById('hasilVerif').textContent = data.pesan;
}
</script></body></html>
"""

# ==============================================
# 🛣️ RUTE API
# ==============================================
@app.route('/')
def utama():
    return render_template_string(HALAMAN)

@app.route('/api/daftar-fb', methods=['POST'])
def api_daftar_fb():
    data = request.get_json()
    jml = int(data.get("jumlah", 1))
    mode = data.get("mode_email", "otomatis")
    email_manual = data.get("email", "")

    daftar_proxy = baca_proxy_dari_txt()
    if not daftar_proxy:
        return jsonify({"sukses": False, "pesan": "❌ File proxy.txt kosong atau tidak ada"})

    proxy, info_proxy = pilih_proxy_tercepat(daftar_proxy)
    if not proxy:
        return jsonify({"sukses": False, "pesan": info_proxy})

    pesan = f"🔧 {info_proxy}\n\n📋 HASIL GENERATE:\n\n"
    url_verif_terakhir = None

    for i in range(1, jml+1):
        akun = buat_data(i, mode, email_manual)
        sukses, status, url_verif = daftar_fb(akun, proxy)
        pesan += f"👤 {akun['nama_depan']} {akun['nama_belakang']}\n📧 {akun['email']}\n🔑 {akun['sandi']}\n📊 {status}\n──────────────────\n"
        if url_verif:
            url_verif_terakhir = url_verif
        time.sleep(2)

    return jsonify({"sukses": True, "pesan": pesan, "url_verif": url_verif_terakhir})

@app.route('/api/verifikasi-otp', methods=['POST'])
def api_verifikasi_otp():
    data = request.get_json()
    url = data.get("url_verif", "")
    kode = data.get("kode_otp", "")
    daftar_proxy = baca_proxy_dari_txt()
    proxy, _ = pilih_proxy_tercepat(daftar_proxy) if daftar_proxy else (None, "")
    sukses, pesan = verifikasi_otp(url, kode, proxy)
    return jsonify({"sukses": sukses, "pesan": pesan})

wsgi_app = app
