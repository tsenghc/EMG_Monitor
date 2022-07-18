import flask
import numpy as np
import json
app = flask.Flask(__name__)
app.config["DEBUG"] = True



@app.route('/', methods=['GET'])
def home():
    data1 = np.random.normal(size=100)
    data =list(data1)
    return json.dumps(data)


app.run()