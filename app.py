@app.route("/")
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>FB Generator</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body { -webkit-tap-highlight-color: transparent; }
            pre { white-space: pre-wrap; word-wrap: break-word; }
        </style>
    </head>
    <body class="bg-gray-100 min-h-screen p-4 font-sans">
        <div class="max-w-md mx-auto bg-white rounded-xl shadow-lg overflow-hidden">
            <!-- Header -->
            <div class="bg-blue-600 p-4 text-center">
                <h1 class="text-xl font-bold text-white">🚀 FB Generator</h1>
                <p class="text-blue-100 text-sm">Proxy + TempMail Otomatis</p>
            </div>

            <!-- Konten -->
            <div class="p-5 space-y-4">
                <p class="text-gray-700 text-center">Tekan tombol di bawah untuk mulai membuat akun:</p>

                <button id="tombolMulai" onclick="mulaiProses()" 
                    class="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-4 rounded-lg transition duration-200 shadow-md">
                    ✅ Mulai Buat Akun
                </button>

                <!-- Area Hasil -->
                <div id="areaHasil" class="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200 min-h-[200px] text-sm">
                    <p class="text-gray-500 text-center">Hasil proses akan muncul di sini...</p>
                </div>
            </div>

            <!-- Footer -->
            <div class="text-center text-xs text-gray-500 p-3 border-t">
                Versi Vercel • Tanpa Selenium
            </div>
        </div>

        <script>
            async function mulaiProses() {
                const tombol = document.getElementById('tombolMulai');
                const area = document.getElementById('areaHasil');
                
                tombol.disabled = true;
                tombol.textContent = "⏳ Sedang Memproses...";
                area.innerHTML = `<div class="text-center text-gray-600 animate-pulse">
                    <p>Mencari proxy...</p>
                    <p>Membuat email...</p>
                    <p>Mendaftarkan akun...</p>
                </div>`;

                try {
                    const res = await fetch("/jalankan");
                    const data = await res.json();
                    
                    let tampil = `<div class="space-y-2">`;
                    tampil += `<p class="font-semibold ${data.status === 'berhasil' ? 'text-green-600' : 'text-red-600'}">${data.status.toUpperCase()}</p>`;
                    
                    if(data.info_proxy) tampil += `<p><b>Proxy:</b> ${data.info_proxy}</p>`;
                    if(data.email) tampil += `<p><b>Email:</b> ${data.email}</p>`;
                    if(data.sandi) tampil += `<p><b>Sandi:</b> ${data.sandi}</p>`;
                    if(data.status_daftar) tampil += `<p><b>Status:</b> ${data.status_daftar}</p>`;
                    if(data.otp) tampil += `<p class="text-blue-600 font-bold"><b>Kode OTP:</b> ${data.otp}</p>`;
                    if(data.pesan) tampil += `<p class="text-red-500">${data.pesan}</p>`;
                    
                    tampil += `</div>`;
                    area.innerHTML = tampil;

                } catch (err) {
                    area.innerHTML = `<p class="text-red-500">❌ Gagal terhubung ke server</p>`;
                }

                tombol.disabled = false;
                tombol.textContent = "✅ Mulai Buat Akun";
            }
        </script>
    </body>
    </html>
    """)
                                  
