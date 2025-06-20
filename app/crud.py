from sqlalchemy.orm import Session
from . import models, schemas
import uuid
from datetime import datetime

# ---------- 资产分类 ----------
def create_asset_category(db: Session, category: schemas.AssetCategoryCreate):
    db_category = models.AssetCategory(
        uid=str(uuid.uuid4()),
        region=category.region,
        category_type=category.category_type,
        redeem_location=category.redeem_location,
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_asset_category_by_uid(db: Session, uid: str):
    return db.query(models.AssetCategory).filter(models.AssetCategory.uid == uid).first()

# ---------- 创建账本 ----------
def create_ledger(db: Session, ledger: schemas.LedgerCreate):
    db_ledger = models.Ledger(
        uid=str(uuid.uuid4()),
        name=ledger.name,
        created_at=datetime.utcnow(),
        asset_category_uid=ledger.asset_category_uid,
        base_currency=ledger.base_currency,
        balance=0.0,
        float_profit=0.0,
        tax_pending=0.0,
        after_tax_balance=0.0,
        irr=0.0,
        irr_weighted=0.0,
        irr_after_tax=0.0,
        irr_after_tax_weighted=0.0,
    )
    db.add(db_ledger)
    db.commit()
    db.refresh(db_ledger)
    return db_ledger

def get_ledger_by_uid(db: Session, uid: str):
    return db.query(models.Ledger).filter(models.Ledger.uid == uid).first()

# ---------- 创建交易 + 自动更新账本 ----------
def create_transaction(db: Session, tx: schemas.TransactionCreate):
    ledger = get_ledger_by_uid(db, tx.ledger_uid)
    if not ledger:
        raise Exception("Ledger not found")

    db_tx = models.Transaction(
        uid=str(uuid.uuid4()),
        ledger_id=ledger.id,
        amount=tx.amount,
        transaction_type=tx.transaction_type,
        currency=tx.currency,
        rate_to_base=tx.rate_to_base,
        converted_amount=tx.converted_amount,
        event_time=tx.event_time,
        sent_time=datetime.utcnow(),
        recorded_time=datetime.utcnow(),
        purpose=tx.purpose,
        raw_text=tx.raw_text,
    )

    db.add(db_tx)

    # 自动更新账本余额（注意这里只是简单相加）
    ledger.balance += tx.converted_amount
    ledger.last_changed_at = datetime.utcnow()
    ledger.last_transaction_id = db_tx.id

    db.commit()
    db.refresh(db_tx)
    return db_tx

# ---------- 查询 ----------
def get_transaction_by_uid(db: Session, uid: str):
    return db.query(models.Transaction).filter(models.Transaction.uid == uid).first()

def list_transactions_by_ledger(db: Session, ledger_uid: str):
    ledger = get_ledger_by_uid(db, ledger_uid)
    if not ledger:
        return []
    return db.query(models.Transaction).filter(models.Transaction.ledger_id == ledger.id).all()
