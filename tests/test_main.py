
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app=app)


def test_root():
    
    response = client.get("/")
    
    assert response.status_code == 200

def test_validate():
    
    response = client.post("/validate/26018835419")
    
    assert response.status_code == 200
    assert response.json() == {"valid": True}

def test_age():
    
    response = client.post("/age/26018835419")

    assert response.status_code == 200
    assert response.json() == {"age": 36}

def test_gender():
    
    response = client.post("gender/26018835419")

    assert response.status_code == 200
    assert response.json() == {"gender": "female"}

def test_validate():

    response = client.post("validate/26018835419")

    assert response.status_code == 200
    assert response.json() == {"valid": True}

def test_retrieve_valid_id_numbers():

    response = client.get("retrieve_valid_id_numbers/")

    expected = {'total_valid_id_numbers': 0}

    assert response.status_code == 200
    assert response.json().keys() == expected.keys()

def test_retrieve_stratified_valid_numbers():

    response = client.get("retrieve_stratified_valid_numbers/")
    
    expected =  {
                    'male':
                    {
                        '0-19': 0, 
                        '20-64': 0,
                        '>=65': 0
                    },
                    'female': 
                    {
                        '0-19': 0, 
                        '20-64': 0,
                        '>=65': 0
                    },
                        
                    }

    assert response.status_code == 200
    assert response.json().keys() == expected.keys()