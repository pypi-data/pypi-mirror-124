import gzip
import io
import json
import os
import pandas as pd
import requests
import time
import zipfile

class EasieUsertb():
    def __getitem__(self, k):
        try:
            return getattr(self, k)
        except:
            return None

    def __init__(self, username, developer_key, url_api="https://api.easiedata.com", workspace_abs_path=None):
        self.url_api = url_api
        self.username = username
        self.developer_key = developer_key

        if workspace_abs_path is None:
            workspace_abs_path = os.getcwd()

        self.path = workspace_abs_path + '/'
        self.headers = {
            'Authorization': json.dumps({
                'username': self.username,
                'developer_key':self.developer_key
            })
        }

        return None

    def post_easieusertb(
        self, action, table_name, params={}, df=None):

        try:
            files = None
            if df is not None:
                timedelta_cols = [col for col in df.columns if df[col].dtype == 'timedelta64[ns]']
                df[timedelta_cols] = df[timedelta_cols].astype(str)

                file_name = table_name + 'temp.json'
                json_string = df.to_json(orient='table')

                f = io.BytesIO()
                z = zipfile.ZipFile(f, "w",zipfile.ZIP_DEFLATED, False) 

                z.writestr(file_name,json_string)
                z.close()
                f.seek(0)

                files = {'data': ('df', f, 'application/json')} 

                r = requests.post(
                    self.url_api + '/developer/add_to_queue_post',
                    headers=self.headers,
                    data={'action':action, 'front_tablename': table_name, 'params':json.dumps(params)},
                    files=files
                )

                f.close()

            else:
                r = requests.post(
                    self.url_api + '/developer/add_to_queue_post',
                    headers=self.headers,
                    data={'action':action, 'front_tablename': table_name, 'params':json.dumps(params)},
                    files=files
                )

            self.http_status = r.status_code
            try:
                self.res = r.json()
            except:
                self.res = r

            if self.http_status != 200:
                return self

            self.queue_pk = self.res['data'][0]
            self.token = self.res['data'][1]

            done = 0
            while(not done):
                time.sleep(2)
                r = requests.get(
                    self.url_api + '/developer/check_if_done_post',
                    headers=self.headers,
                    data={'pk': self.queue_pk, 'token': self.token, 'method': 'POST'}
                )

                self.http_status = r.status_code
                try:
                    self.res = r.json()
                except:
                    self.res = r

                if self.http_status != 200:
                    return self

                done = self.res['data']

            r = requests.get(
                self.url_api + '/developer/easie_usertb_post/%d' % self.queue_pk,
                headers=self.headers,
                data={'token': self.token}
            )

            self.http_status = r.status_code
            try:
                self.res = r.json()
            except:
                self.res = r

            if self.http_status != 200:
                return self


        except:
            self.res = {
                'success': False,
                'front_msg': 'Something is wrong, contact support!'
            }


        return self

    def get_easieusertb(self, table_name, params={}):
        try:
            r = requests.post(
                self.url_api + '/developer/add_to_queue_get',
                headers=self.headers,
                data={'action':'get_df', 'front_tablename': table_name, 'params': json.dumps(params)}
            )

            self.http_status = r.status_code
            try:
                self.res = r.json()
            except:
                self.res = r

            if self.http_status != 200:
                return self

            self.queue_pk = self.res['data'][0]
            self.token = self.res['data'][1]

            done = 0
            while(not done):
                time.sleep(2)
                r = requests.get(
                    self.url_api + '/developer/check_if_done_get',
                    headers=self.headers,
                    data={'pk': self.queue_pk, 'token': self.token, 'method': 'GET'}
                )

                self.http_status = r.status_code
                try:
                    self.res = r.json()
                except:
                    self.res = r

                if self.http_status != 200:
                    return self

                done = self.res['data']

            r = requests.get(
                self.url_api + '/developer/easie_usertb_get/%d' % self.queue_pk,
                headers=self.headers,
                data={'token': self.token}
            )

            self.http_status = r.status_code
            if self.http_status == 200:

                z = zipfile.ZipFile(io.BytesIO(r.content))
                data = z.read(z.namelist()[0])
                self.df = pd.read_json(data, orient='table')
                self.res = {
                    'success': True,
                    'front_msg': 'Success!'
                }

            else:
                try:
                    self.res = r.json()
                except:
                    self.res = r

        except:
            self.res = {
                'success': False,
                'front_msg': 'Something is wrong, contact support!'
            }

        return self
