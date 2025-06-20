from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# 资产分类表
class AssetCategory(Base):
    __tablename__ = "asset_categories"

    uid = Column(Integer, primary_key=True)
    region = Column(String)  # 地域属性：中国、香港等
    category_type = Column(String)  # 类别属性：股票、基金等
    redeem_location = Column(String)  # 赎回资金落地：如中国

# 账本表
class Ledger(Base):
    __tablename__ = "ledgers"

    id = Column(Integer, primary_key=True)
    uid = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_changed_at = Column(DateTime)
    last_transaction_id = Column(Integer)

    asset_category_id = Column(Integer, ForeignKey("asset_categories.id"))
    asset_category = relationship("AssetCategory", backref="ledgers")

    base_currency = Column(String, nullable=False)  # 人民币、美元等
    balance = Column(Float, default=0.0)
    float_profit = Column(Float, default=0.0)
    tax_pending = Column(Float, default=0.0)
    after_tax_balance = Column(Float, default=0.0)

    irr = Column(Float, default=0.0)
    irr_weighted = Column(Float, default=0.0)
    irr_after_tax = Column(Float, default=0.0)
    irr_after_tax_weighted = Column(Float, default=0.0)

# 流水表
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    ledger_id = Column(Integer, ForeignKey("ledgers.id"), nullable=False)
    ledger = relationship("Ledger", backref="transactions")

    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)  # 收入/支出/收益/转账等
    to_ledger_id = Column(Integer, ForeignKey("ledgers.id"))  # 如果是转账
    currency = Column(String, nullable=False)
    rate_to_base = Column(Float, nullable=False)
    converted_amount = Column(Float, nullable=False)

    event_time = Column(DateTime, nullable=False)
    sent_time = Column(DateTime)
    recorded_time = Column(DateTime, default=datetime.utcnow)

    purpose = Column(String)
    raw_text = Column(String)

# 快照表（每日）
class LedgerSnapshot(Base):
    __tablename__ = "ledger_snapshots"

    id = Column(Integer, primary_key=True)
    ledger_id = Column(Integer, ForeignKey("ledgers.id"), nullable=False)
    ledger = relationship("Ledger", backref="snapshots")

    snapshot_date = Column(DateTime, nullable=False)  # 一天一条
    balance = Column(Float)
    float_profit = Column(Float)
    after_tax_balance = Column(Float)

    irr = Column(Float)
    irr_weighted = Column(Float)
    irr_after_tax = Column(Float)
    irr_after_tax_weighted = Column(Float)

    calculated_from_tx_id = Column(Integer)  # 快照由哪条交易触发生成（审计用）
