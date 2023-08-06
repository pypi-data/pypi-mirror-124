import numpy as np
import pymongo
from assignmentcalculatorunimib.calculator import somma, sottrazione

try:
    client = pymongo.MongoClient('localhost', 27017)
    client.server_info()
except pymongo.errors.ServerSelectionTimeoutError:
    client = pymongo.MongoClient('mongodb', 27017)

proc_svil = client['proc_svil']
assignment_1 = proc_svil['first']


def scelta_operatore(operatore, array_1, array_2):
    if operatore == "somma":
        return True, save_to_mongo(somma(array_1, array_2))
    if operatore == "sottrazione":
        return True, save_to_mongo(sottrazione(array_1, array_2))
    return False, -1


def crea_array(value_1, value_2, value_3):
    return np.array([value_1, value_2, value_3])


def save_to_mongo(array):
    assignment_1.insert_one({
        'element': array.tolist()
    })
    return array
