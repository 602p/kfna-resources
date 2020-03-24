from flask import Flask
import os
app = Flask(__name__)

@app.route('/rebuild')
def rebuild():
    return "<html><body><b>After you click this it may take a few seconds to work... don't click it multiple times please :)</b><br/><a href=\"/rebuild/do\">Rebuild</a></body></html>"

@app.route('/rebuild/do')
def rebuild_do():
    return "<html><body><pre>"+os.popen('bash build.sh', 'r').read()+"</pre><br/><a href=\"/restaurants\">Back</a></body></html>"