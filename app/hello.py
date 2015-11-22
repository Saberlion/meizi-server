from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, jsonify

from spider.db import Meizi

app = Flask(__name__)
#app.config.from_pyfile('hello.cfg')

class res:
    code =''
    msg= ''
    res =[]
    def __init__(self, code, msg, res):
        self.code = code
        self.msg = msg
        self.res = res

@app.route('/')
def hello():
    return "hello"

@app.route('/meizi/<int:num>',methods=['GET'])
def meizi(num):
    meizis = Meizi.getRandomN(num)
    return jsonify(
        {
        "code":0,
        "msg":'success',
        "meizi":meizis
        }
    )

if __name__ == '__main__':
    app.run()