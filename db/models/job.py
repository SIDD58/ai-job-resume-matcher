from db.base import Base
from sqlalchemy import Column,  Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
class Job(Base):
    __tablename__ = 'jobs'
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    job_description = Column(Text, nullable=False)
    created_by = Column(Text, nullable=False)