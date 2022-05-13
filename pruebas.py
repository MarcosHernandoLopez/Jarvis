import json

data = {
    'lord': "prueba",
    'género': 'hombre'
}



with open('config.json', 'w') as f:
    data['lord'] = "Prueba 2"
    json.dump(data, f)
    f.close()

f2 = open('config.json')
data = json.load(f2)
print(data)