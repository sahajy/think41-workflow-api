from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Workflow(Base):
    __tablename__ = "workflows"
    id = Column(Integer, primary_key=True, index=True)
    workflow_str_id = Column(String, unique=True, index=True)
    name = Column(String)

    steps = relationship("Step", back_populates="workflow")

class Step(Base):
    __tablename__ = "steps"
    id = Column(Integer, primary_key=True, index=True)
    step_str_id = Column(String, index=True)
    description = Column(String)
    workflow_id = Column(Integer, ForeignKey("workflows.id"))

    workflow = relationship("Workflow", back_populates="steps")
    prerequisites = relationship("Dependency", foreign_keys="Dependency.step_id", back_populates="step")

class Dependency(Base):
    __tablename__ = "dependencies"
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"))
    step_id = Column(Integer, ForeignKey("steps.id"))
    prerequisite_step_id = Column(Integer, ForeignKey("steps.id"))

    step = relationship("Step", foreign_keys=[step_id])
    prerequisite = relationship("Step", foreign_keys=[prerequisite_step_id])
