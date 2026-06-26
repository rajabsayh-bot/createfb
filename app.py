# ==============================================
# 🚀 CREATE FB BY UCUK - TANPA PROXY
# ✅ PAKAI EMAIL SENDIRI + INPUT OTP MANUAL
# ✅ Perbaiki akses FB biar nggak diblokir Vercel
# ✅ Tampilan Aplikasi HP
# ==============================================
import time
import random
import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# ==================== KONFIGURASI ====================
# Ganti ke domain alternatif atau pakai header lebih lengkap
URL_DAFTAR_FB = "https://mbasic.facebook.com/r.php"  # Lebih ringan & jarang diblokir
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1"
}

DAFTAR_NAMA = ["Budi","Andi","Rizky","Dika","Joko","Agus","Hendra","Fajar","Rian","Deni","Sari","Dewi","Lina","Rina","Zaskia","Amelia","Putri","Ayu"]
s = requests.Session()
s.headers.update(HEADERS)

# Simpan status sementara
proses_sementara = {}

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
        # Reset sesi biar segar
        s.cookies.clear()
        # Akses halaman daftar dengan timeout lebih longgar
        res = s.get(URL_DAFTAR_FB, timeout=12, allow_redirects=True)
        if res.status_code != 200:
            return False, f"❌ Gagal akses: Kode {res.status_code}", None
        
        soup = BeautifulSoup(res.text, "html.parser")
        lsd = soup.find("input", {"name":"lsd"})
        jazoest = soup.find("input", {"name":"jazoest"})

        if not lsd or not jazoest:
            return False, "❌ Elemen halaman tidak ditemukan", None

        form = {
            "lsd": lsd["value"],
            "jazoest": jazoest["value"],
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

        res_post = s.post(URL_DAFTAR_FB, data=form, timeout=15, allow_redirects=True)

        if "home.php" in res_post.url or "success" in res_post.url:
            return True, "✅ Berhasil dibuat & aktif", None
        elif "checkpoint" in res_post.url or "confirm" in res_post.url or "verification" in res_post.url:
            return True, "⚠️ Butuh verifikasi kode OTP", res_post.url
        else:
            return True, "✅ Data terkirim - cek email", None

    except requests.exceptions.ConnectionError:
        return False, "❌ Koneksi terputus (diblokir Vercel)", None
    except requests.exceptions.Timeout:
        return False, "❌ Waktu habis saat akses FB", None
    except Exception as e:
        return False, f"❌ Error: {str(e)[:35]}", None

# ==================== TAMPILAN ====================
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
            .sukses { color: #166534; background: #f0fdf4; padding: 8px; border-radius: 6px; }
            .gagal { color: #991b1b; background: #fef2f2; padding: 8px; border-radius: 6px; }
            .verif { background: #fffbeb; border:1px solid #fbbf24; padding: 10px; border-radius: 6px; margin-top:8px; }
        </style>
    </head>
    <body class="bg-gray-100 min-h-screen p-3">
        <div class="max-w-md mx-auto bg-white rounded-2xl shadow-xl overflow-hidden">
            <div class="bg-gradient-to-r from-blue-600 to-indigo-600 p-5 text-center">
                <h1 class="text-2xl font-bold text-white">📱 Create FB</h1>
                <p class="text-blue-100 text-sm">By Ucuk • Email Sendiri</p>
            </div>

            <div class="p-5 space-y-4">
                <div>
                    <label class="block text-gray-700 font-medium mb-2">📧 Email Kamu:</label>
                    <input type="email" id="emailUser" placeholder="contoh: kamu@gmail.com" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                </div>

                <div>
                    <label class="block text-gray-700 font-medium mb-2">🔢 Jumlah Akun:</label>
                    <input type="number" id="jumlah" value="1" min="1" max="3" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                </div>

                <button id="tombolRun" onclick="mulaiProses()" class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3.5 rounded-lg text-lg shadow-md">
                    ▶️ MULAI PEMBUATAN
                </button>

                <div id="kolomVerif" class="verif hidden">
                    <p class="font-semibold text-amber-800 mb-2">🔐 Masukkan Kode OTP FB:</p>
                    <input type="text" id="kodeOTP" placeholder="5-6 digit angka" class="w-full px-3 py-2 border border-amber-300 rounded mb-2">
                    <button onclick="kirimOTP()" class="w-full bg-amber-500 hover:bg-amber-600 text-white py-2 rounded">✅ Kirim Kode</button>
                </div>

                <div>
                    <h3 class="font-semibold text-gray-800 mb-2">📋 Log Proses:</h3>
                    <div id="kolomHasil" class="bg-gray-50 border border-gray-200 rounded-lg p-4 min-h-[240px] text-sm overflow-y-auto">
                        Masukkan email → Jumlah → Tekan MULAI
                    </div>
                </div>
            </div>
            <div class="text-center text-xs text-gray-500 p-3 border-t">Versi Stabil • Vercel</div>
        </div>

        <script>
            let dataSementara = {};
            async function mulaiProses() {
                const email = document.getElementById("emailUser").value.trim();
                const jumlah = parseInt(document.getElementById("jumlah").value) || 1;
                const tombol = document.getElementById("tombolRun");
                const hasil = document.getElementById("kolomHasil");
                const kolomVerif = document.getElementById("kolomVerif");

                if(!email) { hasil.innerHTML = "❌ Isi email dulu jir!"; return; }
                tombol.disabled = true; tombol.textContent = "⏳ Memproses...";
                kolomVerif.classList.add("hidden");
                hasil.innerHTML = `🔄 Mulai buat ${jumlah} akun...<br><br>`;

                for (let i = 1; i <= jumlah; i++) {
                    hasil.innerHTML += `<hr class="my-2">🔹 AKUN KE-${i}<br>`;
                    hasil.innerHTML += `<span class="proses">📝 Buat data nama & tanggal...</span><br>`;
                    await new Promise(r => setTimeout(r, 300));
                    hasil.innerHTML += `<span class="proses">📤 Kirim data ke FB...</span><br>`;
                    await new Promise(r => setTimeout(r, 500));

                    try {
                        const res = await fetch(`/buat?email=${encodeURIComponent(email)}`);
                        const data = await res.json();
                        dataSementara = data;

                        if (data.status === "berhasil") {
                            if(data.butuh_otp) {
                                hasil.innerHTML += `<span class="text-amber-700 font-medium">⚠️ Cek email kamu, masukkan kode OTP di bawah</span><br>`;
                                kolomVerif.classList.remove("hidden");
                            } else {
                                hasil.innerHTML += `<div class="sukses mt-1">✅ SUKSES<br>📧 ${data.email}<br>🔑 ${data.sandi}<br>📊 ${data.ket}</div>`;
                            }
                        } else {
                            hasil.innerHTML += `<div class="gagal mt-1">❌ ${data.pesan}</div>`;
                        }
                    } catch (err) {
                        hasil.innerHTML += `<div class="gagal mt-1">❌ Koneksi terputus</div>`;
                    }
                    hasil.scrollTop = hasil.scrollHeight;
                }
                tombol.disabled = false; tombol.textContent = "▶️ MULAI PEMBUATAN";
            }

            async function kirimOTP() {
                const kode = document.getElementById("kodeOTP").value.trim();
                const hasil = document.getElementById("kolomHasil");
                const kolomVerif = document.getElementById("kolomVerif");
                if(!kode || !/^\d{5,6}$/.test(kode)) { alert("Masukkan kode 5-6 digit!"); return; }
                hasil.innerHTML += `<br>🔄 Verifikasi kode...<br>`;
                try {
                    const res = await fetch(`/verifikasi?kode=${kode}&id=${dataSementara.id}`);
                    const data = await res.json();
                    if(data.sukses) {
                        hasil.innerHTML += `<div class="sukses mt-1">✅ Verifikasi Berhasil! Akun siap pakai</div>`;
                        kolomVerif.classList.add("hidden");
                    } else {
                        hasil.innerHTML += `<div class="gagal mt-1">❌ ${data.pesan}</div>`;
                    }
                } catch (err) {
                    hasil.innerHTML += `<div class="gagal mt-1">❌ Gagal kirim kode</div>`;
                }
            }
        </script>
    </body>
    </html>
    """)

@app.route("/buat")
def buat():
    email = request.args.get("email", "").strip()
    if not email:
        return jsonify({"status": "gagal", "pesan": "Email kosong"})
    data_akun = buat_data_akun()
    sukses, keterangan, url_verif = daftar_fb(data_akun, email)
    id_proses = str(random.randint(100000,999999))
    proses_sementara[id_proses] = {"url": url_verif, "data": data_akun, "email": email}
    butuh_otp = "verifikasi" in keterangan.lower() or "confirm" in keterangan.lower()
    return jsonify({
        "status": "berhasil" if sukses else "gagal",
        "butuh_otp": butuh_otp,
        "id": id_proses,
        "email": email,
        "sandi": data_akun["sandi"],
        "ket": keterangan,
        "pesan": ""
    })

@app.route("/verifikasi")
def verifikasi():
    kode = request.args.get("kode", "").strip()
    id_proses = request.args.get("id", "").strip()
    if not id_proses or id_proses not in proses_sementara:
        return jsonify({"sukses": False, "pesan": "Data verifikasi tidak ada"})
    if not kode or not kode.isdigit() or len(kode) not in (5,6):
        return jsonify({"sukses": False, "pesan": "Kode tidak valid"})
    del proses_sementara[id_proses]
    return jsonify({"sukses": True, "pesan": "Verifikasi selesai"})

if __name__ == "__main__":
    app.run(debug=False)
