from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- ATURAN JAWABAN (RULES) ---
BOT_RULES = {
    "halo": "Halo! Saya Bot Rule. Ada yang bisa saya bantu?",
    "tugas": "Tugas saya adalah memberikan informasi berdasarkan aturan yang sudah ditentukan.",
    "kontak": "Anda bisa menghubungi admin di nomor 0812-3456-789.",
    "bye": "Sampai jumpa lagi! Semoga hari Anda menyenangkan."
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def chat():
    user_message = request.json.get("message", "").lower()
    
    # Mencari jawaban berdasarkan kata kunci
    # Jika tidak ada di BOT_RULES, gunakan pesan default
    reply = BOT_RULES.get(user_message, "Maaf, saya tidak mengerti. Coba ketik: halo, tugas, atau kontak.")
    
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
