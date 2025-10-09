from sqlalchemy.orm import Session
from typing import Optional

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.models.settings import Setting
except ImportError:
    # Try importing directly (Docker container)
    from models.settings import Setting

class SettingsService:
    """Service class to handle application settings"""
    
    @staticmethod
    def get_setting(db: Session, key: str) -> Optional[Setting]:
        """Get a setting by key"""
        return db.query(Setting).filter(Setting.key == key).first()
    
    @staticmethod
    def get_tax_rate(db: Session) -> float:
        """Get the current tax rate from settings or return default"""
        setting = SettingsService.get_setting(db, "tax_rate")
        if not setting:
            return 0.08  # Default to 8%
        try:
            return float(setting.value)
        except ValueError:
            return 0.08  # Default to 8% if invalid value
    
    @staticmethod
    def update_tax_rate(db: Session, tax_rate: float) -> dict:
        """Update the tax rate setting"""
        # Validate tax rate
        if tax_rate < 0 or tax_rate > 100:
            raise ValueError("Tax rate must be between 0 and 100")
        
        # Check if setting already exists
        db_setting = SettingsService.get_setting(db, "tax_rate")
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