from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Gabungan Regulasi BKN 3/2023 & FAQ 28 Jan 2026
KNOWLEDGE_BASE = {
    "start": {
        "reply": "Selamat datang di Layanan Konsultasi Angka Kredit (AK) Jabatan Fungsional. Pilih topik:",
        "options": ["Konversi Predikat", "Kenaikan Pangkat/Jenjang", "Tugas Belajar", "Sisa AK"]
    },
    "konversi predikat": {
        "reply": "Sesuai Pasal 4 Peraturan BKN 3/2023, AK ditetapkan berdasarkan konversi Predikat Kinerja:\n- Sangat Baik: 150%\n- Baik: 100%\n- Cukup: 75%",
        "options": ["Kenaikan Pangkat/Jenjang", "Kembali"]
    },
    "kenaikan pangkat/jenjang": {
        "reply": "FAQ: Jika naik pangkat dari III/c ke III/d (dalam jenjang yang sama), AK lama diakumulasikan. Namun, jika naik jenjang (misal ke Ahli Madya IV/a), wajib lulus Uji Kompetensi.",
        "options": ["Sisa AK", "Uji Kompetensi", "Kembali"]
    },
    "sisa ak": {
        "reply": "Berdasarkan Pasal 19 ayat (5) BKN 3/2023: Kelebihan AK untuk kenaikan pangkat ke jenjang jabatan lebih tinggi TIDAK diperhitungkan (Hangus).",
        "options": ["Konversi Predikat", "Kembali"]
    },
    "tugas belajar": {
        "reply": "FAQ: Selesai Tugas Belajar mendapat tambahan AK 25% dari AK Kumulatif. Catatan: Jika ijazah sudah dipakai naik pangkat, tidak bisa diklaim lagi.",
        "options": ["Konversi Predikat", "Kembali"]
    }
}

@app.route('/')
def index():
    return render_template('index.html', mode="Rule-Based (Integrated)")

@app.route('/get_response', methods=['POST'])
def get_response():
    user_text = request.json.get("message", "").lower()
    response_data = KNOWLEDGE_BASE.get("start")
    
    for key in KNOWLEDGE_BASE:
        if key in user_text:
            response_data = KNOWLEDGE_BASE[key]
            break
            
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=5001, debug=True)