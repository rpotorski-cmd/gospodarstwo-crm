from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, Date
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, default="pracownik")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Worker can be assigned to specific clients
    assigned_clients = relationship("ClientAssignment", back_populates="user")
    activity_logs = relationship("ActivityLog", back_populates="user")


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    cycles = Column(Integer, default=0)
    pigs = Column(Integer, default=0)
    sold = Column(Integer, default=0)
    profit = Column(Float, default=0)
    mortality = Column(Float, default=0)
    fcr = Column(Float, default=0)
    deaths = Column(Integer, default=0)
    kolczyk = Column(Text, default="")
    profit_per_pig = Column(Float, default=0)
    feeds = Column(String(255), default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    assignments = relationship("ClientAssignment", back_populates="client")
    cycle_records = relationship("CycleRecord", back_populates="client")


class ClientAssignment(Base):
    __tablename__ = "client_assignments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="assigned_clients")
    client = relationship("Client", back_populates="assignments")


class CycleRecord(Base):
    __tablename__ = "cycle_records"

    id = Column(Integer, primary_key=True, index=True)
    cycle_number = Column(Integer, index=True)
    month = Column(String(20))
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    client_name = Column(String(100))
    feed = Column(String(100))
    start_qty = Column(Integer, default=0)
    sold_qty = Column(Integer, default=0)
    profit = Column(Float, nullable=True)
    mortality = Column(Float, default=0)
    cycle_type = Column(String(50), default="Kabanek")
    status = Column(String(20), default="active")  # active, settled, preliminary
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    client = relationship("Client", back_populates="cycle_records")


class FeedMonthly(Base):
    __tablename__ = "feed_monthly"

    id = Column(Integer, primary_key=True, index=True)
    feed = Column(String(100), nullable=False, index=True)
    ym = Column(String(7), nullable=False)  # YYYY-MM
    date = Column(String(10), nullable=False)
    cycles = Column(Integer, default=0)
    pigs = Column(Integer, default=0)
    profit = Column(Float, default=0)
    mortality = Column(Float, default=0)
    fcr = Column(Float, default=0)


class FinanceRecord(Base):
    __tablename__ = "finance_records"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(100), nullable=False, index=True)
    date = Column(String(10), nullable=False, index=True)
    pigs = Column(Integer, default=0)
    sold = Column(Integer, default=0)
    profit = Column(Float, nullable=True)
    mortality = Column(Float, default=0)
    fcr = Column(Float, default=0)
    deaths = Column(Integer, default=0)
    feed = Column(String(100), default="")
    status = Column(Integer, default=0)  # 0=in_progress, 1=preliminary, 2=settled


class YearlyStats(Base):
    __tablename__ = "yearly_stats"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(String(4), unique=True, nullable=False)
    cycles = Column(Integer, default=0)
    pigs = Column(Integer, default=0)
    profit = Column(Float, default=0)
    mortality = Column(Float, default=0)
    fcr = Column(Float, default=0)


class FeedSupplier(Base):
    __tablename__ = "feed_suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    color = Column(String(7), default="#607D8B")
    total_pigs = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(50), nullable=False)
    resource = Column(String(50), nullable=False)
    resource_id = Column(Integer, nullable=True)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="activity_logs")
