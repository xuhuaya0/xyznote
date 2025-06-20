from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 资产分类（用于账本创建时选择）
class AssetCategoryCreate(BaseModel):
    region: str
    category_type: str
    redeem_location: str

class AssetCategoryOut(AssetCategoryCreate):
    uid: str
    class Config:
        orm_mode = True

# 账本（创建 & 返回）
class LedgerCreate(BaseModel):
    name: str
    asset_category_uid: str
    base_currency: str

class LedgerOut(LedgerCreate):
    uid: str
    created_at: datetime
    last_changed_at: Optional[datetime]
    balance: float
    float_profit: float
    tax_pending: float
    after_tax_balance: float
    irr: float
    irr_weighted: float
    irr_after_tax: float
    irr_after_tax_weighted: float

    class Config:
        orm_mode = True

# 流水
class TransactionCreate(BaseModel):
    ledger_uid: str
    amount: float
    transaction_type: str
    currency: str
    rate_to_base: float
    converted_amount: float
    event_time: datetime
    purpose: Optional[str]
    raw_text: Optional[str]
    to_ledger_uid: Optional[str]  # 如果是转账才填

class TransactionOut(TransactionCreate):
    uid: str
    recorded_time: datetime

    class Config:
        orm_mode = True

# 快照
class LedgerSnapshotOut(BaseModel):
    uid: str
    ledger_uid: str
    snapshot_date: datetime
    balance: float
    float_profit: float
    after_tax_balance: float
    irr: float
    irr_weighted: float
    irr_after_tax: float
    irr_after_tax_weighted: float

    class Config:
        orm_mode = True
