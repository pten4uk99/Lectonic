import requests

r = requests.post('http://127.0.0.1:8000/registration/', data = {'login':'Gadya', 'email': 'gad@mail.ru', 'pass':'12345', 'pass_repeat':'12345'})
print (r.text)