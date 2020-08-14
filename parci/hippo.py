import requests
import json

import time

import datetime

start_time = time.time()

http_proxy = "http://80.187.140.74:8080"

proxyDict = {
    "http": http_proxy,
}

# url_template = "http://parci.free.fr/include/hippodromes.php?option=2"  # dd/MM/yyyy

# url_reunion_template = "http://parci.free.fr/include/hippodrome_corde_sol.php?idHippodrome=%s"


url_reunion = 'http://parci.free.fr/include/reunions/reunions.php?idReunion=%s'

# base = datetime.datetime.today() - datetime.timedelta(days=1)
# date_list = [(base - datetime.timedelta(days=x)).strftime('%d/%m/%Y')
#              for x in range(10)]

for x in range(25000,26000):
    url = url_reunion % x
    # print(url)
    r = requests.get(url, proxies=proxyDict)
    time.sleep(0.25)
    if r.status_code == 200:
        json_res = json.loads(r.text)
        print('Reunion = ', x, ', typeReu = ', json_res['typeReunion'])
        # with open('data/%s.json' % (date.replace('/', '')), 'w', encoding='utf-8') as f:
        #     json.dump(json_res, f)

        # for result in json_res['results']:
        #     url_reunion = url_reunion_template % result['idReunion']
        #     r_reunion = requests.get(url_reunion, proxies=proxyDict)
        #     time.sleep(0.25)
        #     with open('data/%s-%s.json' % (date.replace('/', ''), result['idReunion']), 'w', encoding='utf-8') as f:
        #         json_reunion_res = json.loads(r_reunion.text)
        #         json.dump(json_reunion_res, f)

    else:
        print(r)
# for date in date_list:
#     print(date)
#     url = url_template % date
#     r = requests.get(url, proxies=proxyDict)

#     if r.status_code == 200:
#         json_res = json.loads(r.text)

#         with open('data/%s.json' % (date.replace('/', '')), 'w', encoding='utf-8') as f:
#             json.dump(json_res, f)

#         for result in json_res['results']:
#             url_reunion = url_reunion_template % result['idReunion']
#             r_reunion = requests.get(url_reunion, proxies=proxyDict)
#             time.sleep(0.25)
#             with open('data/%s-%s.json' % (date.replace('/', ''), result['idReunion']), 'w', encoding='utf-8') as f:
#                 json_reunion_res = json.loads(r_reunion.text)
#                 json.dump(json_reunion_res, f)

#     else:
#         print(r)

print("--- %s seconds ---" % (time.time() - start_time))