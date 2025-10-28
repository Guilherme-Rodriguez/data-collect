# %%

import requests
import datetime
import json

# %%

class Collector():

    def __init__(self, url, instance_name):
        self.url = url
        self.instance_name = instance_name

    def get_content(self, **kwargs):
        resp = requests.get(self.url, params = kwargs)
        return resp

    def save_parquet(self, data):
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f")
        df = pd.DataFrame(data)
        df.to_parquet('data/{self.instance_name}/parquet/{now}.parquet', index = False)

    def save_json(self, data):
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f")
        with open('data/episodios/json/{now}.json', 'w') as open_file:
            json.dump(data, open_file)

    def save_data(self, data, format = 'json'):
        if format == 'json':
            self.save_json(data)

        elif format == 'parquet':
            self.save_parquet(data)

    def get_and_save(self, save_format = 'json', **kwargs):
        resp = self.get_content(kwargs)
        if resp.status_code == 200:
            self.save_data(data.json())
        else:
            print(f"Request sem sucesso: {resp.status_code}", resp.json())



# %%



# %%
