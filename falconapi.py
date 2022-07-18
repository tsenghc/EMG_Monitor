import falcon
import numpy as np
import json
from waitress import serve

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.


class ThingsResource(object):
    def on_get(self, req, resp):

        data1 = np.random.normal(size=100)
        data = list(data1)
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps(data)


# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
things = ThingsResource()

# things will handle all requests to the '/things' URL path
app.add_route('/', things)
serve(app, host='127.0.0.1', port=8000)  # it is the same if i use serve(srv3)
