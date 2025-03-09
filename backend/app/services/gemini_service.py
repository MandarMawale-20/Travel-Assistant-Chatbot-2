import google.generativeai as genai
from app.core.config import settings

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        
    async def get_travel_recommendations(self, location, preferences=None, budget=None):
        prompt = f"Give me travel recommendations for {location}."
        
        if preferences:
            prompt += f" I'm interested in {preferences}."
            
        if budget:
            prompt += f" My budget is approximately {budget}."
            
        response = self.model.generate_content(prompt)
        return response.text
        
    async def answer_travel_query(self, query):
        # Add travel context to make responses more travel-focused
        prompt = f"As a travel assistant, answer this query: {query}"
        response = self.model.generate_content(prompt)
        return response.text

gemini_service = GeminiService()