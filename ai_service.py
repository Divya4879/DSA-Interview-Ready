import os
import requests
import json
import hashlib
import assemblyai as aai
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.assemblyai_api_key = os.getenv('ASSEMBLYAI_API_KEY')
        aai.settings.api_key = self.assemblyai_api_key

    def transcribe_audio(self, audio_file_path):
        """
        Transcribe audio using AssemblyAI free tier
        """
        try:
            print(f"Starting transcription for: {audio_file_path}")
            
            # Check if file exists
            if not os.path.exists(audio_file_path):
                print(f"Audio file not found: {audio_file_path}")
                return None
            
            # Simple AssemblyAI transcription (free tier)
            transcriber = aai.Transcriber()
            
            print("Submitting audio for transcription...")
            transcript = transcriber.transcribe(audio_file_path)
            
            print(f"Transcription status: {transcript.status}")
            
            # Wait for transcription to complete
            if transcript.status == aai.TranscriptStatus.error:
                print(f"Transcription failed: {transcript.error}")
                return "Sorry, could not transcribe audio. Please type your explanation."
            
            if transcript.status == aai.TranscriptStatus.completed:
                print(f"Transcription successful: {transcript.text[:100] if transcript.text else 'No text'}...")
                return transcript.text if transcript.text else "No speech detected. Please try again."
            else:
                print(f"Transcription status: {transcript.status}")
                return "Transcription in progress. Please wait..."
            
        except Exception as e:
            print(f"AssemblyAI transcription error: {str(e)}")
            # Return a helpful fallback message
            return "Voice transcription temporarily unavailable. Please type your explanation in the text box below."

    def analyze_code(self, problem_id, code, explanation, language):
        """
        Analyze code using Groq API with correct free tier model
        """
        prompt = f"""Analyze this coding interview solution:

Problem: {problem_id}
Language: {language}

Code:
{code}

Explanation:
{explanation}

Provide analysis as JSON:
{{
  "code_quality": 85,
  "algorithm_efficiency": 75,
  "communication": 90,
  "problem_solving": 80,
  "feedback": "Clear solution with good variable names. Consider edge cases.",
  "strengths": ["Clean code", "Good explanation"],
  "improvements": ["Add error handling", "Optimize time complexity"],
  "recommendation": "Hire"
}}"""
        
        try:
            # Using llama3-8b-8192 model (free tier)
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",  # Correct endpoint
                headers={
                    "Authorization": f"Bearer {self.groq_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "messages": [
                        {
                            "role": "system", 
                            "content": "You are a senior software engineer conducting a technical interview. Provide constructive feedback in JSON format."
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    "model": "llama3-8b-8192",  # Free tier model
                    "temperature": 0.3,
                    "max_tokens": 1024,
                    "top_p": 1,
                    "stream": False
                }
            )
            
            if response.status_code != 200:
                print(f"Groq API error: {response.status_code} - {response.text}")
                raise Exception(f"Groq API error: {response.text}")
                
            response_data = response.json()
            analysis_text = response_data['choices'][0]['message']['content']
            
            # Clean and parse JSON response
            try:
                # Remove markdown formatting if present
                if "```json" in analysis_text:
                    analysis_text = analysis_text.split("```json")[1].split("```")[0]
                elif "```" in analysis_text:
                    analysis_text = analysis_text.split("```")[1]
                
                # Extract JSON from the response
                import re
                json_match = re.search(r'\{.*?\}', analysis_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    return json.loads(json_str)
                else:
                    raise json.JSONDecodeError("No JSON found", analysis_text, 0)
                
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {str(e)}")
                print(f"Raw response: {analysis_text}")
                
                # Extract scores using regex as fallback
                import re
                scores = {}
                
                # Try to extract scores from the text
                score_patterns = {
                    'code_quality': r'code[_\s]*quality["\s]*:\s*(\d+)',
                    'algorithm_efficiency': r'algorithm[_\s]*efficiency["\s]*:\s*(\d+)',
                    'communication': r'communication["\s]*:\s*(\d+)',
                    'problem_solving': r'problem[_\s]*solving["\s]*:\s*(\d+)'
                }
                
                for key, pattern in score_patterns.items():
                    match = re.search(pattern, analysis_text, re.IGNORECASE)
                    if match:
                        scores[key] = int(match.group(1))
                    else:
                        scores[key] = 75  # Default score
                
                # Fallback structured response
                return {
                    'code_quality': scores.get('code_quality', 75),
                    'algorithm_efficiency': scores.get('algorithm_efficiency', 70),
                    'communication': scores.get('communication', 80),
                    'problem_solving': scores.get('problem_solving', 75),
                    'feedback': analysis_text[:500] + "..." if len(analysis_text) > 500 else analysis_text,
                    'strengths': ['Code structure', 'Problem approach'],
                    'improvements': ['Edge cases', 'Error handling'],
                    'recommendation': 'Hire' if sum(scores.values()) / len(scores) > 70 else 'Need more evaluation'
                }
                
        except Exception as e:
            print(f"Groq API analysis error: {str(e)}")
            return {
                'error': str(e),
                'code_quality': 50,
                'algorithm_efficiency': 50,
                'communication': 50,
                'problem_solving': 50,
                'feedback': f'Analysis failed: {str(e)}. Please try again.',
                'strengths': ['Attempted the problem'],
                'improvements': ['Try submitting again'],
                'recommendation': 'Technical issue - retry needed'
            }

    def test_apis(self):
        """
        Test both APIs to ensure they're working
        """
        print("🧪 Testing AI APIs...")
        
        # Test Groq API
        try:
            test_analysis = self.analyze_code(
                "test_problem", 
                "def solution(): return True", 
                "This is a test solution", 
                "python"
            )
            if 'error' not in test_analysis:
                print("✅ Groq API working")
            else:
                print(f"❌ Groq API error: {test_analysis['error']}")
        except Exception as e:
            print(f"❌ Groq API test failed: {str(e)}")
        
        # Test AssemblyAI (just check if we can initialize)
        try:
            transcriber = aai.Transcriber()
            print("✅ AssemblyAI initialized")
        except Exception as e:
            print(f"❌ AssemblyAI test failed: {str(e)}")
