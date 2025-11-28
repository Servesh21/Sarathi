from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Dict, Any, Optional
import shutil
import os
import uuid
import re  # <--- Needed for cleaning text

# Import your existing modules
from app.database import get_db
from app.models.user import User
from app.auth import get_current_active_user
from app.agents import create_sarathi_agent
from app.services.voice import transcribe_audio, text_to_speech

router = APIRouter(prefix="/agent", tags=["AI Agent"])

# --- HELPER: Clean Text Function ---
def clean_text_for_display(text: str) -> str:
    """
    Removes Markdown formatting (*, **, #) so the Voice doesn't read 'Asterisk'
    and the Chat UI looks cleaner.
    """
    if not text:
        return ""
    # Remove bold/italic markers (**word** -> word)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    # Remove headers (### Title -> Title)
    text = re.sub(r'#+\s', '', text)
    return text.strip()

# --- MODELS ---
class AgentQuery(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None

class AgentResponse(BaseModel):
    response: str
    recommendations: list
    action_items: list
    query_type: str
    analysis: Optional[Dict[str, Any]] = None
    audio_url: Optional[str] = None
    transcription: Optional[str] = None


# --- 1. STANDARD TEXT CHAT ---
@router.post("/chat", response_model=AgentResponse)
async def chat_with_agent(
    query_data: AgentQuery,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Chat with Sarathi AI agent (Text Only)"""
    
    # Create agent
    agent = await create_sarathi_agent(db)
    
    # Build user profile
    user_profile = {
        'user_id': current_user.id,
        'name': current_user.name,
        'city': current_user.city,
        'vehicle_type': current_user.vehicle_type,
        'monthly_income_target': current_user.monthly_income_target,
        'monthly_expense_average': current_user.monthly_expense_average,
        'preferred_language': current_user.preferred_language
    }
    
    try:
        result = await agent.process_query(
            user_id=current_user.id,
            query=query_data.query,
            user_profile=user_profile
        )
        
        # Clean the text before sending back
        clean_response = clean_text_for_display(result['response'])

        return AgentResponse(
            response=clean_response,
            recommendations=result['recommendations'],
            action_items=result['action_items'],
            query_type=result['query_type'],
            analysis={
                'earnings': result.get('earnings_analysis'),
                'vehicle': result.get('vehicle_analysis'),
                'financial': result.get('financial_analysis')
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Agent processing failed: {str(e)}"
        )


# --- 2. VOICE CHAT ---
@router.post("/voice-chat")
async def chat_with_voice(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    1. Receive Audio File
    2. Transcribe to Text
    3. Run Agent
    4. Convert Response to Audio
    """
    
    # 1. Save the uploaded file temporarily
    temp_filename = f"temp_{uuid.uuid4()}_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 2. Transcribe (Voice -> Text)
        user_query_text = await transcribe_audio(temp_filename)
        
        if not user_query_text:
            return {
                "response": "I couldn't hear you clearly. Please try again.",
                "recommendations": [],
                "action_items": [],
                "query_type": "error",
                "audio_url": None
            }

        # 3. Setup Agent & Profile
        agent = await create_sarathi_agent(db)
        
        user_profile = {
            'user_id': current_user.id,
            'name': current_user.name,
            'city': current_user.city,
            'vehicle_type': current_user.vehicle_type,
            'monthly_income_target': current_user.monthly_income_target,
            'monthly_expense_average': current_user.monthly_expense_average,
            'preferred_language': current_user.preferred_language
        }

        # 4. Run the Brain (Text -> Answer)
        result = await agent.process_query(
            user_id=current_user.id,
            query=user_query_text,
            user_profile=user_profile
        )

        # 5. Clean Text & Speak
        # IMPORTANT: We clean the text FIRST, so the TTS doesn't read "**" characters
        clean_response = clean_text_for_display(result['response'])
        
        # Generate Audio from the clean text
        audio_url = await text_to_speech(clean_response)

        return {
            "response": clean_response, # Send clean text to phone
            "recommendations": result['recommendations'],
            "action_items": result['action_items'],
            "query_type": result['query_type'],
            "analysis": {
                'earnings': result.get('earnings_analysis'),
                'vehicle': result.get('vehicle_analysis'),
                'financial': result.get('financial_analysis')
            },
            "audio_url": audio_url,
            "transcription": user_query_text
        }

    except Exception as e:
        print(f"Voice Processing Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Cleanup temp file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
@router.post("/webhooks/whatsapp")
async def whatsapp_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """Handle WhatsApp webhook (Twilio)"""
    
    try:
        form_data = await request.form()
        
        from_number = form_data.get('From', '').replace('whatsapp:', '')
        message_body = form_data.get('Body', '')
        media_url = form_data.get('MediaUrl0')  # Voice message URL
        
        # Find user by WhatsApp number
        from sqlalchemy import select
        result = await db.execute(
            select(User).filter(User.whatsapp_number == from_number)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            # Send registration message
            from app.services import whatsapp_service
            whatsapp_service.send_message(
                f'whatsapp:{from_number}',
                "Welcome to Sarathi! Please register on our app first to get started."
            )
            return {"status": "user_not_found"}
        
        # Process message
        if media_url:
            # Voice message - download and process
            from app.services import whatsapp_service
            audio_data = await whatsapp_service.download_voice_message(media_url)
            
            if audio_data:
                from app.services import gemini_service
                
                # Transcribe
                transcription = await gemini_service.transcribe_audio(audio_data)
                
                # Extract trip info
                trip_info = await gemini_service.extract_trip_info(transcription)
                
                # Create trip automatically
                from app.models.trip import Trip
                from datetime import datetime, timedelta
                
                trip = Trip(
                    user_id=user.id,
                    start_location=trip_info.get('start_location', 'Unknown'),
                    end_location=trip_info.get('end_location', 'Unknown'),
                    start_time=datetime.now() - timedelta(hours=1),
                    end_time=datetime.now(),
                    earnings=trip_info.get('earnings', 0),
                    fuel_cost=trip_info.get('fuel_cost', 0),
                    toll_cost=trip_info.get('toll_cost', 0),
                    other_expenses=trip_info.get('other_expenses', 0),
                    transcription=transcription,
                    voice_message_url=media_url,
                    net_earnings=trip_info.get('earnings', 0) - (
                        trip_info.get('fuel_cost', 0) +
                        trip_info.get('toll_cost', 0) +
                        trip_info.get('other_expenses', 0)
                    )
                )
                
                db.add(trip)
                await db.commit()
                
                # Send confirmation
                whatsapp_service.send_message(
                    f'whatsapp:{from_number}',
                    f"✅ Trip logged!\n\n📍 {trip.start_location} → {trip.end_location}\n💰 ₹{trip.earnings:.2f}\n✅ Net: ₹{trip.net_earnings:.2f}"
                )
        
        else:
            # Text message - chat with agent
            agent = await create_sarathi_agent(db)
            
            user_profile = {
                'user_id': user.id,
                'name': user.name,
                'city': user.city,
                'vehicle_type': user.vehicle_type
            }
            
            result = await agent.process_query(
                user_id=user.id,
                query=message_body,
                user_profile=user_profile
            )
            
            # Send response via WhatsApp
            from app.services import whatsapp_service
            whatsapp_service.send_message(
                f'whatsapp:{from_number}',
                result['response']
            )
        
        return {"status": "success"}
    
    except Exception as e:
        print(f"WhatsApp webhook error: {e}")
        return {"status": "error", "message": str(e)}
