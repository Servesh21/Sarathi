from twilio.rest import Client
from app.config import settings
from typing import Optional
import httpx


class WhatsAppService:
    """Service for WhatsApp integration via Twilio"""
    
    def __init__(self):
        self.client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )
        self.from_number = settings.TWILIO_WHATSAPP_NUMBER
    
    def send_message(self, to_number: str, message: str) -> bool:
        """Send WhatsApp message"""
        try:
            # Ensure number is in WhatsApp format
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:+91{to_number.replace("+", "").replace(" ", "")}'
            
            message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            
            return message.sid is not None
        except Exception as e:
            print(f"WhatsApp message send error: {e}")
            return False
    
    def send_alert(
        self,
        to_number: str,
        alert_type: str,
        title: str,
        message: str
    ) -> bool:
        """Send formatted alert via WhatsApp"""
        formatted_message = f"""🚨 *{title}*

{message}

_Sarathi Alert - {alert_type}_"""
        
        return self.send_message(to_number, formatted_message)
    
    def send_earnings_summary(
        self,
        to_number: str,
        earnings: float,
        trips: int,
        net_profit: float
    ) -> bool:
        """Send daily earnings summary"""
        message = f"""📊 *Daily Earnings Summary*

💰 Total Earnings: ₹{earnings:.2f}
🚗 Total Trips: {trips}
✅ Net Profit: ₹{net_profit:.2f}

Keep up the great work!

_Sarathi - Your Financial Companion_"""
        
        return self.send_message(to_number, message)
    
    def send_vehicle_alert(
        self,
        to_number: str,
        issue: str,
        severity: str,
        action: str
    ) -> bool:
        """Send vehicle maintenance alert"""
        emoji = "🔴" if severity == "critical" else "🟡" if severity == "high" else "🟢"
        
        message = f"""{emoji} *Vehicle Alert*

⚠️ Issue: {issue}
📋 Action Required: {action}

Please address this soon to avoid breakdowns.

_Sarathi Vehicle Health Monitor_"""
        
        return self.send_message(to_number, message)
    
    def send_goal_reminder(
        self,
        to_number: str,
        goal_name: str,
        progress: float,
        target: float
    ) -> bool:
        """Send goal progress reminder"""
        percentage = (progress / target) * 100
        
        message = f"""🎯 *Goal Update: {goal_name}*

Progress: ₹{progress:.2f} / ₹{target:.2f} ({percentage:.1f}%)

You're doing great! Keep saving consistently.

_Sarathi Goal Tracker_"""
        
        return self.send_message(to_number, message)
    
    async def download_voice_message(self, media_url: str) -> Optional[bytes]:
        """Download voice message from WhatsApp"""
        try:
            async with httpx.AsyncClient() as client:
                # Authenticate with Twilio credentials
                auth = (settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                response = await client.get(media_url, auth=auth)
                
                if response.status_code == 200:
                    return response.content
                return None
        except Exception as e:
            print(f"Voice message download error: {e}")
            return None


# Singleton instance
whatsapp_service = WhatsAppService()
