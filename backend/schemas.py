from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MetricBase(BaseModel):
    metric_name: str
    value: float
    date: Optional[datetime] = None
    note: Optional[str] = None

class MetricCreate(MetricBase):
    pass

class Metric(MetricBase):
    id: int
    feature_id: int

    class Config:
        from_attributes = True

class FeatureBase(BaseModel):
    name: str
    description: Optional[str] = None
    business_value: float
    time_criticality: float
    risk_reduction: float
    job_size: float
    rice_reach: Optional[float] = None
    rice_impact: Optional[float] = None
    rice_confidence: Optional[float] = None
    rice_effort: Optional[float] = None
    ice_impact: Optional[float] = None
    ice_confidence: Optional[float] = None
    ice_ease: Optional[float] = None

class FeatureCreate(FeatureBase):
    pass

class FeatureUpdate(BaseModel):
    status: Optional[str] = None
    business_value: Optional[float] = None
    time_criticality: Optional[float] = None
    risk_reduction: Optional[float] = None
    job_size: Optional[float] = None

class Feature(FeatureBase):
    id: int
    wsjf_score: Optional[float] = None
    rice_score: Optional[float] = None
    ice_score: Optional[float] = None
    status: str
    created_at: datetime
    metrics: list[Metric] = []

    class Config:
        from_attributes = True