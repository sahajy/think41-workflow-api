from sqlalchemy.orm import Session
from models import Workflow, Step, Dependency
from schemas import WorkflowCreate, StepCreate, DependencyCreate
from fastapi import HTTPException
from collections import defaultdict, deque

def create_workflow(db: Session, wf: WorkflowCreate):
    existing = db.query(Workflow).filter_by(workflow_str_id=wf.workflow_str_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Workflow already exists")
    workflow = Workflow(**wf.dict())
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    return workflow

def add_step(db: Session, workflow_str_id: str, step_data: StepCreate):
    workflow = db.query(Workflow).filter_by(workflow_str_id=workflow_str_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    step = Step(step_str_id=step_data.step_str_id, description=step_data.description, workflow_id=workflow.id)
    db.add(step)
    db.commit()
    db.refresh(step)
    return step

def add_dependency(db: Session, workflow_str_id: str, dep_data: DependencyCreate):
    workflow = db.query(Workflow).filter_by(workflow_str_id=workflow_str_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if dep_data.step_str_id == dep_data.prerequisite_step_str_id:
        raise HTTPException(status_code=400, detail="A step cannot depend on itself")

    steps = db.query(Step).filter(Step.workflow_id == workflow.id).all()
    id_map = {step.step_str_id: step.id for step in steps}

    if dep_data.step_str_id not in id_map or dep_data.prerequisite_step_str_id not in id_map:
        raise HTTPException(status_code=404, detail="Step or prerequisite not found")

    dependency = Dependency(
        workflow_id=workflow.id,
        step_id=id_map[dep_data.step_str_id],
        prerequisite_step_id=id_map[dep_data.prerequisite_step_str_id]
    )
    db.add(dependency)
    db.commit()
    return dependency

def get_workflow_details(db: Session, workflow_str_id: str):
    workflow = db.query(Workflow).filter_by(workflow_str_id=workflow_str_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    steps = db.query(Step).filter_by(workflow_id=workflow.id).all()
    dependencies = db.query(Dependency).filter_by(workflow_id=workflow.id).all()

    id_to_str = {s.id: s.step_str_id for s in steps}
    str_to_desc = {s.step_str_id: s.description for s in steps}
    prereq_map = defaultdict(list)

    for d in dependencies:
        prereq_map[id_to_str[d.step_id]].append(id_to_str[d.prerequisite_step_id])

    details = [{
        "step_str_id": sid,
        "description": str_to_desc[sid],
        "prerequisites": prereq_map.get(sid, [])
    } for sid in str_to_desc]

    return {
        "workflow_str_id": workflow.workflow_str_id,
        "name": workflow.name,
        "steps": details
    }

def get_execution_order(db: Session, workflow_str_id: str):
    workflow = db.query(Workflow).filter_by(workflow_str_id=workflow_str_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    steps = db.query(Step).filter_by(workflow_id=workflow.id).all()
    dependencies = db.query(Dependency).filter_by(workflow_id=workflow.id).all()

    id_to_str = {s.id: s.step_str_id for s in steps}
    str_to_id = {s.step_str_id: s.id for s in steps}

    graph = defaultdict(list)
    indegree = defaultdict(int)

    for d in dependencies:
        a = id_to_str[d.prerequisite_step_id]
        b = id_to_str[d.step_id]
        graph[a].append(b)
        indegree[b] += 1

    q = deque([s for s in id_to_str.values() if indegree[s] == 0])
    result = []

    while q:
        current = q.popleft()
        result.append(current)
        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                q.append(neighbor)

    if len(result) != len(steps):
        raise HTTPException(status_code=400, detail="cycle_detected")

    return result
