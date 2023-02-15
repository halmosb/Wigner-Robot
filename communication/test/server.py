import requests

x = requests.get('http://148.6.183.54:5000/login?nm=alma')
print(x.text)

x = requests.post('http://148.6.183.54:5000/login', {"nm": "körte"})
print(x.text)