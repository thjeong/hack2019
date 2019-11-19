from flask import Flask, send_file

app = Flask(__name__, static_url_path='', static_folder='static/dist/hack2019')

@app.route('/')
def index():
    return send_file('dist/hack2019/index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
