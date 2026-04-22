from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# --- DATA FLOW KEMNAKER (RULE-BASED DECISION TREE) ---
# Struktur: ID Node -> Teks Pertanyaan & Opsi Jawaban
KEMNAKER_FLOW = {
    "start": {
        "text": "Selamat datang di Asisten Virtual Kemnaker RI. Apa yang bisa kami bantu hari ini?",
        "options": [
            {"text": "Layanan SIAPkerja (KarirHub)", "next": "siapkerja"},
            {"text": "Wajib Lapor (WLKP)", "next": "wlkp"},
            {"text": "Bantuan & Pengaduan (HI)", "next": "hi_pengaduan"},
            {"text": "Informasi Pelatihan (SkillHub)", "next": "pelatihan"}
        ]
    },
    "siapkerja": {
        "text": "SIAPkerja adalah ekosistem digital layanan ketenagakerjaan. Apa yang Anda butuhkan?",
        "options": [
            {"text": "Cari Lowongan Kerja", "next": "karirhub_url"},
            {"text": "Cek Status Kepesertaan", "next": "check_status"},
            {"text": "Kembali", "next": "start"}
        ]
    },
    "karirhub_url": {
        "text": "Silakan akses KarirHub untuk mencari lowongan pekerjaan resmi di: karirhub.kemnaker.go.id",
        "options": [{"text": "Menu Utama", "next": "start"}]
    },
    "check_status": {
        "text": "Untuk cek status kepesertaan atau bantuan pemerintah, silakan login ke akun SIAPkerja Anda di kemnaker.go.id.",
        "options": [{"text": "Menu Utama", "next": "start"}]
    },
    "wlkp": {
        "text": "Sesuai UU No. 7 Tahun 1981, perusahaan wajib melaporkan data ketenagakerjaan secara daring.",
        "options": [
            {"text": "Login Portal WLKP", "next": "wlkp_url"},
            {"text": "Lihat Panduan Lapor", "next": "wlkp_panduan"},
            {"text": "Kembali", "next": "start"}
        ]
    },
    "wlkp_url": {
        "text": "Akses portal Wajib Lapor Ketenagakerjaan di Perusahaan (WLKP) di: wlkp.kemnaker.go.id",
        "options": [{"text": "Menu Utama", "next": "start"}]
    },
    "wlkp_panduan": {
        "text": "Pastikan Anda menyiapkan NIB dan data profil perusahaan sebelum melakukan pelaporan.",
        "options": [{"text": "Menu Utama", "next": "start"}]
    },
    "hi_pengaduan": {
        "text": "Layanan ini mencakup konsultasi terkait gaji, THR, atau perselisihan (PHK). Pilih opsi:",
        "options": [
            {"text": "Pusat Bantuan (Lapor!)", "next": "bantuan_url"},
            {"text": "Info Upah Minimum", "next": "upah_info"},
            {"text": "Kembali", "next": "start"}
        ]
    },
    "bantuan_url": {
        "text": "Untuk pengaduan resmi, silakan sampaikan melalui portal: bantuan.kemnaker.go.id",
        "options": [{"text": "Menu Utama", "next": "start"}]
    },
    "upah_info": {
        "text": "Informasi mengenai UMP dan UMK terbaru dapat dilihat di bagian regulasi pada website resmi Kemnaker.",
        "options": [{"text": "Menu Utama", "next": "start"}]
    },
    "pelatihan": {
        "text": "SkillHub menyediakan pelatihan bersertifikat melalui Balai Latihan Kerja (BLK).",
        "options": [
            {"text": "Jelajahi Pelatihan", "next": "skillhub_url"},
            {"text": "Kembali", "next": "start"}
        ]
    },
    "skillhub_url": {
        "text": "Cari pelatihan yang sesuai dengan minat Anda di: skillhub.kemnaker.go.id",
        "options": [{"text": "Menu Utama", "next": "start"}]
    }
}

# --- TEMPLATE UI (TAILWIND CSS + FONT AWESOME) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kemnaker RI - Assistant</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
        .chat-bubble { max-width: 85%; word-wrap: break-word; }
        .fade-in { animation: fadeIn 0.3s ease-out forwards; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body class="bg-gray-50 flex h-screen overflow-hidden text-gray-800">

    <aside class="w-72 bg-blue-900 text-white flex flex-col p-6 shadow-xl hidden md:flex">
        <div class="mb-10 text-center">
            <i class="fas fa-briefcase text-4xl mb-3 text-blue-200"></i>
            <h1 class="text-xl font-bold">Kemnaker RI</h1>
            <p class="text-[10px] text-blue-200 mt-1 tracking-widest uppercase">Layanan Ketenagakerjaan</p>
        </div>
        
        <nav class="flex-1 space-y-8">
            <div class="p-3 bg-blue-800 rounded-lg text-xs space-y-2 border border-blue-700">
                <p class="font-bold border-b border-blue-700 pb-1 mb-2 uppercase">System Info</p>
                <p class="flex items-center gap-2"><i class="fas fa-check-circle text-green-400"></i> Local Protocol 1.0</p>
                <p class="flex items-center gap-2"><i class="fas fa-shield-alt text-blue-300"></i> Rule-Based Logic</p>
            </div>

            <button onclick="location.reload()" class="w-full text-left p-3 text-sm text-blue-100 hover:bg-blue-800 rounded-lg transition-all flex items-center gap-3">
                <i class="fas fa-sync-alt"></i> Restart Assistant
            </button>
        </nav>

        <div class="mt-auto pt-6 border-t border-blue-800 text-[10px] text-blue-300 italic text-center">
            User: Rico (SQA Auditor) | 2026
        </div>
    </aside>

    <main class="flex-1 flex flex-col bg-white relative">
        <header class="h-16 border-b flex items-center justify-between px-8 bg-white/80 backdrop-blur-md z-10">
            <div class="flex items-center gap-3">
                <span class="px-3 py-1 bg-blue-50 text-blue-600 rounded-full text-xs font-bold uppercase tracking-tighter border border-blue-100">
                    Portal SIAPkerja
                </span>
            </div>
            <div class="text-gray-400 text-sm italic">Audit Mode: Enabled</div>
        </header>

        <div id="chat-box" class="flex-1 overflow-y-auto p-8 space-y-6 bg-slate-50">
            </div>
    </main>

    <script>
        const flow = {{ flow_data | tojson }};
        const chatBox = document.getElementById('chat-box');

        function renderBotMessage(node) {
            const msgDiv = document.createElement('div');
            msgDiv.className = "flex flex-col gap-2 fade-in mb-4";
            
            let optionsHtml = '';
            node.options.forEach(opt => {
                optionsHtml += `
                    <button onclick="handleSelection('${opt.text}', '${opt.next}', this)" 
                        class="block w-full text-left px-4 py-2.5 mt-2 bg-white border border-blue-200 rounded-xl text-xs font-medium hover:bg-blue-600 hover:text-white hover:border-blue-600 transition-all duration-200 shadow-sm outline-none">
                        <i class="fas fa-chevron-right mr-2 opacity-50"></i> ${opt.text}
                    </button>
                `;
            });

            msgDiv.innerHTML = `
                <div class="flex gap-4">
                    <div class="w-9 h-9 rounded-xl flex-shrink-0 flex items-center justify-center shadow-sm bg-blue-700 text-white font-bold">K</div>
                    <div class="chat-bubble p-4 rounded-2xl shadow-sm bg-white text-gray-800 rounded-tl-none border border-gray-100">
                        <div class="text-sm leading-relaxed mb-1 font-medium">${node.text}</div>
                        <div class="mt-3 border-t border-gray-100 pt-2">
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
                <div class="chat-bubble p-4 rounded-2xl text-sm leading-relaxed shadow-sm bg-blue-600 text-white rounded-tr-none">
                    ${text}
                </div>
            `;
            chatBox.appendChild(msgDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function handleSelection(text, nextNode, buttonElement) {
            // Nonaktifkan tombol agar tidak diklik dua kali
            const parentBubble = buttonElement.closest('.chat-bubble');
            const allButtons = parentBubble.querySelectorAll('button');
            allButtons.forEach(btn => {
                btn.disabled = true;
                btn.classList.add('opacity-50', 'cursor-not-allowed');
            });

            renderUserMessage(text);
            
            // Beri jeda sedikit seolah bot sedang berpikir
            setTimeout(() => {
                loadNode(nextNode);
            }, 400);
        }

        function loadNode(nodeId) {
            const node = flow[nodeId];
            renderBotMessage(node);
        }

        // Inisialisasi percakapan
        window.onload = () => loadNode('start');
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, flow_data=KEMNAKER_FLOW)

if __name__ == '__main__':
    # Debug=True mempermudah proses development
    app.run(debug=True, port=5003)