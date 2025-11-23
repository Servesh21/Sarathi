from typing import Dict, Any
from app.agents.state import AgentState
from app.agents.tools import DatabaseTool
from app.services import gemini_service
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.config import settings
from datetime import datetime, timedelta


class DiagnosticAgent:
    """Node that handles vehicle diagnostics and maintenance"""
    
    def __init__(self, db_tool: DatabaseTool):
        self.db_tool = db_tool
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.5
        )
    
    async def __call__(self, state: AgentState) -> AgentState:
        """Provide vehicle diagnostic insights"""
        
        # Get vehicle information
        vehicle_info = await self.db_tool.get_vehicle_info(state['user_id'])
        latest_check = await self.db_tool.get_latest_vehicle_check(state['user_id'])
        
        recommendations = []
        alerts = []
        
        if not vehicle_info:
            state['response'] = "I don't have your vehicle information yet. Please add your vehicle details first."
            state['next_step'] = 'end'
            return state
        
        # Check for document expiry
        if vehicle_info.get('insurance_expiry'):
            insurance_expiry = datetime.fromisoformat(vehicle_info['insurance_expiry'])
            days_to_expiry = (insurance_expiry - datetime.now()).days
            
            if days_to_expiry < 0:
                alerts.append({
                    'type': 'critical',
                    'message': '🔴 Insurance expired! Renew immediately to avoid legal issues.'
                })
            elif days_to_expiry < 30:
                alerts.append({
                    'type': 'warning',
                    'message': f'⚠️ Insurance expiring in {days_to_expiry} days. Renew soon.'
                })
        
        # Check for service due
        if vehicle_info.get('current_odometer_km') and vehicle_info.get('next_service_due_km'):
            current_km = vehicle_info['current_odometer_km']
            service_due_km = vehicle_info['next_service_due_km']
            
            if current_km >= service_due_km:
                alerts.append({
                    'type': 'maintenance',
                    'message': f'🔧 Service overdue! Current: {current_km}km, Due: {service_due_km}km'
                })
            elif service_due_km - current_km < 500:
                alerts.append({
                    'type': 'maintenance',
                    'message': f'🔧 Service due soon. {service_due_km - current_km:.0f}km remaining.'
                })
        
        # Analyze latest health check
        if latest_check:
            severity = latest_check.get('severity_score', 0)
            
            if severity > 70:
                alerts.append({
                    'type': 'critical',
                    'message': f'🔴 Critical issues detected (severity: {severity}/100). Immediate attention required!'
                })
            elif severity > 40:
                alerts.append({
                    'type': 'warning',
                    'message': f'⚠️ Moderate issues detected (severity: {severity}/100). Schedule maintenance soon.'
                })
            
            if latest_check.get('immediate_action_required'):
                recommendations.append({
                    'type': 'urgent',
                    'title': 'Immediate Action Required',
                    'description': latest_check.get('recommendations', 'Please check vehicle condition')
                })
            
            # Component-specific recommendations
            if latest_check.get('tire_condition') in ['poor', 'critical']:
                recommendations.append({
                    'type': 'component',
                    'title': 'Tire Replacement Needed',
                    'description': 'Worn tires reduce safety and fuel efficiency. Replace soon.'
                })
            
            if latest_check.get('engine_oil_level') in ['low', 'critical']:
                recommendations.append({
                    'type': 'component',
                    'title': 'Engine Oil Top-up',
                    'description': 'Low engine oil can damage the engine. Top up immediately.'
                })
            
            if latest_check.get('brake_condition') in ['poor', 'critical']:
                recommendations.append({
                    'type': 'component',
                    'title': 'Brake Service Required',
                    'description': 'Brake issues are safety-critical. Get them checked ASAP.'
                })
        else:
            recommendations.append({
                'type': 'info',
                'title': 'Upload Vehicle Photos',
                'description': 'Upload photos of your vehicle for AI-powered health diagnostics.'
            })
        
        # Detect fatigue from work pattern
        trip_history = await self.db_tool.get_trip_history(state['user_id'], days=7)
        
        if len(trip_history) > 0:
            # Calculate daily average trips
            daily_trips = len(trip_history) / 7
            
            if daily_trips > 20:
                recommendations.append({
                    'type': 'health',
                    'title': 'High Work Intensity Detected',
                    'description': f'You average {daily_trips:.1f} trips/day. Consider taking regular breaks to avoid burnout.'
                })
        
        # Update state
        state['vehicle_analysis'] = {
            'vehicle_info': vehicle_info,
            'latest_check': latest_check,
            'alerts': alerts
        }
        state['recommendations'] = recommendations
        
        # Generate response
        response_prompt = f"""Based on vehicle diagnostic data, provide helpful maintenance advice:

Vehicle: {vehicle_info.get('make', 'Unknown')} {vehicle_info.get('model', '')} ({vehicle_info.get('vehicle_type', '')})
Current Odometer: {vehicle_info.get('current_odometer_km', 0):.0f} km

Alerts:
{chr(10).join([a['message'] for a in alerts]) if alerts else "No critical alerts"}

Recommendations:
{chr(10).join([f"- {r['title']}: {r['description']}" for r in recommendations[:3]]) if recommendations else "Vehicle appears to be in good condition"}

Latest Health Check:
{f"Severity: {latest_check.get('severity_score', 'N/A')}/100" if latest_check else "No recent diagnostics"}

Provide friendly, supportive advice. Keep it concise (3-4 sentences)."""
        
        messages = state['messages'] + [
            SystemMessage(content="You are Sarathi, a vehicle health advisor. Provide clear maintenance guidance."),
            HumanMessage(content=response_prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        state['response'] = response.content
        state['action_items'] = [r['title'] for r in recommendations[:3]]
        state['messages'].append(AIMessage(content=response.content))
        state['next_step'] = 'end'
        
        return state
