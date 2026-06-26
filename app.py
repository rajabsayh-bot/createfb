# ==============================================
# 🚀 CREATE FB BY UCUK - TANPA PROXY
# ✅ Khusus Testing di Vercel
# ✅ Pakai 1secmail.com (Lebih Stabil)
# ✅ Tampilan Aplikasi HP + Simulasi Proses
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

# API 1secmail.com (Lebih stabil untuk Vercel)
API_1SEC = "https://www.1secmail.com/api/v1/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-G991B) Chrome/126.0.0.0 Mobile Safari/537.36",
    "Accept": "text/html,application/json,*/*",
    "Accept-Language": "id-ID,id;q=0.9"
}

DAFTAR_NAMA = ["Budi","Andi","Rizky","Dika","Joko","Agus","Hendra","Fajar","Rian","Deni","Sari","Dewi","Lina","Rina"]
s = requests.Session()

# ==================== FUNGSI EMAIL (1SECMAIL) ====================
def buat_email():
    try:
        # Ambil domain acak
        res = requests.get(f"{API_1SEC}?action=getDomainList", timeout=5)
        if res.status_code != 200:
            return False, "❌ Gagal dapat domain email"
        domain = random.choice(res.json())
        nama = f"ucuk{random.randint(10000,99999)}"
        email = f"{nama}@{domain}"
        return True, {"email": email, "login": nama, "domain": domain}
    except:
        return False, "❌ Koneksi ke layanan email gagal"

def cek_pesan(login, domain):
    try:
        res = requests.get(f"{API_1SEC}?action=getMessages&login={login}&domain={domain}", timeout=5)
        if res.status_code == 200 and res.json():
            return True, res.json()
        return False, []
    except:
        return False, []

def baca_kode_otp(login, domain, pesan_id):
    try:
        res = requests.get(f"{API_1SEC}?action=readMessage&login={login}&domain={domain}&id={pesan_id}", timeout=5)
        if res.status_code == 200:
            isi = res.json().get("body", "")
            subjek = res.json().get("subject", "")
            cari = f"{subjek} {isi}"
            kode = re.search(r"\b\d{5,6}\b", cari)
            return kode.group() if kode else "Tidak ditemukan"
        return "Gagal baca pesan"
    except:
        return "Error"

# ==================== FUNGSI DAFTAR FB ====================
def buat_data_akun():
    nama_depan = random.choice(DAFTAR_NAMA)
    nama_belakang = f"{random.choice(DAFTAR_NAMA)}{random.randint(10,99)}"
    sandi = f"Fb{random.randint(10000,99999)}"
    hari = str(random.randint(1,28))
    bulan = str(random.randint(1,12))
    tahun = str(random.randint(1990,2004))
    jk = random.choice(["M","F"])
    return {
        "nama_depan": nama_depan,
        "nama_belakang": nama_belakang,
        "sandi": sandi,
        "hari": hari,
        "bulan": bulan,
        "tahun": tahun,
        "jk": jk
    }

def daftar_fb(data, email):
    try:
        res = s.get(URL_DAFTAR_FB, headers=HEADERS, timeout=8)
        if res.status_code != 200:
            return False, "❌ Gagal membuka halaman pendaftaran"
        
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

        res_post = s.post(URL_DAFTAR_FB, data=form, headers=HEADERS, timeout=10, allow_redirects=True)

        if "home.php" in res_post.url:
            return True, "✅ Berhasil dibuat & langsung aktif"
        elif "checkpoint" in res_post.url or "confirm" in res_post.url:
            return True, "⚠️ Berhasil - butuh verifikasi OTP"
        else:
            return True, "✅ Data terkirim - tunggu konfirmasi"

    except Exception as e:
        return False, f"❌ Error: {str(e)[:30]}"

# ==================== TAMPILAN + SIMULASI ====================
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
            .proses { color: #2563eb; }
            .sukses { color: #166534; background: #f0fdf4; padding: 6px; border-radius: 4px; }
            .gagal { color: #991b1b; background: #fef2f2; padding: 6px; border-radius: 4px; }
        </style>
    </head>
    <body class="bg-gray-100 min-h-screen p-3">
        <div class="max-w-md mx-auto bg-white rounded-2xl shadow-xl overflow-hidden">
            
            <!-- HEADER -->
            <div class="bg-gradient-to-r from-blue-600 to-indigo-600 p-5 text-center">
                <h1 class="text-2xl font-bold text-white">📱 Create FB</h1>
                <p class="text-blue-100 text-sm">By Ucuk • Tanpa Proxy</p>
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
                    <h3 class="font-semibold text-gray-800 mb-2">📋 Log Proses:</h3>
                    <div id="kolomHasil" class="bg-gray-50 border border-gray-200 rounded-lg p-4 min-h-[240px] text-sm overflow-y-auto">
                        Siap digunakan...<br>
                        Masukkan jumlah akun lalu tekan tombol RUN
                    </div>
                </div>

            </div>

            <!-- FOOTER -->
            <div class="text-center text-xs text-gray-500 p-3 border-t">
                Versi Testing • Vercel
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
                    hasil.innerHTML += `<hr class="my-2">🔹 AKUN KE-${i}<br>`;
                    
                    // Simulasi langkah
                    hasil.innerHTML += `<span class="proses">📝 Membuat data nama & tanggal lahir...</span><br>`;
                    await new Promise(r => setTimeout(r, 400));

                    hasil.innerHTML += `<span class="proses">📧 Membuat email sementara...</span><br>`;
                    await new Promise(r => setTimeout(r, 400));

                    hasil.innerHTML += `<span class="proses">📤 Mengirim data pendaftaran...</span><br>`;
                    await new Promise(r => setTimeout(r, 500));

                    hasil.innerHTML += `<span class="proses">🔍 Mengecek status pendaftaran...</span><br>`;
                    await new Promise(r => setTimeout(r, 500));

                    // Ambil data asli dari server
                    try {
                        const res = await fetch(`/buat?nomor=${i}`);
                        const data = await res.json();
                        
                        if (data.status === "berhasil") {
                            hasil.innerHTML += `<div class="sukses mt-1">
                                ✅ SUKSES<br>
                                📧 Email: ${data.email}<br>
                                🔑 Sandi: ${data.sandi}<br>
                                📊 Status: ${data.ket}<br>
                                ${data.otp ? `🔢 Kode OTP: ${data.otp}<br>` : ''}
                            </div>`;
                        } else {
                            hasil.innerHTML += `<div class="gagal mt-1">❌ GAGAL: ${data.pesan}</div>`;
                        }
                    } catch (err) {
                        hasil.innerHTML += `<div class="gagal mt-1">❌ Gagal terhubung ke server</div>`;
                    }

                    hasil.scrollTop = hasil.scrollHeight;
                }

                tombol.disabled = false;
                tombol.textContent = "▶️ RUN Pembuatan";
                hasil.innerHTML += `<br>✅ Semua proses selesai!`;
            }
        </script>
    </body>
    </html>
    """)

@app.route("/buat")
def buat_satu():
    # Buat email baru
    ok_email, data_email = buat_email()
    if not ok_email:
        return jsonify({"status": "gagal", "pesan": data_email})
    
    # Buat data akun
    data_akun = buat_data_akun()
    
    # Daftar ke FB
    sukses, keterangan = daftar_fb(data_akun, data_email["email"])
    
    otp = ""
    if "verifikasi" in keterangan.lower():
        time.sleep(3)
        ok_pesan, daftar_pesan = cek_pesan(data_email["login"], data_email["domain"])
        if ok_pesan and daftar_pesan:
            otp = baca_kode_otp(data_email["login"], data_email["domain"], daftar_pesan[0]["id"])
    
    return jsonify({
        "status": "berhasil" if sukses else "gagal",
        "pesan": "",
        "email": data_email["email"],
        "sandi": data_akun["sandi"],
        "ket": keterangan,
        "otp": otp
    })

if __name__ == "__main__":
    app.run(debug=False)
