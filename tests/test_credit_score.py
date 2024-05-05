import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.routers.credit_score import get_credit_score  # Importa a função diretamente
# Demais imports necessários para seu teste

from fastapi.testclient import TestClient
from app.main import app  # Ajuste a importação conforme a definição do seu app
import pytest

client = TestClient(app)

def test_get_credit_score_success():
    response = client.get(
        "/get_credit_score/",
        params={
            'id': 569520,
            'age': 66,
            'gender': 'female',
            'driving_experience': 9,
            'education': 'high school',
            'income': 'upper class',
            'vehicle_year': 2016,
            'vehicle_type': 'sedan',
            'annual_mileage': 12000
        }
    )
    assert response.status_code == 200
    assert response.json() == {'credit_score': 0.629027313918201}

def test_get_credit_score_not_found():
    response = client.get(
        "/get_credit_score/",
        params={
            'id': 999, 
            'age': 30,
            'gender': 'male',
            'driving_experience': 10,
            'education': 'college',
            'income': 'high',
            'vehicle_year': 2015,
            'vehicle_type': 'sedan',
            'annual_mileage': 12000
        }
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Nenhum registro correspondente encontrado'}

def test_get_credit_score_not_found_people():
    response = client.get(
        "/get_credit_score/",
        params={
            'id': 24851, 
            'age': 17,
            'gender': 'male',
            'driving_experience': 9,
            'education': 'none',
            'income': 'poverty',
            'vehicle_year': 2014,
            'vehicle_type': 'sedan',
            'annual_mileage': 12000
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Registro encontrado, mas não tem Score.'}