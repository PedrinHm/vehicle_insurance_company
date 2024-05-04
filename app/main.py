from fastapi import FastAPI, HTTPException, Query
import pandas as pd
import re

app = FastAPI()

# Carregar o dataset
data = pd.read_csv('data/Car_Insurance_Claim.csv')

def clean_numeric_input(value):
    """ Limpa o input numérico, removendo letras e caracteres não numéricos. """
    return int(re.sub('[^\d]', '', value))

def check_age(value, range_str):
    """ Verifica se a idade está dentro do intervalo especificado. """
    if '+' in range_str:
        start = int(range_str[:-1])
        return value >= start
    return False

def check_experience(value, range_str):
    """ Verifica se a experiência de condução está dentro do intervalo especificado. """
    if '-' in range_str:
        low, high = map(int, range_str.replace('y', '').split('-'))
        return low <= value <= high
    return False

def check_vehicle_year(value, range_str):
    """ Verifica se o ano do veículo está dentro do intervalo especificado. """
    if 'before' in range_str:
        year = int(range_str.split(' ')[1])
        return value < year
    elif 'after' in range_str:
        year = int(range_str.split(' ')[1])
        return value >= year
    return False

@app.get("/get_credit_score/")
async def get_credit_score(
    id: int = Query(..., description="ID"),
    age: int = Query(..., description="Idade"),
    gender: str = Query(..., description="Gênero"),
    driving_experience: int = Query(..., description="Experiência de condução"),
    education: str = Query(..., description="Nível de educação"),
    income: str = Query(..., description="Renda"),
    vehicle_year: int = Query(..., description="Categoria do ano do veículo"),
    vehicle_type: str = Query(..., description="Tipo do veículo"),
    annual_mileage: int = Query(..., description="Quilometragem anual")
):
    filtered_data = data[data['ID'] == id]
    if not filtered_data.empty:
        record = filtered_data.iloc[0]
        if (check_age(age, record['AGE']) and
            record['GENDER'].lower() == gender.lower() and
            check_experience(driving_experience, record['DRIVING_EXPERIENCE']) and
            record['EDUCATION'].lower() == education.lower() and
            record['INCOME'].lower() == income.lower() and
            check_vehicle_year(vehicle_year, record['VEHICLE_YEAR']) and
            record['VEHICLE_TYPE'].lower() == vehicle_type.lower() and
            annual_mileage == record['ANNUAL_MILEAGE']):
            credit_score = record['CREDIT_SCORE']
            return {"credit_score": credit_score if pd.notna(credit_score) else None}
        else:
            raise HTTPException(status_code=400, detail="Registro encontrado, mas não tem Score.")
    else:
        raise HTTPException(status_code=404, detail="Nenhum registro correspondente encontrado")
