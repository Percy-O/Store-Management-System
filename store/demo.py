import requests
import json



host = 'http://127.0.0.1:8000/'

def login():
	global token_output

	data={'username':'Percy',
		'password':'holawahlay'
		}

	endpoint = host +  'auth/jwt/create'
	response = requests.post(endpoint,data=data)
	response_dict = json.loads(response.text)
	print(response_dict)
	token_output = response_dict['access']
	# print(token_output)
login()


def view():

	# print(token_output)
	headers = {
		'Authorization':f'JWT {token_output}'
	}
	# data={
	# 	'user_id ':1
	# }
	endpoint = host + 'api/staff/me'
	response = requests.get(endpoint,headers=headers,)
	response_dict = json.loads(response.text)
	print(response_dict)

view()
