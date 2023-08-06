import requests

def init(host, token):
    _client.init(host, token)

def push_model(model_name, path):
    _validate_model_name(model_name)
    _client.push_model(model_name, path)

def pull_model(model_name):
    _validate_model_name(model_name)
    _client.pull_model(model_name)

def _validate_model_name(model_name):
    if not isinstance(model_name, str):
        raise ValueError('"model_name" must be a string.')


class _Client:
    def __init__(self):
        self.token = ''
        self.host = ''

    def init(self, host, token):
        self.host = host
        self.token = token

    def _get_route(self):
        return f'http://{self.host}'

    def _get_headers(self):
        return {'Authorization': f'Bearer {self.token}'}

    def _check_init(self):
        if not self.host or not self.token:
            raise ValueError('Must call init() first, passing host, and token.')

    def push_model(self, model_name, path):
        self._check_init()

        with open(path, 'rb') as f:
            r = requests.post(
                f'{self._get_route()}/model',
                headers=self._get_headers(),
                files={'model_file': f},
                data={
                    'model_name': model_name
                }
            )

            if not r.ok:
                print(r.text)
                
            r.raise_for_status()


    def pull_model(self, model_name):
        self._check_init()

        r = requests.get(
            f'{self._get_route()}/model',
            headers=self._get_headers(),
            json={
                'model_name': model_name
            }
        )

        if not r.ok:
            print(r.text)

        r.raise_for_status()
        with open(model_name + '.pt', 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)

_client = _Client()
