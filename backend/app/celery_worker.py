from celery import Celery
from app.config import settings

celery_app = Celery(
    "sarathi",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    worker_prefetch_multiplier=1,
)

# Background task for sending WhatsApp notifications
@celery_app.task(name="send_whatsapp_notification")
def send_whatsapp_notification(to_number: str, message: str):
    """Send WhatsApp notification via Twilio"""
    from app.services.whatsapp_service import WhatsAppService
    service = WhatsAppService()
    return service.send_message(to_number, message)

# Background task for processing vehicle diagnostics
@celery_app.task(name="process_vehicle_diagnostics")
def process_vehicle_diagnostics(health_check_id: int):
    """Process vehicle images and generate diagnostic report"""
    # This would be implemented for async processing of large image batches
    pass

# Background task for generating daily earnings reports
@celery_app.task(name="generate_daily_earnings_report")
def generate_daily_earnings_report(user_id: int):
    """Generate and send daily earnings summary"""
    pass
