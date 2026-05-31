from sqlalchemy.orm import Session
import sys, os
sys.path.append(os.path.dirname(__file__))
import models, schemas

def calculate_scores(feature: schemas.FeatureCreate):
    wsjf = round(
        (feature.business_value + feature.time_criticality + feature.risk_reduction)
        / feature.job_size, 2
    )

    rice = None
    if all([feature.rice_reach, feature.rice_impact, feature.rice_confidence, feature.rice_effort]):
        rice = round(
            (feature.rice_reach * feature.rice_impact * feature.rice_confidence)
            / feature.rice_effort, 2
        )

    ice = None
    if all([feature.ice_impact, feature.ice_confidence, feature.ice_ease]):
        ice = round(
            feature.ice_impact * feature.ice_confidence * feature.ice_ease, 2
        )

    return wsjf, rice, ice


def get_features(db: Session):
    return db.query(models.Feature).order_by(models.Feature.wsjf_score.desc()).all()


def get_feature(db: Session, feature_id: int):
    return db.query(models.Feature).filter(models.Feature.id == feature_id).first()


def create_feature(db: Session, feature: schemas.FeatureCreate):
    wsjf, rice, ice = calculate_scores(feature)
    db_feature = models.Feature(
        **feature.model_dump(),
        wsjf_score=wsjf,
        rice_score=rice,
        ice_score=ice
    )
    db.add(db_feature)
    db.commit()
    db.refresh(db_feature)
    return db_feature


def update_feature(db: Session, feature_id: int, feature: schemas.FeatureUpdate):
    db_feature = get_feature(db, feature_id)
    for key, value in feature.model_dump(exclude_none=True).items():
        setattr(db_feature, key, value)
    db.commit()
    db.refresh(db_feature)
    return db_feature


def delete_feature(db: Session, feature_id: int):
    db_feature = get_feature(db, feature_id)
    db.delete(db_feature)
    db.commit()
    return db_feature


def get_metrics(db: Session, feature_id: int):
    return db.query(models.Metric).filter(models.Metric.feature_id == feature_id).all()


def create_metric(db: Session, feature_id: int, metric: schemas.MetricCreate):
    db_metric = models.Metric(**metric.model_dump(), feature_id=feature_id)
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric