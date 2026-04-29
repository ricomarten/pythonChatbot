from flask import Flask, render_template

app = Flask(__name__)

# Route utama (Halaman Beranda)
@app.route('/')
def home():
    return "<h1>Halo! Ini adalah aplikasi Flask pertama saya.</h1>"

# Route dengan parameter (Menyapa User)
@app.route('/user/<nama>')
def greet(nama):
    # return f"Selamat datang, {nama}!"
    # render_template akan mencari file di folder templates
    return render_template('index.html', nama_user=nama)

if __name__ == '__main__':
    app.run(debug=True)
