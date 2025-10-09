from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.database import get_db
    from app.models.settings import Setting, SettingCreate, SettingUpdate, SettingResponse
except ImportError:
    # Try importing directly (Docker container)
    from database import get_db
    from models.settings import Setting, SettingCreate, SettingUpdate, SettingResponse

router = APIRouter(prefix="/api/settings", tags=["Settings"])

@router.get("/", response_model=List[SettingResponse])
def get_settings(db: Session = Depends(get_db)):
    """Retrieve all settings"""
    settings = db.query(Setting).all()
    return settings

@router.get("/{key}", response_model=SettingResponse)
def get_setting(key: str, db: Session = Depends(get_db)):
    """Retrieve a specific setting by key"""
    setting = db.query(Setting).filter(Setting.key == key).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting

@router.post("/", response_model=SettingResponse)
def create_setting(setting: SettingCreate, db: Session = Depends(get_db)):
    """Create a new setting"""
    # Check if setting already exists
    existing_setting = db.query(Setting).filter(Setting.key == setting.key).first()
    if existing_setting:
        raise HTTPException(status_code=400, detail="Setting already exists")
    
    # Create setting record
    db_setting = Setting(
        key=setting.key,
        value=setting.value,
        description=setting.description
    )
    
    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    
    return db_setting

@router.put("/{key}", response_model=SettingResponse)
def update_setting(key: str, setting_update: SettingUpdate, db: Session = Depends(get_db)):
    """Update an existing setting"""
    db_setting = db.query(Setting).filter(Setting.key == key).first()
    if not db_setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    
    # Update setting value
    db_setting.value = setting_update.value
    
    db.commit()
    db.refresh(db_setting)
    
    return db_setting

@router.delete("/{key}")
def delete_setting(key: str, db: Session = Depends(get_db)):
    """Delete a setting"""
    db_setting = db.query(Setting).filter(Setting.key == key).first()
    if not db_setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    
    db.delete(db_setting)
    db.commit()
    return {"message": "Setting deleted successfully"}

# Tax rate specific endpoints
@router.get("/tax-rate", response_model=float)
def get_tax_rate(db: Session = Depends(get_db)):
    """Get the current tax rate"""
    setting = db.query(Setting).filter(Setting.key == "tax_rate").first()
    if not setting:
        # Return default tax rate of 8% if not set
        return 0.08
    try:
        return float(setting.value)
    except ValueError:
        # Return default if value is not a valid float
        return 0.08

@router.post("/tax-rate")
def update_tax_rate(tax_rate: float, db: Session = Depends(get_db)):
    """Update the tax rate"""
    # Validate tax rate
    if tax_rate < 0 or tax_rate > 100:
        raise HTTPException(status_code=400, detail="Tax rate must be between 0 and 100")
    
    # Check if setting already exists
    db_setting = db.query(Setting).filter(Setting.key == "tax_rate").first()
    if not db_setting:
        # Create new setting
        db_setting = Setting(
            key="tax_rate",
            value=str(tax_rate),
            description="Tax rate percentage"
        )
        db.add(db_setting)
    else:
        # Update existing setting
        db_setting.value = str(tax_rate)
    
    db.commit()
    if db_setting.id:
        db.refresh(db_setting)
    
    return {"message": f"Tax rate updated to {tax_rate}%", "tax_rate": tax_rate}