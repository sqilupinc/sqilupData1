from flask import Flask
from flask import Flask,json,jsonify
from flask import request
import subprocess
from subprocess import Popen, PIPE
import datetime

now = datetime.datetime.now()

app = Flask(__name__)

@app.route('/transapi', methods = ['POST'])
def postJsonHandler():
    print (request.is_json)
    content = request.get_json()
    print (content)

    process = subprocess.Popen(['python' , '/home/ec2-user/spark/STOCK_A_US.py' ], stdout=subprocess.PIPE)
    out, err = process.communicate()
    print(out)
    if process.returncode == 0:
     print('Tranformaton process successful')
     Transoutput='SUCESS'
    elif process.returncode == 1:
     print('Tranformation error occured')
     Transoutput='ERROR'
    else:
     assert process.returncode > 1
     print('error occurred')
     Transoutput='ERROR'
    return 'Transform API execition completed at -'+ str(now) + ',' +  ' Excution Status -' + Transoutput

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)