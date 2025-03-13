from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, DateTime, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import enum
from datetime import date

Base = declarative_base()

class Gender(str, enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    TRANSGENDER = "Transgender"

class YesNo(str, enum.Enum):
    YES = "Yes"
    NO = "No"

class Religion(str, enum.Enum):
    HINDU = "Hindu"
    MUSLIM = "Muslim"
    CHRISTIAN = "Christian"
    SIKH = "Sikh"
    BUDDHIST = "Buddhist"
    JAIN = "Jain"
    OTHERS = "Others"

class Category(str, enum.Enum):
    GENERAL = "General"
    OBC = "OBC"
    SC = "SC"
    ST = "ST"

class QualificationType(str, enum.Enum):
    EDUCATIONAL = "Educational Qualification"
    SCHEME = "Trained Under Schemes"

class EducationTrade(str, enum.Enum):
    FIFTH = "5th"
    SIXTH = "6th"
    SEVENTH = "7th"
    EIGHTH = "8th"
    NINTH = "9th"
    TENTH = "10th"
    ELEVENTH = "11th"
    TWELFTH = "12th"
    ITI = "ITI"
    MSBSVET = "MSBSVET"
    ITI_DUAL = "ITI Dual"
    ITI_RESULT_AWAITED = "ITI Result Awaited"
    DIPLOMA_PURSUING = "Diploma Pursuing"
    GRADUATE_PURSUING = "Graduate Pursuing"
    ADVANCED_DIPLOMA = "Advanced Diploma"
    GRADUATE = "Graduate"
    POST_GRADUATE = "Post Graduate"
    DOCTORAL = "Doctoral"
    OTHERS = "Others"

class SchemeTrade(str, enum.Enum):
    NULM = "NULM"
    DDUGKY = "DDUGKY"
    STATE_SPECIFIC = "State Specific Schemes"
    PMKVY = "PMKVY"
    SDI_MES = "SDI-MES"
    CENTRAL = "Central Schemes"
    VSE_MHRD = "Vocationalization of School Education (VSE)-MHRD"
    PMKVY_MSDE = "PMKVY-MSDE"
    DDUGKY_MORD = "DDUGKY-MoRD"
    ESTP_NULM = "EST&P-NULM"
    PMAYG_MOSJE = "PMAYG-MoSJE"
    CPWD_MOUD = "CPWD-MoUD"
    NSKFDC_MOSJE = "NSKFDC-MoSJE"
    NBCFDC_MOSJE = "NBCFDC-MoSJE"
    NSDFDC_MOSJE = "NSDFDC-MoSJE"
    ISDS_TEXTILES = "ISDS-MoTextiles"
    SEEKHO_MAMA = "Seekho aur Kamao-MoMA"
    SSC_FEE = "SSC-fee based cources"

class ParentRelation(str, enum.Enum):
    FATHER = "Father"
    MOTHER = "Mother"
    SPOUSE = "Spouse"

class RegistrationSession(Base):
    __tablename__ = "registration_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    session_id = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed = Column(String, default=False)
    
    messages = relationship("ConversationMessage", back_populates="session")
    registration = relationship("StudentRegistration", back_populates="session", uselist=False)

class ConversationMessage(Base):
    __tablename__ = "conversation_messages"

    id = Column(Integer, primary_key=True)
    session_id = Column(String, ForeignKey("registration_sessions.session_id"))
    message = Column(Text, nullable=False)
    is_user_message = Column(String, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    session = relationship("RegistrationSession", back_populates="messages")

class StudentRegistration(Base):
    __tablename__ = "student_registrations"

    id = Column(Integer, primary_key=True)
    session_id = Column(String, ForeignKey("registration_sessions.session_id"), unique=True)
    naps_registration_code = Column(String(11), unique=True)
    registration_date = Column(Date, nullable=False)
    name = Column(String, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    disability_divyang = Column(Enum(YesNo), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    parent_name = Column(String, nullable=False)
    parent_relation = Column(Enum(ParentRelation), nullable=False)
    religion = Column(Enum(Religion), nullable=False)
    category = Column(Enum(Category), nullable=False)
    qualification_type = Column(Enum(QualificationType), nullable=False)
    education_trade = Column(Enum(EducationTrade))
    scheme_trade = Column(Enum(SchemeTrade))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    session = relationship("RegistrationSession", back_populates="registration") 