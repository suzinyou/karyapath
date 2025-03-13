from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, services
from .database import engine, get_db

app = FastAPI()

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

@app.post("/registration-flow", response_model=schemas.RegistrationResponse)
async def registration_flow(
    request: schemas.RegistrationRequest,
    db: Session = Depends(get_db)
):
    """
    Handle the registration flow conversation.
    If message is None, starts a new registration flow.
    If message is provided, continues the existing conversation.
    """
    registration_service = services.RegistrationService(db)
    
    if not request.message:
        # Start new registration
        return registration_service.start_registration(request.user_id, request.session_id)
    
    # Continue existing registration
    return registration_service.process_message(request.session_id, request.message) 