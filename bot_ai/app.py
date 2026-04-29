from flask import Flask, render_template, request, jsonify
import ollama

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get("message", "")
    
    try:
        #response = ollama.chat(model='llama3.2', messages=[
        #    {'role': 'user', 'content': user_input},
        #])
        response = ollama.chat(model='kemnaker-bot', messages=[
            {'role': 'user', 'content': user_input}
        ])

        
        reply_text = response['message']['content']
    except Exception as e:
        reply_text = f"Maaf, terjadi kesalahan: {str(e)}"
    
    return jsonify({"reply": reply_text})

if __name__ == '__main__':
    app.run(port=5002,debug=True)