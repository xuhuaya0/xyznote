
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ---------- 用户 ----------
class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

# ---------- 资产分类 ----------
class AssetCategoryCreate(BaseModel):
    region: str
    category_type: str
    redeem_location: str

class AssetCategoryOut(AssetCategoryCreate):
    uid: str

    class Config:
        orm_mode = True

# ---------- 账本 ----------
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

# ---------- 交易 ----------
class TransactionCreate(BaseModel):
    ledger_uid: str
    amount: float
    transaction_type: str  # income, expense, transfer
    currency: str
    rate_to_base: float
    converted_amount: float
    event_time: datetime
    purpose: Optional[str]
    raw_text: Optional[str]

class TransactionUpdate(BaseModel):
    amount: Optional[float]
    transaction_type: Optional[str]
    currency: Optional[str]
    rate_to_base: Optional[float]
    converted_amount: Optional[float]
    event_time: Optional[datetime]
    purpose: Optional[str]
    raw_text: Optional[str]

class TransactionOut(TransactionCreate):
    uid: str
    recorded_time: datetime

    class Config:
        orm_mode = True

# ---------- 快照 ----------
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
