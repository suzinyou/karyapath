from datetime import datetime, date
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from . import models, schemas

class RegistrationService:
    def __init__(self, db: Session):
        self.db = db

    def _create_message(self, session_id: str, message: str, is_user_message: bool = False) -> models.ConversationMessage:
        db_message = models.ConversationMessage(
            session_id=session_id,
            message=message,
            is_user_message=is_user_message
        )
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message

    def start_registration(self, user_id: str, session_id: str) -> schemas.RegistrationResponse:
        # Create a new registration session
        session = models.RegistrationSession(
            user_id=user_id,
            session_id=session_id
        )
        self.db.add(session)
        self.db.commit()

        # Create welcome message
        welcome_message = (
            "Welcome to KaryaPath! I'll help you register for our platform. "
            "This registration will help us guide you better through your apprenticeship and career journey. "
            "Let's start with your basic information.\n\n"
            "First, could you please tell me your full name?"
        )
        self._create_message(session_id, welcome_message)
        
        return schemas.RegistrationResponse(
            message=welcome_message,
            session_id=session_id
        )

    def _get_next_field(self, registration: Optional[models.StudentRegistration]) -> Optional[str]:
        """Determine the next field to collect based on current registration state."""
        if not registration:
            return "name"
        
        fields = [
            ("name", "Could you please tell me your full name?"),
            ("naps_registration_code", "Please provide your NAPS registration code (10-11 digits):"),
            ("date_of_birth", "What is your date of birth? (YYYY-MM-DD format)"),
            ("gender", "What is your gender? (Male/Female/Transgender)"),
            ("disability_divyang", "Do you have any disabilities? (Yes/No)"),
            ("parent_name", "What is your parent's or guardian's name?"),
            ("parent_relation", "What is your relation with them? (Father/Mother/Spouse)"),
            ("religion", "What is your religion? (Hindu/Muslim/Christian/Sikh/Buddhist/Jain/Others)"),
            ("category", "What is your category? (General/OBC/SC/ST)"),
            ("qualification_type", "What is your qualification type? (Educational Qualification/Trained Under Schemes)"),
            ("trade_name", None)  # Special handling based on qualification_type
        ]

        for field, prompt in fields:
            if not hasattr(registration, field) or getattr(registration, field) is None:
                if field == "trade_name" and registration.qualification_type:
                    if registration.qualification_type == models.QualificationType.EDUCATIONAL:
                        return "Please select your educational qualification:\n" + "\n".join([
                            f"- {trade.value}" for trade in models.EducationTrade
                        ])
                    else:
                        return "Please select the scheme you were trained under:\n" + "\n".join([
                            f"- {trade.value}" for trade in models.SchemeTrade
                        ])
                return prompt
        return None

    def process_message(self, session_id: str, message: str) -> schemas.RegistrationResponse:
        # Record user message
        self._create_message(session_id, message, is_user_message=True)

        # Get or create registration
        registration = self.db.query(models.StudentRegistration).filter_by(session_id=session_id).first()
        if not registration:
            registration = models.StudentRegistration(
                session_id=session_id,
                registration_date=date.today()
            )
            self.db.add(registration)

        # Process the message based on the current state
        next_field = self._get_next_field(registration)
        if not next_field:
            # Registration is complete
            session = self.db.query(models.RegistrationSession).filter_by(session_id=session_id).first()
            session.completed = True
            self.db.commit()
            
            response = "Thank you! Your registration is complete. We'll use this information to provide you with better guidance for your career journey."
            self._create_message(session_id, response)
            return schemas.RegistrationResponse(
                message=response,
                completed=True,
                session_id=session_id
            )

        # Update the registration based on the current field
        try:
            if next_field == "name":
                registration.name = message.strip()
            elif next_field == "naps_registration_code":
                if not (10 <= len(message.strip()) <= 11):
                    raise ValueError("NAPS registration code must be 10-11 digits")
                registration.naps_registration_code = message.strip()
            elif next_field == "date_of_birth":
                registration.date_of_birth = datetime.strptime(message.strip(), "%Y-%m-%d").date()
            elif next_field == "gender":
                registration.gender = models.Gender(message.strip())
            elif next_field == "disability_divyang":
                registration.disability_divyang = models.YesNo(message.strip())
            elif next_field == "parent_name":
                registration.parent_name = message.strip()
            elif next_field == "parent_relation":
                registration.parent_relation = models.ParentRelation(message.strip())
            elif next_field == "religion":
                registration.religion = models.Religion(message.strip())
            elif next_field == "category":
                registration.category = models.Category(message.strip())
            elif next_field == "qualification_type":
                registration.qualification_type = models.QualificationType(message.strip())
            elif "trade_name" in next_field.lower():
                if registration.qualification_type == models.QualificationType.EDUCATIONAL:
                    registration.education_trade = models.EducationTrade(message.strip())
                else:
                    registration.scheme_trade = models.SchemeTrade(message.strip())
            
            self.db.commit()
            
            # Get the next prompt
            next_prompt = self._get_next_field(registration)
            if not next_prompt:
                # Registration is complete
                session = self.db.query(models.RegistrationSession).filter_by(session_id=session_id).first()
                session.completed = True
                self.db.commit()
                
                response = "Thank you! Your registration is complete. We'll use this information to provide you with better guidance for your career journey."
                self._create_message(session_id, response)
                return schemas.RegistrationResponse(
                    message=response,
                    completed=True,
                    session_id=session_id
                )
            
            self._create_message(session_id, next_prompt)
            return schemas.RegistrationResponse(
                message=next_prompt,
                session_id=session_id
            )
            
        except (ValueError, KeyError) as e:
            error_message = f"I'm sorry, but that doesn't seem to be a valid input. {str(e)}"
            self._create_message(session_id, error_message)
            return schemas.RegistrationResponse(
                message=error_message + "\n\n" + next_field,
                session_id=session_id
            ) 