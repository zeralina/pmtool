from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    # WSJF
    business_value = Column(Float, nullable=False)
    time_criticality = Column(Float, nullable=False)
    risk_reduction = Column(Float, nullable=False)
    job_size = Column(Float, nullable=False)
    wsjf_score = Column(Float, nullable=True)

    # RICE
    rice_reach = Column(Float, nullable=True)
    rice_impact = Column(Float, nullable=True)
    rice_confidence = Column(Float, nullable=True)
    rice_effort = Column(Float, nullable=True)
    rice_score = Column(Float, nullable=True)

    # ICE
    ice_impact = Column(Float, nullable=True)
    ice_confidence = Column(Float, nullable=True)
    ice_ease = Column(Float, nullable=True)
    ice_score = Column(Float, nullable=True)

    status = Column(String, default="backlog")
    created_at = Column(DateTime, default=datetime.utcnow)

    metrics = relationship("Metric", back_populates="feature")


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    feature_id = Column(Integer, ForeignKey("features.id"))
    metric_name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    note = Column(Text, nullable=True)

    feature = relationship("Feature", back_populates="metrics")