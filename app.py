from flask import Flask, send_file, request, make_response
from server.responseFunctions import login_func, incomeDeduction1, incomeDeduction2

app = Flask(__name__, static_url_path='', static_folder='dist/hack2019')

@app.route('/')
def index():
    return send_file('dist/hack2019/index.html')


@app.route('/login', methods=["POST"])
def login():
    a = request.json
    response = login_func(a['userid'])
    return response

@app.route('/summary1', methods=['POST'])
def summary1():
    a = request.json
    response = incomeDeduction1(a['userid'], a['total_salary'])
    return response

@app.route('/summary2', methods=['POST'])
def summary2():
    a = request.json
    response = incomeDeduction2(a)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')
