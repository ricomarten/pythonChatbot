from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# --- DATA FLOW KEMENDAG (RULE-BASED) ---
KEMENDAG_FLOW = {
    "start": {
        "text": "Selamat datang di Layanan Informasi Kemendag RI. Silakan pilih kategori layanan yang Anda butuhkan:",
        "options": [
            {"text": "SIPT & Ekspor-Impor", "next": "sipt"},
            {"text": "Harga Bahan Pokok (SP2KP)", "next": "bapok"},
            {"text": "Pengaduan Konsumen", "next": "konsumen"},
            {"text": "Profil Kemendag", "next": "profil"}
        ]
    },
    "sipt": {
        "text": "Layanan perizinan tersedia melalui SIPT (Sistem Informasi Perizinan Terpadu). Apa yang ingin Anda urus?",
        "options": [
            {"text": "Pendaftaran SIUP", "next": "sipt_url"},
            {"text": "Izin Ekspor/Impor (Inatrade)", "next": "inatrade_url"},
            {"text": "Kembali", "next": "start"}
        ]
    },
    "sipt_url": {
        "text": "Silakan akses portal resmi SIPT di: sipt.kemendag.go.id",
        "options": [{"text": "Menu Utama", "next": "start"}]
    },
    "inatrade_url": {
        "text": "Untuk layanan Ekspor/Impor, silakan akses inatrade.kemendag.go.id. Pastikan NIB Anda sudah terdaftar.",
        "options": [{"text": "Menu Utama", "next": "start"}]
    },
    "bapok": {
        "text": "Informasi harga harian bahan pokok di seluruh pasar Indonesia terpantau di Sistem SP2KP. Anda ingin melihat harga?",
        "options": [
            {"text": "Lihat Harga Nasional", "next": "sp2kp_url"},
            {"text": "Kembali", "next": "start"}
        ]
    },
    "sp2kp_url": {
        "text": "Update harga harian tersedia di: sp2kp.kemendag.go.id",
        "options": [{"text": "Menu Utama", "next": "start"}]
    },
    "konsumen": {
        "text": "Layanan Pengaduan Konsumen tersedia melalui Ditjen Perlindungan Konsumen dan Tertib Niaga. Pilih opsi:",
        "options": [
            {"text": "Cara Buat Pengaduan", "next": "adu_cara"},
            {"text": "Cek Status Pengaduan", "next": "adu_status"},
            {"text": "Kembali", "next": "start"}
        ]
    },
    "adu_cara": {
        "text": "Anda dapat membuat laporan melalui WhatsApp resmi di 0853-1111-1010 atau portal simpktn.kemendag.go.id.",
        "options": [{"text": "Menu Utama", "next": "start"}]
    },
    "adu_status": {
        "text": "Untuk cek status, silakan siapkan nomor tiket pengaduan Anda dan akses simpktn.kemendag.go.id.",
        "options": [{"text": "Menu Utama", "next": "start"}]
    },
    "profil": {
        "text": "Kementerian Perdagangan dipimpin oleh Menteri Perdagangan RI. Informasi lebih lanjut tersedia di kemendag.go.id.",
        "options": [{"text": "Menu Utama", "next": "start"}]
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kemendag Assistant - Rule Based</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
        .chat-bubble { max-width: 85%; word-wrap: break-word; }
        .fade-in { animation: fadeIn 0.3s ease-out forwards; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body class="bg-gray-50 flex h-screen overflow-hidden text-gray-800">

    <aside class="w-72 bg-red-900 text-white flex flex-col p-6 shadow-xl hidden md:flex">
        <div class="mb-10 text-center">
            <i class="fas fa-landmark text-4xl mb-3 text-red-200"></i>
            <h1 class="text-xl font-bold">Kemendag RI</h1>
            <p class="text-[10px] text-red-200 mt-1 tracking-widest uppercase">Virtual Assistant</p>
        </div>
        
        <nav class="flex-1 space-y-8">
            <div>
                <label class="text-xs text-red-300 uppercase font-bold tracking-wider">Status System</label>
                <div class="mt-3 p-3 bg-red-800 rounded-lg text-xs space-y-2 border border-red-700">
                    <p class="flex items-center gap-2"><i class="fas fa-check-circle text-green-400"></i> Server Online</p>
                    <p class="flex items-center gap-2"><i class="fas fa-shield-alt text-blue-400"></i> Rule-Based Logic</p>
                </div>
            </div>

            <div class="space-y-2">
                <button onclick="location.reload()" class="w-full text-left p-3 text-sm text-red-100 hover:bg-red-800 rounded-lg transition-all flex items-center gap-3">
                    <i class="fas fa-sync-alt"></i> Restart Assistant
                </button>
            </div>
        </nav>

        <div class="mt-auto pt-6 border-t border-red-800">
            <div class="text-[10px] text-red-300 italic text-center">
                &copy; 2026 Audit System - Kemendag RI
            </div>
        </div>
    </aside>

    <main class="flex-1 flex flex-col bg-white relative">
        <header class="h-16 border-b flex items-center justify-between px-8 bg-white/80 backdrop-blur-md z-10">
            <div class="flex items-center gap-3">
                <span class="px-3 py-1 bg-red-50 text-red-600 rounded-full text-xs font-bold uppercase tracking-tighter border border-red-100">
                    Sistem Layanan Terpadu
                </span>
            </div>
            <div class="text-gray-400 text-sm italic">Mode: Decision Tree (Non-AI)</div>
        </header>

        <div id="chat-box" class="flex-1 overflow-y-auto p-8 space-y-6 bg-slate-50">
            </div>

        <div class="p-8 bg-white border-t">
            <div class="max-w-4xl mx-auto">
                <p class="text-xs text-gray-500 mb-3 font-semibold uppercase tracking-wider">Pilih Opsi Layanan:</p>
                <div id="options-container" class="flex flex-wrap gap-3">
                    </div>
                <p class="text-[10px] text-center text-gray-400 mt-6 italic">
                    <i class="fas fa-info-circle mr-1"></i> Klik pada tombol pilihan di atas untuk melanjutkan interaksi.
                </p>
            </div>
        </div>
    </main>

    <script>
    const flow = {{ flow_data | tojson }};
    const chatBox = document.getElementById('chat-box');

    function renderBotMessage(node) {
        const msgDiv = document.createElement('div');
        msgDiv.className = "flex flex-col gap-2 fade-in mb-4";
        
        // Template untuk Bubble Chat Bot
        let optionsHtml = '';
        
        // Membuat tombol pilihan di dalam bubble chat
        node.options.forEach(opt => {
            optionsHtml += `
                <button onclick="handleSelection('${opt.text}', '${opt.next}', this)" 
                    class="block w-full text-left px-4 py-2 mt-2 bg-white border border-red-200 rounded-lg text-xs font-medium hover:bg-red-600 hover:text-white hover:border-red-600 transition-all duration-200">
                    <i class="fas fa-chevron-right mr-2 opacity-50"></i> ${opt.text}
                </button>
            `;
        });

        msgDiv.innerHTML = `
            <div class="flex gap-4">
                <div class="w-9 h-9 rounded-xl flex-shrink-0 flex items-center justify-center shadow-sm bg-red-700 text-white">
                    <i class="fas fa-university text-xs"></i>
                </div>
                <div class="chat-bubble p-4 rounded-2xl shadow-sm bg-gray-100 text-gray-800 rounded-tl-none border border-gray-200">
                    <div class="text-sm leading-relaxed mb-1">${node.text}</div>
                    <div class="mt-3 border-t border-gray-200 pt-2">
                        ${optionsHtml}
                    </div>
                </div>
            </div>
        `;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function renderUserMessage(text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = "flex gap-4 flex-row-reverse fade-in mb-4";
        msgDiv.innerHTML = `
            <div class="w-9 h-9 rounded-xl flex-shrink-0 flex items-center justify-center shadow-sm bg-gray-800 text-white">
                <i class="fas fa-user text-xs"></i>
            </div>
            <div class="chat-bubble p-4 rounded-2xl text-sm leading-relaxed shadow-sm bg-red-600 text-white rounded-tr-none">
                ${text}
            </div>
        `;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function handleSelection(text, nextNode, buttonElement) {
        // Matikan semua tombol di bubble chat yang sama agar tidak bisa diklik dua kali
        const parentBubble = buttonElement.closest('.chat-bubble');
        const allButtons = parentBubble.querySelectorAll('button');
        allButtons.forEach(btn => {
            btn.disabled = true;
            btn.classList.add('opacity-50', 'cursor-not-allowed');
        });

        // Render pesan user
        renderUserMessage(text);

        // Lanjut ke pesan bot berikutnya
        setTimeout(() => loadNode(nextNode), 500);
    }

    function loadNode(nodeId) {
        const node = flow[nodeId];
        renderBotMessage(node);
    }

    // Jalankan alur pertama kali
    window.onload = () => loadNode('start');
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, flow_data=KEMENDAG_FLOW)

if __name__ == '__main__':
    app.run(debug=True, port=5000)