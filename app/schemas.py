from pydantic import BaseModel, constr
from datetime import date, datetime
from typing import Optional, Literal
from .models import Gender, YesNo, Religion, Category, QualificationType, EducationTrade, SchemeTrade, ParentRelation

class RegistrationRequest(BaseModel):
    user_id: str
    session_id: str
    message: Optional[str] = None

class RegistrationResponse(BaseModel):
    message: str
    completed: bool = False
    session_id: str

class StudentRegistrationBase(BaseModel):
    naps_registration_code: constr(min_length=10, max_length=11)
    registration_date: date
    name: str
    gender: Gender
    disability_divyang: YesNo
    date_of_birth: date
    parent_name: str
    parent_relation: ParentRelation
    religion: Religion
    category: Category
    qualification_type: QualificationType
    education_trade: Optional[EducationTrade] = None
    scheme_trade: Optional[SchemeTrade] = None

    class Config:
        from_attributes = True

class StudentRegistrationCreate(StudentRegistrationBase):
    session_id: str

class StudentRegistrationResponse(StudentRegistrationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class ConversationMessageBase(BaseModel):
    message: str
    is_user_message: bool

class ConversationMessageCreate(ConversationMessageBase):
    session_id: str

class ConversationMessageResponse(ConversationMessageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 