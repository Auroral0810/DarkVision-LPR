from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List, Tuple
from app.models.recognition import RecognitionTask, RecognitionRecord, RecognitionModel
from app.schemas.admin.recognition import TaskListParams, RecordListParams, RecognitionModelCreate, RecognitionModelUpdate

def list_tasks(db: Session, params: TaskListParams) -> Tuple[List[RecognitionTask], int]:
    query = db.query(RecognitionTask)
    
    if params.status:
        query = query.filter(RecognitionTask.status == params.status)
    if params.task_type:
        query = query.filter(RecognitionTask.task_type == params.task_type)
    if params.user_id:
        query = query.filter(RecognitionTask.user_id == params.user_id)
        
    total = query.count()
    tasks = query.order_by(desc(RecognitionTask.created_at)).offset((params.page - 1) * params.page_size).limit(params.page_size).all()
    return tasks, total

def delete_task(db: Session, task_id: int) -> bool:
    task = db.query(RecognitionTask).filter(RecognitionTask.id == task_id).first()
    if not task:
        return False
    # Also delete associated results if needed, or rely on cascade
    db.delete(task)
    db.commit()
    return True

def list_records(db: Session, params: RecordListParams) -> Tuple[List[RecognitionRecord], int]:
    query = db.query(RecognitionRecord)
    
    if params.user_id:
        query = query.filter(RecognitionRecord.user_id == params.user_id)
    if params.license_plate:
        query = query.filter(RecognitionRecord.license_plate.like(f"%{params.license_plate}%"))
    if params.plate_type:
        query = query.filter(RecognitionRecord.plate_type == params.plate_type)
    if params.start_time:
        query = query.filter(RecognitionRecord.created_at >= params.start_time)
    if params.end_time:
        query = query.filter(RecognitionRecord.created_at <= params.end_time)
        
    total = query.count()
    records = query.order_by(desc(RecognitionRecord.created_at)).offset((params.page - 1) * params.page_size).limit(params.page_size).all()
    return records, total

def delete_record(db: Session, record_id: int) -> bool:
    record = db.query(RecognitionRecord).filter(RecognitionRecord.id == record_id).first()
    if not record:
        return False
    db.delete(record)
    db.commit()
    return True

def list_models(db: Session, is_active: Optional[bool] = None) -> List[RecognitionModel]:
    query = db.query(RecognitionModel)
    if is_active is not None:
        query = query.filter(RecognitionModel.is_active == is_active)
    return query.order_by(desc(RecognitionModel.created_at)).all()

def create_model(db: Session, model_in: RecognitionModelCreate) -> RecognitionModel:
    if model_in.is_active:
        # Set others to inactive if this one is active
        db.query(RecognitionModel).update({RecognitionModel.is_active: False})
        
    model = RecognitionModel(**model_in.model_dump())
    db.add(model)
    db.commit()
    db.refresh(model)
    return model

def update_model(db: Session, model_id: int, model_in: RecognitionModelUpdate) -> Optional[RecognitionModel]:
    model = db.query(RecognitionModel).filter(RecognitionModel.id == model_id).first()
    if not model:
        return None
        
    update_data = model_in.model_dump(exclude_unset=True)
    
    if update_data.get('is_active'):
        # Set others to inactive
        db.query(RecognitionModel).filter(RecognitionModel.id != model_id).update({RecognitionModel.is_active: False})
        
    for field, value in update_data.items():
        setattr(model, field, value)
        
    db.commit()
    db.refresh(model)
    return model

def delete_model(db: Session, model_id: int) -> bool:
    model = db.query(RecognitionModel).filter(RecognitionModel.id == model_id).first()
    if not model:
        return False
    db.delete(model)
    db.commit()
    return True
