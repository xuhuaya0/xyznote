
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models, schemas, crud
from datetime import timedelta

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 依赖项：获取数据库 session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 示例用户认证（后续需接入 JWT 验证）
@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.register_user(db, user)

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return crud.login_user(db, form_data)

@app.get("/me")
def read_me(current_user: schemas.User = Depends(crud.get_current_user)):
    return current_user

# ---------- 资产分类 ----------
@app.post("/categories/", response_model=schemas.AssetCategoryOut)
def create_category(cat: schemas.AssetCategoryCreate, db: Session = Depends(get_db),
                    user: schemas.User = Depends(crud.get_current_user)):
    return crud.create_asset_category(db, cat, user.id)

@app.get("/categories/", response_model=list[schemas.AssetCategoryOut])
def get_categories(db: Session = Depends(get_db),
                   user: schemas.User = Depends(crud.get_current_user)):
    return crud.get_user_categories(db, user.id)

@app.get("/categories/{uid}", response_model=schemas.AssetCategoryOut)
def get_category(uid: str, db: Session = Depends(get_db),
                 user: schemas.User = Depends(crud.get_current_user)):
    return crud.get_category_by_uid(db, uid, user.id)

@app.delete("/categories/{uid}")
def delete_category(uid: str, db: Session = Depends(get_db),
                    user: schemas.User = Depends(crud.get_current_user)):
    return crud.delete_category(db, uid, user.id)

# ---------- 账本 ----------
@app.post("/ledgers/", response_model=schemas.LedgerOut)
def create_ledger(ledger: schemas.LedgerCreate, db: Session = Depends(get_db),
                  user: schemas.User = Depends(crud.get_current_user)):
    return crud.create_ledger(db, ledger, user.id)

@app.get("/ledgers/", response_model=list[schemas.LedgerOut])
def get_ledgers(db: Session = Depends(get_db),
                user: schemas.User = Depends(crud.get_current_user)):
    return crud.get_user_ledgers(db, user.id)

@app.get("/ledgers/{uid}", response_model=schemas.LedgerOut)
def get_ledger(uid: str, db: Session = Depends(get_db),
               user: schemas.User = Depends(crud.get_current_user)):
    return crud.get_ledger_by_uid(db, uid, user.id)

@app.delete("/ledgers/{uid}")
def delete_ledger(uid: str, db: Session = Depends(get_db),
                  user: schemas.User = Depends(crud.get_current_user)):
    return crud.delete_ledger(db, uid, user.id)

@app.get("/ledgers/{uid}/summary")
def ledger_summary(uid: str, db: Session = Depends(get_db),
                   user: schemas.User = Depends(crud.get_current_user)):
    return crud.get_ledger_summary(db, uid, user.id)

@app.get("/ledgers/{uid}/chart")
def ledger_chart(uid: str, start: str = None, end: str = None,
                 db: Session = Depends(get_db),
                 user: schemas.User = Depends(crud.get_current_user)):
    return crud.get_ledger_chart(db, uid, user.id, start, end)

# ---------- 流水 ----------
@app.post("/transactions/", response_model=schemas.TransactionOut)
def create_transaction(tx: schemas.TransactionCreate, db: Session = Depends(get_db),
                       user: schemas.User = Depends(crud.get_current_user)):
    return crud.create_transaction(db, tx, user.id)

@app.get("/transactions/{uid}", response_model=schemas.TransactionOut)
def get_transaction(uid: str, db: Session = Depends(get_db),
                    user: schemas.User = Depends(crud.get_current_user)):
    return crud.get_transaction_by_uid(db, uid, user.id)

@app.put("/transactions/{uid}")
def update_transaction(uid: str, tx: schemas.TransactionUpdate, db: Session = Depends(get_db),
                       user: schemas.User = Depends(crud.get_current_user)):
    return crud.update_transaction(db, uid, tx, user.id)

@app.delete("/transactions/{uid}")
def delete_transaction(uid: str, db: Session = Depends(get_db),
                       user: schemas.User = Depends(crud.get_current_user)):
    return crud.delete_transaction(db, uid, user.id)

@app.get("/ledgers/{uid}/transactions", response_model=list[schemas.TransactionOut])
def list_transactions(uid: str, db: Session = Depends(get_db),
                      user: schemas.User = Depends(crud.get_current_user)):
    return crud.list_transactions_by_ledger(db, uid, user.id)

# ---------- 快照 ----------
@app.get("/ledgers/{uid}/snapshots")
def get_snapshots(uid: str, db: Session = Depends(get_db),
                  user: schemas.User = Depends(crud.get_current_user)):
    return crud.get_snapshots(db, uid, user.id)

@app.get("/ledgers/{uid}/snapshots/latest")
def get_latest_snapshot(uid: str, db: Session = Depends(get_db),
                        user: schemas.User = Depends(crud.get_current_user)):
    return crud.get_latest_snapshot(db, uid, user.id)

@app.get("/ledgers/{uid}/snapshots/chart")
def get_snapshot_chart(uid: str, start: str = None, end: str = None,
                       db: Session = Depends(get_db),
                       user: schemas.User = Depends(crud.get_current_user)):
    return crud.get_snapshot_chart(db, uid, user.id, start, end)

@app.post("/ledgers/{uid}/snapshots/generate")
def generate_snapshot(uid: str, db: Session = Depends(get_db),
                      user: schemas.User = Depends(crud.get_current_user)):
    return crud.generate_snapshot(db, uid, user.id)
