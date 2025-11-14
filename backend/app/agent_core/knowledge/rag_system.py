"""
Advanced RAG-based Knowledge Management System for Sarathi
Provides contextual knowledge about gig work, vehicle maintenance, financial strategies
Uses ChromaDB for vector storage and retrieval
"""
import os
import uuid
import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document
import logging

logger = logging.getLogger(__name__)

@dataclass
class KnowledgeItem:
    """Represents a piece of domain knowledge"""
    content: str
    metadata: Dict[str, Any]
    category: str  # 'earnings', 'vehicle', 'health', 'financial', 'regulatory'
    priority: float  # 0.0 to 1.0, higher = more critical
    last_updated: str

class SarathiKnowledgeBase:
    """
    Advanced RAG system specifically designed for gig work domain knowledge
    """
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Collections for different types of knowledge
        self.collections = {
            'earnings_optimization': self._get_or_create_collection('earnings_optimization'),
            'vehicle_health': self._get_or_create_collection('vehicle_health'),
            'financial_strategies': self._get_or_create_collection('financial_strategies'),
            'health_wellness': self._get_or_create_collection('health_wellness'),
            'regulatory_compliance': self._get_or_create_collection('regulatory_compliance'),
            'market_intelligence': self._get_or_create_collection('market_intelligence'),
        }
        
        # Initialize knowledge if empty
        asyncio.create_task(self._initialize_domain_knowledge())
    
    def _get_or_create_collection(self, name: str):
        """Get or create a ChromaDB collection"""
        try:
            return self.client.get_collection(name)
        except Exception:
            return self.client.create_collection(name)
    
    async def _initialize_domain_knowledge(self):
        """Initialize the knowledge base with domain-specific knowledge"""
        
        # Check if knowledge already exists
        earnings_count = self.collections['earnings_optimization'].count()
        if earnings_count > 0:
            logger.info("Knowledge base already initialized")
            return
        
        logger.info("Initializing Sarathi knowledge base...")
        
        # Core gig work knowledge
        core_knowledge = [
            # Earnings Optimization
            KnowledgeItem(
                content="""Peak earnings hours for ride-hailing drivers in Indian metro cities:
                Mumbai: 8-10 AM, 6-9 PM weekdays; 7 PM - 2 AM weekends
                Delhi: 7-9 AM, 5-8 PM weekdays; 8 PM - 1 AM weekends
                Bangalore: 8-10 AM, 6-9 PM weekdays; 9 PM - 2 AM weekends
                Hyderabad: 8-10 AM, 6-8 PM weekdays; 8 PM - 1 AM weekends
                
                Surge pricing typically occurs during:
                - Morning office hours (8-10 AM)
                - Evening rush (5-8 PM)
                - Late nights on weekends (9 PM - 2 AM)
                - Rainy days (30-50% higher earnings)
                - Festival seasons (20-40% increase)
                
                Airport runs are most profitable: 3x regular fare, especially early morning (5-7 AM) and late night (10 PM - 2 AM)""",
                metadata={"source": "driver_insights", "city": "all", "reliability": 0.95},
                category="earnings",
                priority=1.0,
                last_updated="2024-11-14"
            ),
            
            # Vehicle Health Prediction
            KnowledgeItem(
                content="""Vehicle breakdown prediction indicators for high-mileage vehicles:
                
                CRITICAL WARNING SIGNS (Immediate attention needed):
                - Engine temperature > 90°C consistently
                - Brake pad thickness < 3mm
                - Tire tread depth < 2mm
                - Engine oil change overdue by >1000km
                - Battery voltage < 12.4V when engine off
                - Strange noises: grinding (brakes), knocking (engine), squealing (belts)
                
                PREDICTIVE MAINTENANCE SCHEDULE:
                Daily (100+ km/day drivers):
                - Check tire pressure, engine oil level, brake fluid
                - Monitor fuel efficiency (sudden drops indicate issues)
                
                Weekly:
                - Inspect tires for wear patterns
                - Check all lights and electrical systems
                - Clean air filter if dusty conditions
                
                Monthly:
                - Professional inspection if >3000km/month
                - Rotate tires, check alignment
                - Service AC system (crucial for driver comfort)
                
                COST-SAVING TIPS:
                - Use genuine spare parts only for safety-critical components
                - Group multiple services together to save labor costs
                - Maintain relationship with trusted mechanic for 20-30% discounts""",
                metadata={"source": "mechanic_network", "reliability": 0.92},
                category="vehicle",
                priority=1.0,
                last_updated="2024-11-14"
            ),
            
            # Financial Resilience Strategies
            KnowledgeItem(
                content="""Financial resilience strategies for gig workers:
                
                EMERGENCY FUND BUILDING:
                1. Start with ₹500/week minimum savings (even during low earnings)
                2. Target: 3 months of expenses (₹45,000-60,000 for most drivers)
                3. Keep in liquid savings account, not fixed deposits
                4. Build gradually: Week 1-4: ₹500, Week 5-8: ₹750, Week 9+: ₹1000
                
                INCOME DIVERSIFICATION:
                - Multi-platform strategy: Ola + Uber + Rapido/food delivery
                - Peak hours on ride-hailing, off-peak on food delivery
                - Weekend long-distance trips (3x hourly rate)
                - Festival season opportunities: decorations pickup/delivery
                
                TAX OPTIMIZATION:
                - Claim vehicle expenses: fuel, maintenance, insurance (40-60% of income)
                - Keep all receipts digitally (smartphone apps)
                - Quarterly GST filing for >20 lakh annual income
                - Professional consultation worth the cost above 15 lakh income
                
                WEALTH BUILDING:
                - SIP in diversified equity funds: ₹2000-5000/month minimum
                - PPF for tax savings: ₹1500/month (lock-in acceptable for drivers)
                - Avoid insurance as investment - term insurance + separate investment better
                - Real estate investment only after 2+ years of stable high earnings""",
                metadata={"source": "financial_advisors", "reliability": 0.88},
                category="financial",
                priority=0.9,
                last_updated="2024-11-14"
            ),
            
            # Driver Health & Burnout Prevention
            KnowledgeItem(
                content="""Driver health and burnout prevention for gig workers:
                
                PHYSICAL HEALTH INDICATORS:
                - Back/neck pain after <4 hours driving (seat adjustment needed)
                - Eye strain/headaches (vision check, better lighting)
                - Frequent urination issues (dehydration or diabetes warning)
                - Weight gain >5kg in 6 months (sedentary lifestyle impact)
                
                MENTAL HEALTH WARNING SIGNS:
                - Irritability with passengers (stress response)
                - Avoiding family time (overwork compensation)
                - Sleep issues despite physical exhaustion
                - Anxiety about daily earnings targets
                
                PREVENTION STRATEGIES:
                Daily:
                - 15-minute walks every 3 hours of driving
                - Proper hydration: 3-4 liters water (not just tea/coffee)
                - Healthy snacks: bananas, nuts, dates (avoid heavy meals)
                
                Weekly:
                - Minimum 1 full day rest (earnings vs health balance)
                - Basic exercise: walking, stretching, yoga
                - Social activities away from vehicle
                
                Monthly:
                - Health checkup if >5000km/month driving
                - Eye exam annually (vision critical for safety)
                - Mental health consultation if stress continues
                
                ERGONOMIC SETUP:
                - Seat height: thighs parallel to floor
                - Back support: maintains natural curve
                - Mirrors adjusted to minimize neck movement
                - Frequent seat position changes during long trips""",
                metadata={"source": "health_experts", "reliability": 0.91},
                category="health",
                priority=0.95,
                last_updated="2024-11-14"
            ),
            
            # Market Intelligence
            KnowledgeItem(
                content="""Real-time market intelligence for maximizing earnings:
                
                DEMAND PREDICTION PATTERNS:
                Weather-based surge:
                - Light rain: +20-30% demand
                - Heavy rain: +50-80% demand, fewer drivers
                - Extreme weather: Airport/railway station runs peak
                
                Event-based opportunities:
                - Cricket matches: 2-3x normal rates in venue vicinity
                - Concerts/festivals: Plan positioning 30min before event ends
                - Wedding season (Nov-Feb): Late night premium runs
                - Office party season (Dec): Higher tips, corporate bookings
                
                LOCATION INTELLIGENCE:
                High-value pickup zones:
                - Business districts: 9-11 AM, 2-4 PM
                - Malls/restaurants: 12-2 PM, 7-10 PM
                - Airports: Early morning (5-8 AM), late night (10 PM-1 AM)
                - Hotels: International travelers (higher tips)
                
                COMPETITION ANALYSIS:
                - Ola vs Uber pricing: Switch platforms based on surge
                - Driver density monitoring: Avoid oversaturated areas
                - Customer waiting times: Position in areas with high wait times
                
                SEASONAL STRATEGIES:
                Monsoon (Jun-Sep): Focus on covered pickup points, higher acceptance rate
                Festival season (Oct-Nov): Religious site shuttles, decoration transport
                Winter (Dec-Feb): Wedding transportation, late-night party runs
                Summer (Mar-May): Early morning/late evening operations, AC maintenance crucial""",
                metadata={"source": "driver_network", "reliability": 0.87},
                category="earnings",
                priority=0.85,
                last_updated="2024-11-14"
            )
        ]
        
        # Add knowledge to appropriate collections
        for knowledge in core_knowledge:
            await self.add_knowledge(knowledge)
        
        logger.info(f"Added {len(core_knowledge)} knowledge items to the knowledge base")
    
    async def add_knowledge(self, knowledge_item: KnowledgeItem):
        """Add a knowledge item to the appropriate collection"""
        try:
            # Determine collection based on category
            collection_map = {
                'earnings': 'earnings_optimization',
                'vehicle': 'vehicle_health',
                'financial': 'financial_strategies',
                'health': 'health_wellness',
                'regulatory': 'regulatory_compliance',
                'market': 'market_intelligence'
            }
            
            collection_name = collection_map.get(knowledge_item.category, 'earnings_optimization')
            collection = self.collections[collection_name]
            
            # Split text if needed
            chunks = self.text_splitter.split_text(knowledge_item.content)
            
            # Prepare documents
            documents = []
            metadatas = []
            ids = []
            
            for i, chunk in enumerate(chunks):
                doc_id = f"{knowledge_item.category}_{uuid.uuid4().hex[:8]}_{i}"
                
                documents.append(chunk)
                metadatas.append({
                    **knowledge_item.metadata,
                    'category': knowledge_item.category,
                    'priority': knowledge_item.priority,
                    'last_updated': knowledge_item.last_updated,
                    'chunk_index': i
                })
                ids.append(doc_id)
            
            # Add to ChromaDB
            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added knowledge item with {len(chunks)} chunks to {collection_name}")
            
        except Exception as e:
            logger.error(f"Error adding knowledge item: {str(e)}")
    
    async def retrieve_contextual_knowledge(
        self, 
        query: str, 
        category: Optional[str] = None,
        top_k: int = 5,
        min_relevance: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant knowledge based on query"""
        try:
            results = []
            
            # Determine which collections to search
            search_collections = []
            if category:
                collection_map = {
                    'earnings': ['earnings_optimization', 'market_intelligence'],
                    'vehicle': ['vehicle_health'],
                    'financial': ['financial_strategies'],
                    'health': ['health_wellness'],
                    'regulatory': ['regulatory_compliance']
                }
                search_collections = collection_map.get(category, list(self.collections.keys()))
            else:
                search_collections = list(self.collections.keys())
            
            # Search each relevant collection
            for collection_name in search_collections:
                collection = self.collections[collection_name]
                
                try:
                    # Query the collection
                    query_results = collection.query(
                        query_texts=[query],
                        n_results=top_k,
                        include=['documents', 'metadatas', 'distances']
                    )
                    
                    # Process results
                    if query_results['documents'][0]:
                        for i, (doc, metadata, distance) in enumerate(zip(
                            query_results['documents'][0],
                            query_results['metadatas'][0],
                            query_results['distances'][0]
                        )):
                            # Convert distance to similarity score (lower distance = higher similarity)
                            similarity = 1.0 - distance
                            
                            if similarity >= min_relevance:
                                results.append({
                                    'content': doc,
                                    'metadata': metadata,
                                    'similarity': similarity,
                                    'collection': collection_name,
                                    'priority': metadata.get('priority', 0.5)
                                })
                
                except Exception as e:
                    logger.warning(f"Error searching collection {collection_name}: {str(e)}")
                    continue
            
            # Sort by relevance and priority
            results.sort(key=lambda x: (x['similarity'] * x['priority']), reverse=True)
            
            return results[:top_k]
            
        except Exception as e:
            logger.error(f"Error retrieving knowledge: {str(e)}")
            return []
    
    async def get_proactive_insights(self, user_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get proactive insights based on user context and patterns"""
        try:
            insights = []
            
            # Analyze user context to provide proactive suggestions
            earnings_data = user_context.get('earnings', {})
            vehicle_data = user_context.get('vehicle', {})
            health_data = user_context.get('health', {})
            
            # Earnings optimization insights
            if earnings_data:
                avg_daily = earnings_data.get('avg_daily_earnings', 0)
                if avg_daily < 1200:  # Below average threshold
                    low_earnings_query = "strategies to increase daily earnings below average"
                    earnings_insights = await self.retrieve_contextual_knowledge(
                        low_earnings_query, 
                        category='earnings',
                        top_k=2
                    )
                    insights.extend(earnings_insights)
            
            # Vehicle health insights
            if vehicle_data:
                km_since_service = vehicle_data.get('km_since_service', 0)
                if km_since_service > 3000:  # Due for service
                    vehicle_query = "vehicle maintenance schedule preventive care"
                    vehicle_insights = await self.retrieve_contextual_knowledge(
                        vehicle_query,
                        category='vehicle',
                        top_k=2
                    )
                    insights.extend(vehicle_insights)
            
            # Health and wellness insights
            days_worked = user_context.get('consecutive_work_days', 0)
            if days_worked > 10:  # Overwork pattern
                health_query = "driver burnout prevention rest schedule"
                health_insights = await self.retrieve_contextual_knowledge(
                    health_query,
                    category='health',
                    top_k=2
                )
                insights.extend(health_insights)
            
            return insights[:5]  # Return top 5 proactive insights
            
        except Exception as e:
            logger.error(f"Error generating proactive insights: {str(e)}")
            return []
    
    async def update_knowledge_from_experience(self, user_feedback: Dict[str, Any]):
        """Update knowledge base based on real user experiences and feedback"""
        try:
            # This would implement continuous learning from user interactions
            # For now, we'll log the feedback for future implementation
            logger.info(f"User feedback logged for knowledge improvement: {user_feedback}")
            
            # Future implementation would:
            # 1. Analyze successful strategies reported by users
            # 2. Update relevance scores based on feedback
            # 3. Add new knowledge from verified user experiences
            # 4. Deprecate outdated information
            
        except Exception as e:
            logger.error(f"Error updating knowledge from experience: {str(e)}")

# Global knowledge base instance
knowledge_base = SarathiKnowledgeBase()