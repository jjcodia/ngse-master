from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY, JSON, JSONB
from sqlalchemy import (
	Column,
	Integer,
	Text,
	Boolean,
	DateTime,
	ForeignKey,
	func
)

Base = declarative_base()

class FormType(Base):
	__tablename__ = 'form_types'
	
	id = Column(Integer, primary_key=True)
	name = Column(Text, nullable=False)
	date_created = Column(DateTime, nullable=False, server_default=func.now())
	last_modified = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

	forms = relationship("Form", back_populates="form_type") # child relationship
	categories = relationship("Category", back_populates="form_type") # child relationship

class Form(Base):
	__tablename__ = 'forms'
	
	id = Column(Integer, primary_key=True)
	name = Column(Text, nullable=False)
	date_created = Column(DateTime, nullable=False, server_default=func.now())
	last_modified = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

	date_start = Column(DateTime, nullable=False)
	date_end = Column(DateTime, nullable=False)
	page_sequence = Column(ARRAY(Integer))

	form_type_id = Column(Integer, ForeignKey('form_types.id')) # parent
	form_type = relationship("FormType", back_populates="forms") # parent relationship

class Category(Base):
	__tablename__ = 'categories'
	
	id = Column(Integer, primary_key=True)
	name = Column(Text, nullable=False)
	date_created = Column(DateTime, nullable=False, server_default=func.now())
	last_modified = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
	
	form_type_id = Column(Integer, ForeignKey('form_types.id')) # parent
	form_type = relationship("FormType", back_populates="categories") # parent relationship

	questions = relationship("Question", back_populates="category")

class Question(Base):
	__tablename__ = 'questions'
	
	id = Column(Integer, primary_key=True)
	name = Column(Text, nullable=False)
	date_created = Column(DateTime, nullable=False, server_default=func.now())
	last_modified = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

	category_id = Column(Integer, ForeignKey('categories.id')) # parent
	category = relationship("Category", back_populates="questions") #parent relationship

	# form_type_id = Column(Integer, ForeignKey('form_types.id')) # parent
	# form_type = relationship("FormType", back_populates="questions") # parent relationship

	meta = Column(JSONB)

	answers = relationship("Answer", back_populates="question")

class Answer(Base):
	__tablename__ = 'answers'
	
	id = Column(Integer, primary_key=True)
	name = Column(Text, nullable=False)
	date_created = Column(DateTime, nullable=False, server_default=func.now())
	last_modified = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

	question_id = Column(Integer, ForeignKey('questions.id')) # parent
	question = relationship("Question", back_populates='answers') # parent relationship

	user_id = Column(Integer, ForeignKey('users.id')) # parent
	user = relationship("User", back_populates='answers') # parent relationship

class UserType(Base):
	__tablename__ = 'user_types'
	
	id = Column(Integer, primary_key=True)
	name = Column(Text, nullable=False)
	date_created = Column(DateTime, nullable=False, server_default=func.now())
	last_modified = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

	user = relationship("User", back_populates='user_type')

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	name = Column(Text, nullable=False)
	date_created = Column(DateTime, nullable=False, server_default=func.now())
	last_modified = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

	email = Column(Text, unique=True, nullable=False)
	password = Column(Text, nullable=False)

	user_type_id = Column(Integer, ForeignKey('user_types.id'))
	user_type = relationship("UserType", back_populates='user')

	# applicant_attr = relationship("ApplicantAttribute", uselist=False, back_populates='users')
	answers = relationship("Answer", back_populates="user")

# class ApplicantAttribute(Base):
# 	__tablename__ = 'applicant_attrs'

# 	id = Column(Integer, primary_key=True)
# 	date_created = Column(DateTime, nullable=False, server_default=func.now())
# 	last_modified = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

# 	erdt_status = Column(Boolean, nullable=False, default=False)
# 	applicant_status = Column(Integer, nullable=False, default=0)
# 	validation_status = Column(Text, nullable=False, default='incomplete')

# 	recommender_A = Column(Integer, ForeignKey('user_types.id'))	
# 	recommender_B = Column(Integer, ForeignKey('user_types.id'))
# 	recommender_C = Column(Integer, ForeignKey('user_types.id'))

# 	applicant_id = Column(Integer, ForeignKey('user_types.id'))
# 	applicant = relationship("User", back_populates='applicant_attrs')