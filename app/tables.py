from sqlalchemy import Table,Column,Integer,Text,MetaData,TIMESTAMP,CheckConstraint
from sqlalchemy.sql import func

metadata=MetaData()

tasks=Table(
    "tasks",
    metadata,
    Column("id",Integer,primary_key=True),
    Column("title",Text,nullable=False),
    Column("description",Text,nullable=False),
    Column("status", Text, nullable=False,server_default="pending"),
    Column("created_at", TIMESTAMP, server_default=func.now()),
    Column("updated_at", TIMESTAMP, server_default=func.now(), onupdate=func.now()),
    CheckConstraint("status IN ('pending','in_progress','completed')")
    
)
