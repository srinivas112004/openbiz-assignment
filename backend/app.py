"""Backend API for Openbiz Assignment.

FastAPI app that:
- Serves scraped schema to frontend
- Validates and stores submissions in PostgreSQL
- Lists stored submissions

Author: Your Name
"""

import os, json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr, ValidationError
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import select

DATABASE_URL = os.getenv('DATABASE_URL','postgresql://postgres:postgres@db:5432/openbiz')
SCHEMA_PATH = os.getenv('SCHEMA_PATH','/data/schema.json')

engine = create_engine(DATABASE_URL, echo=False)
metadata = MetaData()
submissions = Table('submissions', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', String(200)),
                    Column('pan', String(20)),
                    Column('aadhaar', String(20)),
                    Column('email', String(200)),
                    Column('pin', String(20)),
                    Column('city', String(200)),
                    Column('state', String(200))
                   )
metadata.create_all(engine)

app = FastAPI(title='Openbiz Backend')

# Utility function to load the most recent schema from shared volume
def load_schema():
    try:
        with open(SCHEMA_PATH,'r',encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

@app.get("/schema")
def get_schema():
    return load_schema()

# Pydantic model to validate incoming form submissions
class Submission(BaseModel):
    name: Optional[str]
    pan: Optional[constr(regex=r'^[A-Za-z]{5}[0-9]{4}[A-Za-z]{1}$')]
    aadhaar: Optional[constr(regex=r'^[0-9]{12}$')]
    email: Optional[str]
    pin: Optional[str]
    city: Optional[str]
    state: Optional[str]

@app.post("/submit")
def submit(payload: Submission):
    # Convert validated pydantic model to dict
    try:
        data = payload.dict()
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    try:
        with engine.connect() as conn:
            ins = submissions.insert().values(
                name=data.get('name'),
                pan=data.get('pan'),
                aadhaar=data.get('aadhaar'),
                email=data.get('email'),
                pin=data.get('pin'),
                city=data.get('city'),
                state=data.get('state')
            )
            res = conn.execute(ins)
            conn.commit()
            return {"ok":True, "id": res.inserted_primary_key[0]}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/submissions")
def list_submissions():
    try:
        with engine.connect() as conn:
            q = select([submissions])
            rows = conn.execute(q).fetchall()
            return [dict(r) for r in rows]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
