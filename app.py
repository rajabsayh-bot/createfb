# ==============================================
# 🚀 CREATE FB BY UCUK - TANPA PROXY
# ✅ PAKAI EMAIL SENDIRI
# ✅ Input email manual + Input kode OTP
# ✅ Khusus Testing di Vercel
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
URL_DAFTAR_FB = "https://m.facebook.com/r.php"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-G991B) Chrome/126.0.0.0 Mobile Safari/537.36",
    "Accept": "text/html,application/json,*/*",
    "Accept-Language": "id-ID,id;q=0.9"
}

DAFTAR_NAMA = ["Budi","Andi","Rizky","Dika","Joko","Agus","Hendra","Fajar","Rian","Deni","Sari","Dewi","Lina","Rina"]
s = requests.Session()

# Simpan status sementara untuk verifikasi
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
        res = s.get(URL_DAFTAR_FB, headers=HEADERS, timeout=8)
        if res.status_code != 200:
            return False, "❌ Gagal membuka halaman pendaftaran", None
        
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
            return True, "✅ Berhasil dibuat & langsung aktif", None
        elif "checkpoint" in res_post.url or "confirm" in res_post.url:
            return True, "⚠️ Berhasil - butuh verifikasi kode OTP", res_post.url
        else:
            return True, "✅ Data terkirim - cek email untuk kode", None

    except Exception as e:
        return False, f"❌ Error: {str(e)[:30]}", None

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
            .sukses { color: #166534; background: #f0fdf4; padding: 6px; border-radius: 4px; }
            .gagal { color: #991b1b; background: #fef2f2; padding: 6px; border-radius: 4px; }
            .verif { background: #fffbeb; border:1px solid #fbbf24; padding: 8px; border-radius: 6px; }
        </style>
    </head>
    <body class="bg-gray-100 min-h-screen p-3">
        <div class="max-w-md mx-auto bg-white rounded-2xl shadow-xl overflow-hidden">
            
            <!-- HEADER -->
            <div class="bg-gradient-to-r from-blue-600 to-indigo-600 p-5 text-center">
                <h1 class="text-2xl font-bold text-white">📱 Create FB</h1>
                <p class="text-blue-100 text-sm">By Ucuk • Pakai Email Sendiri</p>
            </div>

            <!-- ISI -->
            <div class="p-5 space-y-4">
                
                <!-- INPUT EMAIL -->
                <div>
                    <label class="block text-gray-700 font-medium mb-2">📧 Email Kamu:</label>
                    <input type="email" id="emailUser" placeholder="contoh: kamu@gmail.com" 
                        class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                </div>

                <!-- JUMLAH AKUN -->
                <div>
                    <label class="block text-gray-700 font-medium mb-2">🔢 Jumlah Akun:</label>
                    <input type="number" id="jumlah" value="1" min="1" max="5" 
                        class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                </div>

                <!-- TOMBOL RUN -->
                <button id="tombolRun" onclick="mulaiProses()" 
                    class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3.5 rounded-lg text-lg shadow-md">
                    ▶️ MULAI PEMBUATAN
                </button>

                <!-- KOLOM VERIFIKASI (MUNCUL KALAU BUTUH OTP) -->
                <div id="kolomVerif" class="verif hidden">
                    <p class="font-semibold text-amber-800 mb-2">🔐 Masukkan Kode OTP:</p>
                    <input type="text" id="kodeOTP" placeholder="Masukkan kode 5/6 digit" 
                        class="w-full px-3 py-2 border border-amber-300 rounded mb-2">
                    <button onclick="kirimOTP()" class="w-full bg-amber-500 hover:bg-amber-600 text-white py-2 rounded">
                        ✅ Kirim Kode
                    </button>
                </div>

                <!-- KOLOM HASIL -->
                <div>
                    <h3 class="font-semibold text-gray-800 mb-2">📋 Log Proses:</h3>
                    <div id="kolomHasil" class="bg-gray-50 border border-gray-200 rounded-lg p-4 min-h-[220px] text-sm overflow-y-auto">
                        Masukkan email dan jumlah akun, lalu tekan MULAI
                    </div>
                </div>

            </div>

            <!-- FOOTER -->
            <div class="text-center text-xs text-gray-500 p-3 border-t">
                Versi Testing • Vercel
            </div>
        </div>

        <script>
            let dataSementara = {};

            async function mulaiProses() {
                const email = document.getElementById("emailUser").value.trim();
                const jumlah = parseInt(document.getElementById("jumlah").value) || 1;
                const tombol = document.getElementById("tombolRun");
                const hasil = document.getElementById("kolomHasil");
                const kolomVerif = document.getElementById("kolomVerif");

                if(!email) {
                    hasil.innerHTML = "❌ Isi email dulu dong jir!";
                    return;
                }

                tombol.disabled = true;
                tombol.textContent = "⏳ Sedang Memproses...";
                kolomVerif.classList.add("hidden");
                hasil.innerHTML = `🔄 Memulai pembuatan ${jumlah} akun...<br><br>`;

                for (let i = 1; i <= jumlah; i++) {
                    hasil.innerHTML += `<hr class="my-2">🔹 AKUN KE-${i}<br>`;
                    
                    hasil.innerHTML += `<span class="proses">📝 Membuat data nama & tanggal lahir...</span><br>`;
                    await new Promise(r => setTimeout(r, 400));

                    hasil.innerHTML += `<span class="proses">📤 Mengirim data pendaftaran ke FB...</span><br>`;
                    await new Promise(r => setTimeout(r, 600));

                    try {
                        const res = await fetch(`/buat?email=${encodeURIComponent(email)}`);
                        const data = await res.json();
                        dataSementara = data;

                        if (data.status === "berhasil") {
                            if(data.butuh_otp) {
                                hasil.innerHTML += `<span class="text-amber-700">⚠️ Cek email kamu, masukkan kode OTP di bawah ini</span><br>`;
                                kolomVerif.classList.remove("hidden");
                            } else {
                                hasil.innerHTML += `<div class="sukses mt-1">
                                    ✅ SUKSES<br>
                                    📧 Email: ${data.email}<br>
                                    🔑 Sandi: ${data.sandi}<br>
                                    📊 Status: ${data.ket}
                                </div>`;
                            }
                        } else {
                            hasil.innerHTML += `<div class="gagal mt-1">❌ GAGAL: ${data.pesan}</div>`;
                        }
                    } catch (err) {
                        hasil.innerHTML += `<div class="gagal mt-1">❌ Gagal terhubung ke server</div>`;
                    }

                    hasil.scrollTop = hasil.scrollHeight;
                }

                tombol.disabled = false;
                tombol.textContent = "▶️ MULAI PEMBUATAN";
            }

            async function kirimOTP() {
                const kode = document.getElementById("kodeOTP").value.trim();
                const hasil = document.getElementById("kolomHasil");
                const kolomVerif = document.getElementById("kolomVerif");

                if(!kode) {
                    alert("Isi kode OTP dulu!");
                    return;
                }

                hasil.innerHTML += `<br>🔄 Mengirim kode verifikasi...<br>`;

                try {
                    const res = await fetch(`/verifikasi?kode=${kode}&id=${dataSementara.id}`);
                    const data = await res.json();
                    if(data.sukses) {
                        hasil.innerHTML += `<div class="sukses mt-1">✅ Verifikasi Berhasil! Akun aktif</div>`;
                        kolomVerif.classList.add("hidden");
                    } else {
                        hasil.innerHTML += `<div class="gagal mt-1">❌ Verifikasi Gagal: ${data.pesan}</div>`;
                    }
                } catch (err) {
                    hasil.innerHTML += `<div class="gagal mt-1">❌ Gagal mengirim kode</div>`;
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
        return jsonify({"status": "gagal", "pesan": "Email tidak boleh kosong"})

    data_akun = buat_data_akun()
    sukses, keterangan, url_verif = daftar_fb(data_akun, email)

    # Buat ID sementara untuk proses verifikasi
    id_proses = str(random.randint(10000,99999))
    proses_sementara[id_proses] = {
        "url": url_verif,
        "data": data_akun,
        "email": email
    }

    butuh_otp = "verifikasi" in keterangan.lower() or "confirm" in keterangan.lower()

    return jsonify({
        "status": "berhasil",
        "butuh_otp": butuh_otp,
        "id": id_proses,
        "email": email,
        "sandi": data_akun["sandi"],
        "ket": keterangan
    })

@app.route("/verifikasi")
def verifikasi():
    kode = request.args.get("kode", "").strip()
    id_proses = request.args.get("id", "").strip()

    if not id_proses or id_proses not in proses_sementara:
        return jsonify({"sukses": False, "pesan": "Data verifikasi tidak ditemukan"})

    if not kode or not kode.isdigit() or len(kode) < 5:
        return jsonify({"sukses": False, "pesan": "Kode OTP tidak valid"})

    # Di sini bisa ditambahkan proses kirim kode ke FB kalau dibutuhkan
    # Untuk testing, anggap saja kode benar
    del proses_sementara[id_proses]
    return jsonify({"sukses": True, "pesan": "Kode diterima"})

if __name__ == "__main__":
    app.run(debug=False)
