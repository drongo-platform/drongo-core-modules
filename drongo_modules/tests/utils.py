import json
import time
import urllib3

from threading import Thread

from nest import Nest


class APIClient(object):
    def __init__(self, api_url):
        self.http = urllib3.PoolManager()
        self.api_url = api_url
        self.headers = {'connection': 'keep-alive'}

    def set_auth_token(self, token):
        if token is None:
            del self.headers['Authorization']
        else:
            self.headers['Authorization'] = token

    def request(self, *args, **kwargs):
        while True:
            try:
                return self.http.request(*args, **kwargs)
            except:
                time.sleep(0.5)

    def get(self, url, params=None):
        url = self.api_url + url
        headers = {}
        headers.update(self.headers)
        r = self.request('GET', url, params, headers=headers)
        return json.loads(r.data.decode('utf-8'))

    def post(self, url, payload):
        url = self.api_url + url
        headers = {'Content-Type': 'application/json'}
        headers.update(self.headers)
        r = self.request(
            'POST',
            url,
            body=json.dumps(payload).encode('utf-8'),
            headers=headers
        )
        return json.loads(r.data.decode('utf-8'))

    def put(self, url, payload):
        url = self.api_url + url
        headers = {'Content-Type': 'application/json'}
        headers.update(self.headers)
        r = self.request(
            'PUT',
            url,
            body=json.dumps(payload).encode('utf-8'),
            headers=headers
        )
        return json.loads(r.data.decode('utf-8'))

    def delete(self, url):
        url = self.api_url + url
        headers = {}
        headers.update(self.headers)
        r = self.request('DELETE', url, headers=headers)
        return json.loads(r.data.decode('utf-8'))


class AppServer(object):
    def __init__(self, app):
        self.app = app
        self.thread = None

    def run(self):
        self.nest = Nest(app=self.app, port=12345)
        self.thread = Thread(target=self.nest.run)
        self.thread.start()
        time.sleep(0.5)

    def stop(self):
        self.nest.shutdown()
        self.thread.join()
