import time
from iqoptionapi.stable_api import IQ_Option
Iq = IQ_Option("danieldiego052@gmail.com", "181006vania@")
Iq.connect()  # connect to iqoption

diego = 'USD'
money = 20
time_mode = 1
binary_aprovation = True
digital_aprovation = True

Money = []
ACTIVES = []
ACTION = []
expirations_mode = []

ALL_Asset = Iq.get_all_open_time()
for type_name, data in ALL_Asset.items():
    for Asset, value in data.items():
        if binary_aprovation == True:
            if type_name == 'binary':
                if value["open"] == True:
                    py_string = Asset
                    slice_object = slice(0, 3)
                    if py_string[slice_object] == diego:
                        Money.append(money)
                        ACTIVES.append(Asset)
                        ACTION.append("call")  # put
                        expirations_mode.append(time_mode)
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
                    if py_string[slice_object] == diego:
                        Iq.buy_digital_spot(Asset, money, "call", time_mode)
