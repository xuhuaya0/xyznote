from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# 依赖项：获取数据库 session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- 资产分类 ----------
@app.post("/categories/", response_model=schemas.AssetCategoryOut)
def create_category(category: schemas.AssetCategoryCreate, db: Session = Depends(get_db)):
    return crud.create_asset_category(db, category)

@app.get("/categories/{uid}", response_model=schemas.AssetCategoryOut)
def get_category(uid: str, db: Session = Depends(get_db)):
    category = crud.get_asset_category_by_uid(db, uid)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# ---------- 创建账本 ----------
@app.post("/ledgers/", response_model=schemas.LedgerOut)
def create_ledger(ledger: schemas.LedgerCreate, db: Session = Depends(get_db)):
    return crud.create_ledger(db, ledger)

@app.get("/ledgers/{uid}", response_model=schemas.LedgerOut)
def get_ledger(uid: str, db: Session = Depends(get_db)):
    ledger = crud.get_ledger_by_uid(db, uid)
    if not ledger:
        raise HTTPException(status_code=404, detail="Ledger not found")
    return ledger

# ---------- 添加交易 ----------
@app.post("/transactions/", response_model=schemas.TransactionOut)
def create_transaction(tx: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db, tx)

@app.get("/transactions/{uid}", response_model=schemas.TransactionOut)
def get_transaction(uid: str, db: Session = Depends(get_db)):
    tx = crud.get_transaction_by_uid(db, uid)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx

@app.get("/ledgers/{uid}/transactions", response_model=list[schemas.TransactionOut])
def list_ledger_transactions(uid: str, db: Session = Depends(get_db)):
    return crud.list_transactions_by_ledger(db, uid)
