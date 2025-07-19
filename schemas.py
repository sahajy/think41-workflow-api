from pydantic import BaseModel
from typing import List, Optional

class WorkflowCreate(BaseModel):
    workflow_str_id: str
    name: str

class StepCreate(BaseModel):
    step_str_id: str
    description: str

class DependencyCreate(BaseModel):
    step_str_id: str
    prerequisite_step_str_id: str

class StepDetail(BaseModel):
    step_str_id: str
    description: str
    prerequisites: List[str]

class WorkflowDetails(BaseModel):
    workflow_str_id: str
    name: str
    steps: List[StepDetail]
