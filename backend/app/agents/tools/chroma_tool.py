from typing import Dict, Any, List
from app.database import get_chroma_client
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import settings


class ChromaTool:
    """Tool for vector database operations"""
    
    def __init__(self):
        self.client = get_chroma_client()
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=settings.GOOGLE_API_KEY
        )
    
    async def store_trip_pattern(
        self,
        trip_data: Dict[str, Any],
        user_id: int
    ):
        """Store trip pattern in vector database"""
        collection = self.client.get_or_create_collection("trip_patterns")
        
        # Create searchable text from trip data
        text = f"""
        Trip from {trip_data.get('start_location')} to {trip_data.get('end_location')}
        Earnings: ₹{trip_data.get('earnings')}
        Distance: {trip_data.get('distance_km')}km
        Time: {trip_data.get('created_at')}
        Zone rating: {trip_data.get('zone_rating')}
        """
        
        embedding = self.embeddings.embed_query(text)
        
        collection.add(
            embeddings=[embedding],
            documents=[text],
            metadatas=[{
                'user_id': user_id,
                'trip_id': trip_data.get('id'),
                'earnings': trip_data.get('earnings'),
                'zone_rating': trip_data.get('zone_rating', 0)
            }],
            ids=[f"trip_{user_id}_{trip_data.get('id')}"]
        )
    
    async def find_similar_trips(
        self,
        query: str,
        user_id: int,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Find similar trips based on query"""
        collection = self.client.get_or_create_collection("trip_patterns")
        
        query_embedding = self.embeddings.embed_query(query)
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where={"user_id": user_id}
        )
        
        similar_trips = []
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                similar_trips.append({
                    'document': doc,
                    'metadata': results['metadatas'][0][i],
                    'similarity': 1 - results['distances'][0][i]
                })
        
        return similar_trips
    
    async def store_vehicle_diagnostic(
        self,
        diagnostic_data: Dict[str, Any],
        vehicle_id: int
    ):
        """Store vehicle diagnostic in vector database"""
        collection = self.client.get_or_create_collection("vehicle_diagnostics")
        
        text = f"""
        Vehicle diagnostic:
        Severity: {diagnostic_data.get('severity_score')}
        Issues: {diagnostic_data.get('detected_issues')}
        Recommendations: {diagnostic_data.get('recommendations')}
        Tire: {diagnostic_data.get('tire_condition')}
        Oil: {diagnostic_data.get('engine_oil_level')}
        Brakes: {diagnostic_data.get('brake_condition')}
        """
        
        embedding = self.embeddings.embed_query(text)
        
        collection.add(
            embeddings=[embedding],
            documents=[text],
            metadatas=[{
                'vehicle_id': vehicle_id,
                'check_id': diagnostic_data.get('id'),
                'severity_score': diagnostic_data.get('severity_score', 0)
            }],
            ids=[f"diagnostic_{vehicle_id}_{diagnostic_data.get('id')}"]
        )
    
    async def store_financial_advice(
        self,
        advice: str,
        user_id: int,
        context: Dict[str, Any]
    ):
        """Store financial advice in vector database"""
        collection = self.client.get_or_create_collection("financial_advice")
        
        embedding = self.embeddings.embed_query(advice)
        
        collection.add(
            embeddings=[embedding],
            documents=[advice],
            metadatas=[{
                'user_id': user_id,
                'surplus': context.get('surplus', 0),
                'risk_profile': context.get('risk_profile', 'low')
            }],
            ids=[f"advice_{user_id}_{hash(advice)}"]
        )
    
    async def retrieve_context(
        self,
        query: str,
        collection_name: str,
        top_k: int = 3
    ) -> List[str]:
        """Retrieve relevant context from vector database"""
        collection = self.client.get_or_create_collection(collection_name)
        
        query_embedding = self.embeddings.embed_query(query)
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        if results['documents']:
            return results['documents'][0]
        return []
