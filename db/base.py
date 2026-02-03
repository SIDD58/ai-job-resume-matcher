from sqlalchemy.ext.declarative import declarative_base
Base=declarative_base()

# This is necessary 
# All ORM models must share the same Base

# Models which have same Base will be aware of each other.
# With same base class you cannot have joins and foreign keys and tables can be in same database schema. 