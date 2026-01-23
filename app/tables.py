from sqlalchemy import Table,Column,Integer,Text,MetaData,TIMESTAMP,CheckConstraint,UUID,Boolean
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
    CheckConstraint("status IN ('pending','in_progress','completed')"),
    CheckConstraint("length(trim(description))>0",name="tasks_description_not_empty"),
    CheckConstraint("length(trim(title))>0",name="tasks_title_not_empty")
)

users=Table(
    "users",
    metadata,
    Column("id",UUID(as_uuid=True),server_default=func.uuid_generate_v4(),primary_key=True),
    Column("email",Text,nullable=False,unique=True),
    Column("hashed_password",Text,nullable=False),
    Column("is_active",Boolean,nullable=False,server_default="true"),
    Column("created_at", TIMESTAMP(timezone=True),nullable=False, server_default=func.now()),
    Column("updated_at", TIMESTAMP(timezone=True),nullable=False, server_default=func.now())
    
)
