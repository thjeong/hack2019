from flask import Flask, send_file, request, make_response
from server.responseFunctions import login_func

app = Flask(__name__, static_url_path='', static_folder='dist/hack2019')

@app.route('/')
def index():
    return send_file('dist/hack2019/index.html')


@app.route('/login', methods=["POST"])
def login():
    a = request.form
    response = login_func(a['userid'])
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')
