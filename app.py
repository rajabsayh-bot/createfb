# ==============================================
# 🚀 FB GENERATOR - BUATAN UCUK
# ✅ Tampilan mirip aplikasi HP
# ✅ Bisa atur jumlah akun
# ✅ Ada status sukses/gagal
# ✅ Proxy cepat + TempMail TM
# ✅ Siap di Vercel
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
BATAS_WAKTU_PROXY = 1.5
JUMLAH_PER_KELOMPOK = 30
MAKS_WAKTU_TOTAL = 12

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
    mulai = time.time()
    for i in range(0, total, JUMLAH_PER_KELOMPOK):
        if time.time() - mulai > MAKS_WAKTU_TOTAL - 4:
            return None, "⏱️ Waktu habis, coba proxy lebih cepat"
        kelompok = daftar_proxy[i : i+JUMLAH_PER_KELOMPOK]
        for proxy in kelompok:
            try:
                r = requests.get(URL_TES_PROXY, proxies={"http": proxy, "https": proxy}, headers=HEADERS, timeout=BATAS_WAKTU_PROXY)
                if r.status_code == 200:
                    return proxy, f"✅ {proxy.replace('http://','')}"
            except:
                continue
    return None, "❌ Tidak ada proxy aktif"

# ==================== FUNGSI TEMPMAIL ====================
def buat_email_tm():
    try:
        res = requests.get(f"{API_TM}/mail/id/1/format/json", headers=HEADERS, timeout=5)
        if res.status_code == 200:
            return True, res.json()["mail"]
        return False, "❌ Gagal buat email"
    except:
        return False, "❌ Koneksi ke TM gagal"

def cek_otp(email):
    try:
        res = requests.get(f"{API_TM}/messages/mail/{email}/format/json", headers=HEADERS, timeout=4)
        if res.status_code == 200 and res.json():
            msg = res.json()[0]
            baca = requests.get(f"{API_TM}/read/mail/{email}/id/{msg['id']}/format/json", headers=HEADERS, timeout=4)
            if baca.status_code == 200:
                isi = baca.json().get("mail_body", "")
                kode = re.search(r"\b\d{5,6}\b", isi)
                return kode.group() if kode else "Tidak ada"
        return "Belum masuk"
    except:
        return "Gagal cek"

# ==================== FUNGSI DAFTAR FB ====================
def buat_data():
    return {
        "nama_depan": random.choice(DAFTAR_NAMA),
        "nama_belakang": f"{random.choice(DAFTAR_NAMA)}{random.randint(10,99)}",
        "sandi": f"Fb{random.randint(10000,99999)}",
        "hari": str(random.randint(1,28)),
        "bulan": str(random.randint(1,12)),
        "tahun": str(random.randint(1990,2004)),
        "jk": random.choice(["M","F"])
    }

def daftar_fb(data, proxy, email):
    try:
        proxies = {"http": proxy, "https": proxy}
        res = s.get(URL_DAFTAR_FB, headers=HEADERS, proxies=proxies, timeout=8)
        if res.status_code != 200:
            return False, "❌ Gagal akses halaman"
        soup = BeautifulSoup(res.text, "html.parser")
        lsd = soup.find("input", {"name":"lsd"})
        jazoest = soup.find("input", {"name":"jazoest"})
        form = {
            "lsd": lsd["value"] if lsd else "",
            "jazoest": jazoest["value"] if jazoest else "",
            "firstname": data["nama_depan"],
            "lastname": data["nama_belakang"],
            "reg_email__": email,
            "reg_passwd__": data["sandi"],
            "birthday_day": data["hari"],
            "birthday_month": data["bulan"],
            "birthday_year": data["tahun"],
            "sex": data["jk"],
            "did_submit": "1",
            "locale": "id_ID"
        }
        res_post = s.post(URL_DAFTAR_FB, data=form, headers=HEADERS, proxies=proxies, timeout=10, allow_redirects=True)
        if "home.php" in res_post.url:
            return True, "✅ Berhasil Langsung Aktif"
        elif "checkpoint" in res_post.url or "confirm" in res_post.url:
            return True, "⚠️ Butuh Verifikasi OTP"
        else:
            return True, "✅ Data Terkirim"
    except Exception as e:
        return False, f"❌ Error: {str(e)[:30]}"

# ==================== TAMPILAN APLIKASI ====================
@app.route("/")
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Create FB By Ucuk</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            * { -webkit-tap-highlight-color: transparent; }
            body { font-family: 'Segoe UI', Roboto, sans-serif; }
            pre { white-space: pre-wrap; word-wrap: break-word; }
        </style>
    </head>
    <body class="bg-gray-100 min-h-screen p-3">
        <div class="max-w-md mx-auto bg-white rounded-2xl shadow-xl overflow-hidden">
            
            <!-- HEADER -->
            <div class="bg-gradient-to-r from-blue-600 to-indigo-600 p-5 text-center">
                <h1 class="text-2xl font-bold text-white">📱 Create FB</h1>
                <p class="text-blue-100 text-sm">By Ucuk</p>
            </div>

            <!-- ISI -->
            <div class="p-5 space-y-5">
                
                <!-- JUMLAH AKUN -->
                <div>
                    <label class="block text-gray-700 font-medium mb-2">Jumlah Akun:</label>
                    <input type="number" id="jumlah" value="1" min="1" max="10" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-lg">
                </div>

                <!-- TOMBOL RUN -->
                <button id="tombolRun" onclick="mulaiProses()" class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3.5 rounded-lg text-lg shadow-md transition duration-200">
                    ▶️ RUN Pembuatan
                </button>

                <!-- KOLOM HASIL -->
                <div>
                    <h3 class="font-semibold text-gray-800 mb-2">📋 Hasil Proses:</h3>
                    <div id="kolomHasil" class="bg-gray-50 border border-gray-200 rounded-lg p-4 min-h-[220px] text-sm overflow-y-auto">
                        Siap digunakan...<br>
                        Masukkan jumlah akun lalu tekan RUN
                    </div>
                </div>

            </div>

            <!-- FOOTER -->
            <div class="text-center text-xs text-gray-500 p-3 border-t">
                Versi Vercel • Proxy + TempMail
            </div>
        </div>

        <script>
            async function mulaiProses() {
                const tombol = document.getElementById("tombolRun");
                const hasil = document.getElementById("kolomHasil");
                const jumlah = parseInt(document.getElementById("jumlah").value) || 1;

                tombol.disabled = true;
                tombol.textContent = "⏳ Sedang Memproses...";
                hasil.innerHTML = `🔄 Memulai pembuatan ${jumlah} akun...<br><br>`;

                for (let i = 1; i <= jumlah; i++) {
                    hasil.innerHTML += `🔹 Memproses Akun ke-${i}...<br>`;
                    try {
                        const res = await fetch(`/buat?nomor=${i}`);
                        const data = await res.json();
                        if (data.status === "berhasil") {
                            hasil.innerHTML += `<div class="text-green-700 bg-green-50 p-2 rounded my-1">
                                ✅ SUKSES<br>
                                📧 Email: ${data.email}<br>
                                🔑 Sandi: ${data.sandi}<br>
                                🌐 Proxy: ${data.proxy}<br>
                                📊 Status: ${data.ket}<br>
                                ${data.otp ? `🔢 OTP: ${data.otp}<br>` : ''}
                            </div>`;
                        } else {
                            hasil.innerHTML += `<div class="text-red-700 bg-red-50 p-2 rounded my-1">
                                ❌ GAGAL<br>
                                ${data.pesan}
                            </div>`;
                        }
                    } catch (err) {
                        hasil.innerHTML += `<div class="text-red-600">❌ Gagal terhubung ke server</div>`;
                    }
                    hasil.scrollTop = hasil.scrollHeight;
                }

                tombol.disabled = false;
                tombol.textContent = "▶️ RUN Pembuatan";
                hasil.innerHTML += `<br>✅ Selesai semua!`;
            }
        </script>
    </body>
    </html>
    """)

@app.route("/buat")
def buat_satu():
    daftar_proxy = baca_proxy_dari_txt()
    if not daftar_proxy:
        return jsonify({"status": "gagal", "pesan": "File proxy.txt kosong/tidak ada"})
    
    proxy, info_proxy = cari_proxy_valid(daftar_proxy)
    if not proxy:
        return jsonify({"status": "gagal", "pesan": info_proxy})
    
    ok_email, email = buat_email_tm()
    if not ok_email:
        return jsonify({"status": "gagal", "pesan": email})
    
    data_akun = buat_data()
    sukses, keterangan = daftar_fb(data_akun, proxy, email)
    
    otp = ""
    if "verifikasi" in keterangan.lower():
        time.sleep(3)
        otp = cek_otp(email)
    
    return jsonify({
        "status": "berhasil" if sukses else "gagal",
        "pesan": "",
        "proxy": info_proxy,
        "email": email,
        "sandi": data_akun["sandi"],
        "ket": keterangan,
        "otp": otp
    })

if __name__ == "__main__":
    app.run(debug=False)
