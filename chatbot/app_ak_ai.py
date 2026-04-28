from flask import Flask, render_template, request, jsonify
import ollama
import markdown

app = Flask(__name__)

@app.route('/')
def index():
    # Mengarahkan ke template khusus AI (tanpa menu otomatis)
    return render_template('index_ai.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_text = request.json.get("message")
    
    if not user_text:
        return jsonify({"reply": "Input tidak boleh kosong."}), 400

    try:
        # Panggil Ollama
        response = ollama.chat(model='kemnaker-llama', messages=[
            {'role': 'user', 'content': user_text}
        ])
        
        raw_reply = response['message']['content']
        
        # Konversi Markdown AI (termasuk tabel) menjadi HTML
        formatted_reply = markdown.markdown(raw_reply, extensions=['tables'])
        
        return jsonify({"reply": formatted_reply})
        
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5002, debug=True)