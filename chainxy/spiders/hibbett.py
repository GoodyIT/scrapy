import sys
from scrapy.http import FormRequest
from scrapy.spider import BaseSpider
import requests
import pdb

class HibbettSpider(BaseSpider):
    name = 'hibbett'
    url = 'http://www.hibbett.com/stores/lookup_stores/'
    # you can set the user agent either in the settings or the spider

    headers = {
        "Accept":"*/*",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"en-GB,en-US;q=0.8,en;q=0.6",
        "Connection":"keep-alive",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie":"__utmt=1; ci_csrf_token=csrftoken; diamondcms=B2RXOVY2Vz1Qe1IpUWgHNQ85Aj5WfQZzVD1bIQIlWTcGaQRmAFldaQBmUyUFalp5AmgAO1JjBj8PK1JhA29XYANsDWYCNwNnDzgMMQRnWTEHZldlVjtXMlA1Um9RMQdiD2oCNFZtBmFUO1thAjNZbQY1BDgAMF1iADFTJQVqWnkCaAA5UmEGPw8rUj0DelcOA24NYAIyA3YPagxzBHFZJgc%2BV3BWOFc2UDBSYFFwBzIPOAIqVmkGLlRuW2ACeFlrBjUEKgA9XXMAOFM2BWFaMAJwAH1SIgZgD3tSCwNrVzYDag1qAiIDJg80DHMEOFk1BzVXNlY4VyVQTVI1USgHbQ9lAmhWPgYvVG1bfAJmWX4GLgRQADddMQA5UycFHVpjAjwAfVIpBiUPcVJsAzxXDgM5DTACfwMkD04McARyWWgHYFdUVmdXZVBLUjNRJgcrDzwCN1ZoBi5Ua1tkAnZZdgZNBEAAUl1NAE5TKwVxWmYCOwBjUjQGJQ9OUjEDaVc6A2ANLQJ2A0cPZwxyBG1ZaQdgVyxWN1cwUC5SalF8BzYPMAI8VmgGLlRpW2MCZll%2BBlUEaQBgXWEAcFNuBX5aPwJhAD9SfwY2Dz9SdgMxVyIDNQ01AmUDPg8tDGwEY1l3B3FXXFZjV2RQdFIzUSQHbQ99An1WfQY7VDFbaAJnWWoGPwQ7ADddNwA6UzIFZ1o7AmkAdQ%3D%3D; __atuvc=4%7C17; __atuvs=58ffd270258be894001; __utma=191247923.82098203.1493157453.1493157453.1493160561.2; __utmb=191247923.2.10.1493160561; __utmc=191247923; __utmz=191247923.1493157453.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
        "Host":"www.hibbett.com",
        "Origin":"http://www.hibbett.com",
        "Referer":"http://www.hibbett.com/stores/",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest"
    }
    def start_requests(self):
        URL = 'http://www.hibbett.com/stores/'
        client = requests.session()
        client.get(URL)
        ci_csrf_token = client.cookies['ci_csrf_token']
        self.headers['Cookie'] = self.headers['Cookie'].replace('csrftoken', ci_csrf_token)
        data = {
            'ci_csrf_token' : ci_csrf_token,
            'type': 'state',
            'value': '4'
        }
        # no need for dont_filter
        yield FormRequest(url=self.url, formdata=data, headers=self.headers, callback=self.parseStore)

    def parseStore(self, response):
        pdb.set_trace()
        print response.url