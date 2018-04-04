from flask import Flask, Response, request
import os
app=Flask(__name__)

@app.route('/')
def index():
    return 'welcome to sqilup data project'


@app.route('/health')
def health():
    return '200'



if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)
