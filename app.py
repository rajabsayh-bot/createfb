# ==============================================
# 🚀 FB GENERATOR + PROXY CEPAT + TEMPMAIL TM
# ✅ Cek 50 proxy per kelompok | Batas 1-2 detik
# ✅ Langsung pakai yang valid
# ✅ Temp-Mail.org: Tanpa daftar/token
# ✅ Siap Deploy ke Vercel
# ==============================================
import time
import random
import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# ==================== KONFIGURASI ====================
URL_DAFTAR_FB = "https://m.facebook.com/r.php"
URL_TES_PROXY = "https://m.facebook.com"
BATAS_WAKTU_PROXY = 2  # detik
JUMLAH_PER_KELOMPOK = 50

# API Temp-Mail.org
API_TM = "https://api.temp-mail.org/request"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-G991B) Chrome/126.0.0.0 Mobile Safari/537.36",
    "Accept": "text/html,application/json,*/*",
    "Accept-Language": "id-ID,id;q=0.9"
}

DAFTAR_NAMA = ["Budi","Andi","Rizky","Dika","Joko","Agus","Hendra","Fajar","Rian","Deni","Sari","Dewi"]
s = requests.Session()

# ==================== FUNGSI PROXY ====================
def baca_proxy_dari_txt(nama_file="proxy.txt"):
    try:
        with open(nama_file, "r", encoding="utf-8") as f:
            baris = [b.strip() for b in f if b.strip() and not b.startswith("#")]
        daftar = []
        for p in baris:
            if "://" not in p:
                daftar.append(f"http://{p}")
            else:
                daftar.append(p)
        return daftar
    except:
        return []

def cari_proxy_valid(daftar_proxy):
    if not daftar_proxy:
        return None, "❌ File proxy kosong"
    total = len(daftar_proxy)
    for i in range(0, total, JUMLAH_PER_KELOMPOK):
        kelompok = daftar_proxy[i : i+JUMLAH_PER_KELOMPOK]
        for proxy in kelompok:
            try:
                mulai = time.time()
                r = requests.get(
                    URL_TES_PROXY,
                    proxies={"http": proxy, "https": proxy},
                    headers=HEADERS,
                    timeout=BATAS_WAKTU_PROXY
                )
                if r.status_code == 200:
                    lama = round(time.time() - mulai, 2)
                    return proxy, f"✅ Pakai: {proxy.replace('http://','')} | ⚡ {lama} detik"
            except:
                continue
    return None, "❌ Tidak ada proxy yang valid"

# ==================== FUNGSI TEMPMAIL TM ====================
def buat_email_tm():
    try:
        res = requests.get(f"{API_TM}/mail/id/1/format/json", headers=HEADERS, timeout=10)
        if res.status_code == 200:
            data = res.json()
            email = data["mail"]
            return True, {"email": email, "login": email.split("@")[0], "domain": email.split("@")[1]}
        return False, "❌ Gagal buat email"
    except:
        return False, "❌ Error koneksi ke TM"

def cek_inbox_tm(email):
    try:
        res = requests.get(f"{API_TM}/messages/mail/{email}/format/json", headers=HEADERS, timeout=8)
        if res.status_code == 200:
            return True, res.json()
        return False, []
    except:
        return False, []

def baca_otp_tm(email, pesan_id):
    try:
        res = requests.get(f"{API_TM}/read/mail/{email}/id/{pesan_id}/format/json", headers=HEADERS, timeout=8)
        if res.status_code == 200:
            isi = res.json().get("mail_body", "")
            otp = re.search(r"\b\d{5,6}\b", isi)
            return otp.group() if otp else None
        return None
    except:
        return None

# ==================== FUNGSI DAFTAR FB ====================
def buat_data_akun(nomor, email):
    return {
        "nama_depan": random.choice(DAFTAR_NAMA),
        "nama_belakang": f"{random.choice(DAFTAR_NAMA)}{nomor}",
        "email": email,
        "sandi": f"Fb{random.randint(10000,99999)}",
        "hari": str(random.randint(1,28)),
        "bulan": str(random.randint(1,12)),
        "tahun": str(random.randint(1990,2004)),
        "jk": random.choice(["M","F"])
    }

def daftar_fb(data, proxy):
    try:
        proxies = {"http": proxy, "https": proxy} if proxy else None
        res = s.get(URL_DAFTAR_FB, headers=HEADERS, proxies=proxies, timeout=15)
        if res.status_code != 200:
            return False, "❌ Gagal akses halaman", None

        soup = BeautifulSoup(res.text, "html.parser")
        lsd = soup.find("input", {"name":"lsd"})
        jazoest = soup.find("input", {"name":"jazoest"})

        form = {
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
            "locale": "id_ID"
        }

        res_post = s.post(URL_DAFTAR_FB, data=form, headers=HEADERS, proxies=proxies, timeout=20, allow_redirects=True)

        if "checkpoint" in res_post.url or "confirm" in res_post.url:
            return True, "⚠️ Butuh verifikasi OTP", res_post.url
        elif "home.php" in res_post.url:
            return True, "✅ Berhasil langsung aktif", None
        else:
            return True, "✅ Data terkirim, tunggu OTP", None

    except Exception as e:
        return False, f"❌ Error: {str(e)[:50]}", None

# ==================== ROUTE UNTUK VERCEL ====================
@app.route("/")
def index():
    return render_template_string("""
    <h2>🚀 FB Generator + Proxy + TempMail</h2>
    <p>Klik tombol di bawah untuk mulai proses:</p>
    <button onclick="mulai()">Mulai Buat Akun</button>
    <pre id="hasil"></pre>
    <script>
    async function mulai() {
        document.getElementById("hasil").textContent = "⏳ Memproses...";
        const res = await fetch("/jalankan");
        const data = await res.json();
        document.getElementById("hasil").textContent = JSON.stringify(data, null, 2);
    }
    </script>
    """)

@app.route("/jalankan")
def jalankan():
    daftar_proxy = baca_proxy_dari_txt()
    if not daftar_proxy:
        return jsonify({"status": "gagal", "pesan": "File proxy.txt tidak ada atau kosong"})

    proxy, info_proxy = cari_proxy_valid(daftar_proxy)
    if not proxy:
        return jsonify({"status": "gagal", "pesan": info_proxy})

    ok_email, data_email = buat_email_tm()
    if not ok_email:
        return jsonify({"status": "gagal", "pesan": data_email})

    data_akun = buat_data_akun(random.randint(100,999), data_email["email"])
    sukses, status, url_verif = daftar_fb(data_akun, proxy)

    hasil = {
        "status": "berhasil" if sukses else "gagal",
        "info_proxy": info_proxy,
        "email": data_email["email"],
        "sandi": data_akun["sandi"],
        "status_daftar": status
    }

    if "verifikasi" in status.lower():
        hasil["otp"] = "⏳ Sedang cek kode masuk..."
        for _ in range(6):
            time.sleep(5)
            ok, pesan = cek_inbox_tm(data_email["email"])
            if ok and pesan:
                kode = baca_otp_tm(data_email["email"], pesan[0]["id"])
                hasil["otp"] = kode if kode else "Tidak ditemukan"
                break

    return jsonify(hasil)

if __name__ == "__main__":
    app.run(debug=False)
