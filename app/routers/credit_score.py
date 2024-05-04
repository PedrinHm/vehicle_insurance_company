from fastapi import APIRouter, HTTPException, Query
import pandas as pd
from app.services import validation

router = APIRouter()

data = pd.read_csv('app/data/Car_Insurance_Claim.csv')

@router.get("/get_credit_score/")
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
        if (validation.check_age(age, record['AGE']) and
            record['GENDER'].lower() == gender.lower() and
            validation.check_experience(driving_experience, record['DRIVING_EXPERIENCE']) and
            record['EDUCATION'].lower() == education.lower() and
            record['INCOME'].lower() == income.lower() and
            validation.check_vehicle_year(vehicle_year, record['VEHICLE_YEAR']) and
            record['VEHICLE_TYPE'].lower() == vehicle_type.lower() and
            annual_mileage == record['ANNUAL_MILEAGE']):
            credit_score = record['CREDIT_SCORE']
            return {"credit_score": credit_score if pd.notna(credit_score) else None}
        else:
            raise HTTPException(status_code=400, detail="Registro encontrado, mas não tem Score.")
    else:
        raise HTTPException(status_code=404, detail="Nenhum registro correspondente encontrado")
