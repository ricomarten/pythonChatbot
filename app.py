from flask import Flask, render_template, request, jsonify
import ollama

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_message = data.get("message")
    # Mengambil model yang dipilih dari frontend, default ke deepseek-r1:7b
    selected_model = data.get("model", "deepseek-r1:7b")

    try:
        # Panggilan ke Ollama lokal
        response = ollama.chat(model=selected_model, messages=[
            {
                'role': 'user',
                'content': user_message,
            },
        ])
        
        bot_reply = response['message']['content']
        
    except Exception as e:
        print(f"Error: {e}")
        bot_reply = f"Gagal memanggil model '{selected_model}'. Pastikan Ollama sudah berjalan dan model telah di-download."

    return jsonify({"reply": bot_reply})

if __name__ == '__main__':
    # Berjalan di port 5000
    app.run(debug=True, port=5000)