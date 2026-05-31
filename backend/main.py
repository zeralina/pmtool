from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Prioritization Tool")


@app.get("/features", response_model=list[schemas.Feature])
def get_features(db: Session = Depends(get_db)):
    return crud.get_features(db)


@app.get("/features/{feature_id}", response_model=schemas.Feature)
def get_feature(feature_id: int, db: Session = Depends(get_db)):
    feature = crud.get_feature(db, feature_id)
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    return feature


@app.post("/features", response_model=schemas.Feature)
def create_feature(feature: schemas.FeatureCreate, db: Session = Depends(get_db)):
    return crud.create_feature(db, feature)


@app.put("/features/{feature_id}", response_model=schemas.Feature)
def update_feature(feature_id: int, feature: schemas.FeatureUpdate, db: Session = Depends(get_db)):
    db_feature = crud.get_feature(db, feature_id)
    if not db_feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    return crud.update_feature(db, feature_id, feature)


@app.delete("/features/{feature_id}")
def delete_feature(feature_id: int, db: Session = Depends(get_db)):
    db_feature = crud.get_feature(db, feature_id)
    if not db_feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    crud.delete_feature(db, feature_id)
    return {"message": "Feature deleted"}


@app.get("/features/{feature_id}/metrics", response_model=list[schemas.Metric])
def get_metrics(feature_id: int, db: Session = Depends(get_db)):
    return crud.get_metrics(db, feature_id)


@app.post("/features/{feature_id}/metrics", response_model=schemas.Metric)
def create_metric(feature_id: int, metric: schemas.MetricCreate, db: Session = Depends(get_db)):
    db_feature = crud.get_feature(db, feature_id)
    if not db_feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    return crud.create_metric(db, feature_id, metric)