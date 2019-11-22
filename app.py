from flask import Flask, send_file, request, make_response
from server.responseFunctions import login_func, summary_func, detail_func

app = Flask(__name__, static_url_path='', static_folder='dist/hack2019')

@app.route('/')
def index():
    return send_file('dist/hack2019/index.html')


@app.route('/login', methods=["POST"])
def login():
    a = request.json
    print(a)
    response = login_func(a['userid'])
    return response

@app.route('/summary', methods=['POST'])
def summary():
    a = request.json
    print(a)
    response = summary_func(a['userid'], a['total_salary'])
    return response

@app.route('/detail', methods=['POST'])
def detail():
    a = request.json
    print(a)
    response = detail_func(a)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')
