from fastapi.testclient import TestClient
from main import app
import sys
import os

from models.models import Sheep

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

client = TestClient(app)

def test_read_sheep():
    response = client.get("/sheep/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }

def test_add_sheep():
     sheep_data_name = {
         "id": 7,
         "name": "F1",
         "breed": "Racecar",
         "sex": "ram"
     }

     response = client.post("/sheep/", json=sheep_data_name)

     assert response.status_code == 201

     response_data = response.json()
     assert response_data["id"] == sheep_data_name["id"]
     assert response_data["name"] == sheep_data_name["name"]
     assert response_data["breed"] == sheep_data_name["breed"]
     assert response_data["sex"] == sheep_data_name["sex"]

     new_sheep_id = response_data["id"]
     get_response = client.get(f"/sheep/{new_sheep_id}")
     assert get_response.status_code == 200
     get_data = get_response.json()
     assert get_data["id"] == sheep_data_name["id"]
     assert get_data["name"] == sheep_data_name["name"]
     assert get_data["breed"] == sheep_data_name["breed"]
     assert get_data["sex"] == sheep_data_name["sex"]

def test_delete_sheep():
    delete_sheep = {
        "id": 8,
        "name": "F2",
        "breed": "Racecar",
        "sex": "ram"
    }

    create_response = client.post("/sheep/", json=delete_sheep)
    assert create_response.status_code == 201
    sheep_id = create_response.json()["id"]

    delete_response = client.delete(f"/sheep/{sheep_id}")
    assert delete_response.status_code == 204

    try:
        get_response = client.get(f"/sheep/{sheep_id}")
        assert get_response.status_code == 404 or get_response.json() is None
    except Exception as e:
        assert "ResponseValidationError" in str(type(e).__name__)

def test_update_sheep():
    update_sheep = {
        "id": 9,
        "name": "F3",
        "breed": "Racecar",
        "sex": "ewe"
    }

    create_response = client.post("/sheep/", json=update_sheep)
    assert create_response.status_code == 201
    sheep_id = create_response.json()["id"]

    update_data = {
        "name": "NewName",
        "breed": "NewBreed",
        "sex": "ram"
    }

    update_response = client.put(f"/sheep/{sheep_id}", json=update_data)
    assert update_response.status_code == 200

    updated_sheep = update_response.json()
    assert updated_sheep["id"] == sheep_id
    assert updated_sheep["name"] == update_data["name"]
    assert updated_sheep["breed"] == update_data["breed"]
    assert updated_sheep["sex"] == update_data["sex"]

    get_response = client.get(f"/sheep/{sheep_id}")
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data["id"] == sheep_id
    assert get_data["name"] == update_data["name"]
    assert get_data["breed"] == update_data["breed"]
    assert get_data["sex"] == update_data["sex"]


def test_read_all_sheep():
    response = client.get("/sheep/")
    assert response.status_code == 200

    sheep_list = response.json()
    assert isinstance(sheep_list, list)

    assert any(s["id"] == 1 and s["name"] == "Spice" for s in sheep_list)

    for sheep in sheep_list:
        assert "id" in sheep
        assert "name" in sheep
        assert "breed" in sheep
        assert "sex" in sheep