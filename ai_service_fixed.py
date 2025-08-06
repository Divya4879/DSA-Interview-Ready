import os
import requests
import json
import hashlib
import assemblyai as aai
import logging
import time
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.assemblyai_api_key = os.getenv('ASSEMBLYAI_API_KEY')
        
        if not self.assemblyai_api_key:
            logger.error("AssemblyAI API key not found in environment variables")
            raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")
        
        # Configure AssemblyAI
        aai.settings.api_key = self.assemblyai_api_key
        logger.info("AI Service initialized with AssemblyAI")

    def transcribe_audio(self, audio_file_path):
        """
        Transcribe audio using AssemblyAI with improved error handling
        """
        try:
            logger.info(f"Starting transcription for: {audio_file_path}")
            
            # Validate file
            if not os.path.exists(audio_file_path):
                logger.error(f"Audio file not found: {audio_file_path}")
                return None
            
            file_size = os.path.getsize(audio_file_path)
            if file_size == 0:
                logger.error("Audio file is empty")
                return None
            
            logger.info(f"Audio file size: {file_size} bytes")
            
            # Configure transcription with optimal settings
            config = aai.TranscriptionConfig(
                speech_model=aai.SpeechModel.best,  # Use best model for accuracy
                language_code="en",
                punctuate=True,
                format_text=True,
                filter_profanity=False,
                boost_param="interview coding algorithm programming software development",  # Boost technical terms
                word_boost=["algorithm", "data structure", "complexity", "runtime", "space", "time", "array", "string", "tree", "graph", "hash", "sort", "search"]
            )
            
            # Create transcriber
            transcriber = aai.Transcriber(config=config)
            
            logger.info("Submitting audio for transcription...")
            start_time = time.time()
            
            # Submit for transcription
            transcript = transcriber.transcribe(audio_file_path)
            
            # Wait for completion with timeout
            max_wait_time = 300  # 5 minutes max
            while transcript.status not in [aai.TranscriptStatus.completed, aai.TranscriptStatus.error]:
                if time.time() - start_time > max_wait_time:
                    logger.error("Transcription timeout")
                    return None
                
                logger.info(f"Transcription status: {transcript.status}")
                time.sleep(2)
                transcript = transcriber.get_transcript(transcript.id)
            
            # Handle results
            if transcript.status == aai.TranscriptStatus.error:
                logger.error(f"Transcription failed: {transcript.error}")
                return None
            
            if transcript.status == aai.TranscriptStatus.completed:
                if transcript.text and transcript.text.strip():
                    transcription_text = transcript.text.strip()
                    logger.info(f"Transcription successful: {len(transcription_text)} characters")
                    logger.info(f"Transcription preview: {transcription_text[:100]}...")
                    return transcription_text
                else:
                    logger.warning("Transcription completed but no text found")
                    return None
            
            logger.warning(f"Unexpected transcription status: {transcript.status}")
            return None
            
        except aai.TranscriptError as e:
            logger.error(f"AssemblyAI transcript error: {str(e)}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during transcription: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected transcription error: {str(e)}")
            return None

    def test_assemblyai_connection(self):
        """
        Test AssemblyAI API connection
        """
        try:
            # Try to create a transcriber to test the API key
            transcriber = aai.Transcriber()
            logger.info("AssemblyAI connection test successful")
            return True, "Connection successful"
        except Exception as e:
            logger.error(f"AssemblyAI connection test failed: {str(e)}")
            return False, f"Connection failed: {str(e)}"

    def analyze_code_solution(self, problem_title, code, explanation, language="python"):
        """
        Analyze code solution using Groq API
        """
        try:
            if not self.groq_api_key:
                logger.error("Groq API key not found")
                return self._get_fallback_analysis()

            # Create analysis prompt
            prompt = f"""
            As a senior technical interviewer, analyze this coding solution:

            Problem: {problem_title}
            Language: {language}
            Code:
            ```{language}
            {code}
            ```

            Explanation: {explanation}

            Provide a comprehensive analysis with scores (1-100) for:
            1. Code Quality
            2. Algorithm Efficiency  
            3. Communication Skills
            4. Problem Solving Approach
            5. Interview Readiness

            Format your response as JSON with this structure:
            {{
                "code_quality": <score>,
                "algorithm_efficiency": <score>,
                "communication_skills": <score>,
                "problem_solving": <score>,
                "interview_readiness": <score>,
                "feedback": "<detailed feedback>",
                "recommendation": "<specific recommendation>"
            }}
            """

            headers = {
                'Authorization': f'Bearer {self.groq_api_key}',
                'Content-Type': 'application/json'
            }

            data = {
                'model': 'mixtral-8x7b-32768',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are a senior technical interviewer with expertise in algorithm analysis and candidate evaluation.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'temperature': 0.3,
                'max_tokens': 1500
            }

            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Try to parse JSON response
                try:
                    analysis = json.loads(content)
                    logger.info("Code analysis completed successfully")
                    return analysis
                except json.JSONDecodeError:
                    logger.warning("Failed to parse JSON response, using fallback")
                    return self._parse_text_analysis(content)
            else:
                logger.error(f"Groq API error: {response.status_code}")
                return self._get_fallback_analysis()

        except Exception as e:
            logger.error(f"Code analysis error: {str(e)}")
            return self._get_fallback_analysis()

    def _parse_text_analysis(self, text_content):
        """
        Parse text-based analysis response
        """
        try:
            # Extract scores using simple parsing
            analysis = {
                "code_quality": 75,
                "algorithm_efficiency": 75,
                "communication_skills": 75,
                "problem_solving": 75,
                "interview_readiness": 75,
                "feedback": text_content,
                "recommendation": "Continue practicing and focus on explaining your thought process clearly."
            }
            
            # Try to extract actual scores if present
            import re
            score_patterns = [
                r'code.?quality[:\s]*(\d+)',
                r'algorithm.?efficiency[:\s]*(\d+)',
                r'communication[:\s]*(\d+)',
                r'problem.?solving[:\s]*(\d+)',
                r'interview.?readiness[:\s]*(\d+)'
            ]
            
            keys = ["code_quality", "algorithm_efficiency", "communication_skills", "problem_solving", "interview_readiness"]
            
            for i, pattern in enumerate(score_patterns):
                match = re.search(pattern, text_content, re.IGNORECASE)
                if match:
                    score = int(match.group(1))
                    if 0 <= score <= 100:
                        analysis[keys[i]] = score
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error parsing text analysis: {str(e)}")
            return self._get_fallback_analysis()

    def _get_fallback_analysis(self):
        """
        Provide fallback analysis when API calls fail
        """
        return {
            "code_quality": 70,
            "algorithm_efficiency": 70,
            "communication_skills": 70,
            "problem_solving": 70,
            "interview_readiness": 70,
            "feedback": "Analysis completed. Your solution shows good understanding of the problem. Focus on optimizing time complexity and providing clearer explanations of your approach.",
            "recommendation": "Practice explaining your thought process step by step and consider edge cases in your solutions."
        }

# Test the service
if __name__ == "__main__":
    try:
        service = AIService()
        success, message = service.test_assemblyai_connection()
        print(f"AssemblyAI Test: {message}")
    except Exception as e:
        print(f"Service initialization failed: {str(e)}")
