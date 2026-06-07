import http.client
import os
import unittest
from urllib.request import urlopen
import requests
import json
import pytest

BASE_URL = os.environ.get("BASE_URL")
DEFAULT_TIMEOUT = 2  # in secs

@pytest.mark.api
class TestApi(unittest.TestCase):
    
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_listtodos(self):
        print('---------------------------------------')
        print('Starting - integration test List TODO')
        url = BASE_URL + "/todos/"
        data = {
         "text": "Integration text example"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add Todo: ' + str(json_response))
        
        if 'id' in json_response:
            jsonbody = json_response
        else:
            jsonbody = json.loads(json_response.get('body', '{}'))
            
        ID_TODO = jsonbody['id']
        print('ID todo:' + ID_TODO)
        
        self.assertEqual(response.status_code, 200, f"Error en la petición API a {url}")
        self.assertEqual(jsonbody['text'], "Integration text example", f"Error en la petición API a {url}")
        
        response = requests.get(url)
        print('Response List Todo:' + str(response.json()))
        
        self.assertEqual(response.status_code, 200, f"Error en la petición API a {url}")
        self.assertTrue(response.json())
        print('End - integration test List TODO')

    def test_api_addtodo(self):
        print('---------------------------------------')
        print('Starting - integration test Add TODO')
        url = BASE_URL + "/todos/"
        data = {
         "text": "Integration text example"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add Todo: ' + str(json_response))
        
        if 'id' in json_response:
            jsonbody = json_response
        else:
            jsonbody = json.loads(json_response.get('body', '{}'))
            
        ID_TODO = jsonbody['id']
        print('ID todo:' + ID_TODO)
        
        self.assertEqual(response.status_code, 200, f"Error en la petición API a {url}")
        self.assertEqual(jsonbody['text'], "Integration text example", f"Error en la petición API a {url}")
        
        url_delete = url + ID_TODO
        response = requests.delete(url_delete)
        self.assertEqual(response.status_code, 200, f"Error en la petición API a {url_delete}")
        print('End - integration test Add TODO')

    def test_api_gettodo(self):
        print('---------------------------------------')
        print('Starting - integration test Get TODO')
        url = BASE_URL + "/todos/"
        data = {
         "text": "Integration text example - GET"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add Todo: ' + str(json_response))
        
        if 'id' in json_response:
            jsonbody = json_response
        else:
            jsonbody = json.loads(json_response.get('body', '{}'))
            
        ID_TODO = jsonbody['id']
        print('ID todo:' + ID_TODO)
        
        self.assertEqual(response.status_code, 200, f"Error en la petición API a {url}")
        self.assertEqual(jsonbody['text'], "Integration text example - GET", f"Error en la petición API a {url}")
        
        url_get = BASE_URL + "/todos/" + ID_TODO
        response = requests.get(url_get)
        json_response = response.json()
        print('Response Get Todo: ' + str(json_response))
        
        self.assertEqual(response.status_code, 200, f"Error en la petición API a {url_get}")
        self.assertEqual(json_response['text'], "Integration text example - GET", f"Error en la petición API a {url_get}")
        
        response = requests.delete(url_get)
        self.assertEqual(response.status_code, 200, f"Error en la petición API a {url_get}")
        print('End - integration test Get TODO')
    
    def test_api_updatetodo(self):
        print('---------------------------------------')
        print('Starting - integration test Update TODO')
        url = BASE_URL + "/todos/"
        data = {
         "text": "Integration text example - Initial"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add todo: ' + str(json_response))
        
        if 'id' in json_response:
            jsonbody = json_response
        else:
            jsonbody = json.loads(json_response.get('body', '{}'))
            
        ID_TODO = jsonbody['id']
        print('ID todo:' + ID_TODO)
        
        self.assertEqual(response.status_code, 200, f"Error en la petición API a {url}")
        self.assertEqual(jsonbody['text'], "Integration text example - Initial", f"Error en la petición API a {url}")
        
        url_update = BASE_URL + "/todos/" + ID_TODO
        data = {
         "text": "Integration text example - Modified",
         "checked": True
        }
        response = requests.put(url_update, data=json.dumps(data))
        json_response = response.json()
        print('Response Update todo: ' + str(json_response))
        
        self.assertEqual(response.status_code, 200, f"Error en la petición API a {url_update}")
        self.assertEqual(json_response['text'], "Integration text example - Modified", f"Error en la petición API a {url_update}")
        
        response = requests.get(url_update)
        json_response = response.json()
        print('Response Get Todo: ' + str(json_response))
        
        self.assertEqual(response.status_code, 200, f"Error en la petición API a {url_update}")
        self.assertEqual(json_response['text'], "Integration text example - Modified", f"Error en la petición API a {url_update}")
        
        response = requests.delete(url_update)
        self.assertEqual(response.status_code, 200, f"Error en la petición API a {url_update}")
        print('End - integration test Update TODO')

    def test_api_deletetodo(self):
        print('---------------------------------------')
        print('Starting - integration test Delete TODO')
        url = BASE_URL + "/todos/"
        data = {
         "text": "Integration text example - Initial"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add todo: ' + str(json_response))
        
        if 'id' in json_response:
            jsonbody = json_response
        else:
            jsonbody = json.loads(json_response.get('body', '{}'))
            
        ID_TODO = jsonbody['id']
        print('ID todo:' + ID_TODO)
        
        self.assertEqual(response.status_code, 200, f"Error en la petición API a {url}")
        self.assertEqual(jsonbody['text'], "Integration text example - Initial", f"Error en la petición API a {url}")
        
        url_delete = url + ID_TODO
        response = requests.delete(url_delete)
        
        self.assertEqual(response.status_code, 200, f"Error en la petición API a {url_delete}")
        print('Response Delete Todo:' + str(response))
        
        response = requests.get(url_delete)
        print('Response Get Todo ' + url_delete + ': ' + str(response))
        self.assertEqual(response.status_code, 404, f"Error en la petición API a {url_delete}")
        print('End - integration test Delete TODO')