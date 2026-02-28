from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(255), default="")
    password_hash = Column(String(255))
    role = Column(String(20), default="user")  # admin, user, viewer
    is_active = Column(Boolean, default=True)


class Material(Base):
    """Raw materials (surowce) with prices and nutritional values"""
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True, index=True)
    sort_order = Column(Integer, default=0)
    name = Column(String(255), default="")
    price = Column(Float, default=0)       # c - cena zł/t
    protein = Column(Float, default=0)     # b - białko %
    ne = Column(Float, default=0)          # NE - energia netto MJ
    lys = Column(Float, default=0)         # Ly - SID lizyna
    met = Column(Float, default=0)         # Me - SID metionina+cystyna
    thr = Column(Float, default=0)         # Th - SID treonina
    trp = Column(Float, default=0)         # Tr - SID tryptofan
    fiber = Column(Float, default=0)       # W - włókno
    calcium = Column(Float, default=0)     # Ca - wapń
    phosphorus = Column(Float, default=0)  # P - fosfor


class Recipe(Base):
    """Recipe shares per phase (JSON array of percentages matching material order)"""
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    phase = Column(String(20), unique=True, index=True)  # Starter, Grower, Finiszer
    shares = Column(Text, default="[]")  # JSON array of floats


class Norm(Base):
    """Nutritional norms per phase"""
    __tablename__ = "norms"
    id = Column(Integer, primary_key=True, index=True)
    phase = Column(String(20), unique=True, index=True)
    protein = Column(Float, default=0)
    ne = Column(Float, default=0)
    lys = Column(Float, default=0)
    met = Column(Float, default=0)
    thr = Column(Float, default=0)
    trp = Column(Float, default=0)
    fiber = Column(Float, default=0)
    calcium = Column(Float, default=0)
    phosphorus = Column(Float, default=0)


class Production(Base):
    """Annual production volumes per phase (tons)"""
    __tablename__ = "production"
    id = Column(Integer, primary_key=True, index=True)
    phase = Column(String(20), unique=True, index=True)
    volume = Column(Float, default=0)  # tons per year


class AuditLog(Base):
    __tablename__ = "audit_log"
    id = Column(Integer, primary_key=True, index=True)
    ts = Column(DateTime, default=datetime.utcnow)
    user_name = Column(String(255), default="")
    email = Column(String(255), default="")
    area = Column(String(100), default="")
    action = Column(Text, default="")
