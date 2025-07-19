from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import crud
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/workflows")
def create_workflow(workflow: schemas.WorkflowCreate, db: Session = Depends(get_db)):
    return crud.create_workflow(db, workflow)

@app.post("/workflows/{workflow_str_id}/steps")
def add_step(workflow_str_id: str, step: schemas.StepCreate, db: Session = Depends(get_db)):
    return crud.add_step(db, workflow_str_id, step)

@app.post("/workflows/{workflow_str_id}/dependencies")
def add_dependency(workflow_str_id: str, dep: schemas.DependencyCreate, db: Session = Depends(get_db)):
    return crud.add_dependency(db, workflow_str_id, dep)

@app.get("/workflows/{workflow_str_id}/details", response_model=schemas.WorkflowDetails)
def get_workflow_details(workflow_str_id: str, db: Session = Depends(get_db)):
    return crud.get_workflow_details(db, workflow_str_id)

@app.get("/workflows/{workflow_str_id}/execution-order")
def get_execution_order(workflow_str_id: str, db: Session = Depends(get_db)):
    return {"execution_order": crud.get_execution_order(db, workflow_str_id)}
