from flask import Flask, send_file, request, make_response

app = Flask(__name__, static_url_path='', static_folder='static/dist/hack2019')

@app.route('/')
def index():
    return send_file('dist/hack2019/index.html')

@app.route('/board', methods=["POST"])
def board_list():
    # return "GET방식 요청에 회신 : {}".format(request.args.get('question'))
    j = request.json
    # article_id = request.values.get("article")
    # response = request
    return "hello {} {}".format(j['article'], type(j))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
