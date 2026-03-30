from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

engine = create_engine('sqlite:///pi_stats.db', echo=False)
Base = declarative_base()

class SystemStat(Base):
    __tablename__ = 'system_stats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_address = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    cpu_usage = Column(Float, nullable=False)
    ram_used_mb = Column(Integer, nullable=False)
    disk_free_gb = Column(Float, nullable=False)
    wifi_ssid = Column(String, nullable=True)
    timestamp = Column(DateTime, server_default=func.now())

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("System stats database built successfully.")