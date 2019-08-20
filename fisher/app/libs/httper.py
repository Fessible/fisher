# 请求数据

import requests


class HTTP:

    # 默认返回json格式数据
    @classmethod
    def get(cls, url, return_json=True):
        r = requests.get(url)

        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text
