from bs4 import BeautifulSoup
import requests
import schedule
import time
from iqoptionapi.stable_api import IQ_Option
Iq = IQ_Option("danieldiego052@gmail.com", "181006vania@")
Iq.connect()  # connect to iqoption


resultados = []
money2 = 20
time_mode = 1
binary_aprovation = True
digital_aprovation = True

Money = []
ACTIVES = []
ACTION = []
expirations_mode = []

ALL_Asset = Iq.get_all_open_time()
headers = requests.utils.default_headers()
headers.update(
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'})
data = requests.get(
    'http://br.investing.com/economic-calendar/', headers=headers)


def consult(paridade):
    if data.status_code == requests.codes.ok:
        info = BeautifulSoup(data.text, 'html.parser')

        blocos = ((info.find('table', {'id': 'economicCalendarData'})).find(
            'tbody')).findAll('tr', {'class': 'js-event-item'})

    for blocos2 in blocos:
        impacto = str((blocos2.find('td', {'class': 'sentiment'})).get(
            'data-img_key')).replace('bull', '')
        horario = str(blocos2.get('data-event-datetime')).replace('/', '-')
        id = str(blocos2.get('id')).replace('eventRowId_', '')
        atual = (blocos2.find('td', {'id': 'eventActual_' + id})).text.strip().replace(
            'B', '').replace('K', '').replace('M', '').replace('%', '').replace('T', '').replace(',', '.')
        preview = (blocos2.find('td', {'id': 'eventPrevious_' + id})).text.strip().replace(
            'B', '').replace('K', '').replace('M', '').replace('%', '').replace('T', '').replace(',', '.')
        moeda = (blocos2.find(
            'td', {'class': 'left flagCur noWrap'})).text.strip()

        resultados.append({'par': moeda, 'horario': horario,
                          'impacto': impacto, 'id': id, 'atual': atual, 'preview': preview})


def job(paridade, id, prewiwer):
    if requests.get(
            'http://br.investing.com/economic-calendar/', headers=headers).status_code == requests.codes.ok:
        info = BeautifulSoup(requests.get(
            'http://br.investing.com/economic-calendar/', headers=headers).text, 'html.parser')

        blocos = ((info.find('table', {'id': 'economicCalendarData'})).find(
            'tbody')).findAll('tr', {'class': 'js-event-item'})

    for blocos2 in blocos:
        try:
            atual = (blocos2.find('td', {'id': 'eventActual_' + id})).text.strip().replace(
                'B', '').replace('K', '').replace('M', '').replace('%', '').replace('T', '').replace(',', '.')
        except AttributeError:
            print('Nao deu pra abrir o arquivo')
        else:
            if atual == '':
                job(paridade, id, prewiwer)
            else:
                if float(atual) >= float(prewiwer):
                    ALL_Asset = Iq.get_all_open_time()
                    for type_name, data in ALL_Asset.items():
                        for Asset, value in data.items():
                            if binary_aprovation == True:
                                if type_name == 'binary':
                                    if value["open"] == True:
                                        py_string = Asset
                                        slice_object = slice(0, 3)
                                        if py_string[slice_object] == paridade:
                                            check,id=Iq.buy(money2,Asset,'call',1)
                            if digital_aprovation == True:
                                if type_name == 'digital':
                                    if value["open"] == True:
                                        py_string = Asset
                                        slice_object = slice(0, 3)
                                        if py_string[slice_object] == paridade:
                                            Iq.buy_digital_spot(
                                                Asset, money2, "call", time_mode)
                else:
                    if float(atual) >= float(prewiwer):
                        ALL_Asset = Iq.get_all_open_time()
                        for type_name, data in ALL_Asset.items():
                            for Asset, value in data.items():
                                if binary_aprovation == True:
                                    if type_name == 'binary':
                                        if value["open"] == True:
                                            py_string = Asset
                                            slice_object = slice(0, 3)
                                            if py_string[slice_object] == paridade:
                                                Money.append(money2)
                                                ACTIVES.append(Asset)
                                                ACTION.append("put")  # put
                                                expirations_mode.append(
                                                    time_mode)
                                                id_list = Iq.buy_multi(
                                                    Money, ACTIVES, ACTION, expirations_mode)
                                                Money = []
                                                ACTIVES = []
                                                ACTION = []
                                                expirations_mode = []
                                if digital_aprovation == True:
                                    if type_name == 'digital':
                                        if value["open"] == True:
                                            py_string = Asset
                                            slice_object = slice(0, 3)
                                            if py_string[slice_object] == paridade:
                                                Iq.buy_digital_spot(
                                                    Asset, money2, "put", time_mode)


def loop():
    for info in resultados:
        if info['impacto'] == '3':
            py_string = info['horario']
            slice_object = slice(11, -3)
            schedule.run_pending()
            schedule.every().day.at(py_string[slice_object]).do(
                job, info['par'], info['id'], info['preview'])


consult('INICIO')
loop()

while True:
    schedule.run_pending()
    time.sleep(1)
