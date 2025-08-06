import os
import time
import tempfile
import assemblyai as aai
from flask import request, jsonify
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceTranscriptionService:
    def __init__(self, api_key):
        self.api_key = api_key
        if not api_key:
            logger.error("AssemblyAI API key not provided")
            raise ValueError("AssemblyAI API key is required")
        
        aai.settings.api_key = api_key
        logger.info("AssemblyAI service initialized")

    def transcribe_audio(self, audio_file_path):
        """
        Transcribe audio using AssemblyAI with proper error handling
        """
        try:
            logger.info(f"Starting transcription for: {audio_file_path}")
            
            # Check if file exists and has content
            if not os.path.exists(audio_file_path):
                logger.error(f"Audio file not found: {audio_file_path}")
                return None
            
            file_size = os.path.getsize(audio_file_path)
            if file_size == 0:
                logger.error("Audio file is empty")
                return None
            
            logger.info(f"Audio file size: {file_size} bytes")
            
            # Configure transcription settings
            config = aai.TranscriptionConfig(
                speech_model=aai.SpeechModel.best,
                language_code="en",
                punctuate=True,
                format_text=True,
                filter_profanity=False
            )
            
            # Create transcriber with config
            transcriber = aai.Transcriber(config=config)
            
            logger.info("Submitting audio for transcription...")
            transcript = transcriber.transcribe(audio_file_path)
            
            logger.info(f"Transcription status: {transcript.status}")
            
            # Handle different transcript statuses
            if transcript.status == aai.TranscriptStatus.error:
                logger.error(f"Transcription failed: {transcript.error}")
                return None
            
            if transcript.status == aai.TranscriptStatus.completed:
                if transcript.text and transcript.text.strip():
                    logger.info(f"Transcription successful: {len(transcript.text)} characters")
                    return transcript.text.strip()
                else:
                    logger.warning("Transcription completed but no text found")
                    return None
            else:
                logger.warning(f"Unexpected transcription status: {transcript.status}")
                return None
            
        except aai.TranscriptError as e:
            logger.error(f"AssemblyAI transcript error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}")
            return None

def process_voice_explanation_fixed():
    """
    Fixed voice explanation endpoint with better error handling
    """
    try:
        # Validate request
        if 'audio' not in request.files:
            logger.warning("No audio file in request")
            return jsonify({
                'success': False,
                'error': 'No audio file provided'
            }), 400
        
        audio_file = request.files['audio']
        if not audio_file or audio_file.filename == '':
            logger.warning("Empty audio file")
            return jsonify({
                'success': False,
                'error': 'No audio file selected'
            }), 400
        
        # Log file info
        logger.info(f"Received audio file: {audio_file.filename}, Content-Type: {audio_file.content_type}")
        
        # Create secure temp file
        temp_fd, temp_path = tempfile.mkstemp(suffix='.webm', prefix='audio_')
        
        try:
            # Save audio file
            with os.fdopen(temp_fd, 'wb') as temp_file:
                audio_data = audio_file.read()
                if len(audio_data) == 0:
                    raise ValueError("Audio file contains no data")
                
                temp_file.write(audio_data)
                logger.info(f"Saved audio file: {len(audio_data)} bytes to {temp_path}")
            
            # Get AssemblyAI API key from environment
            api_key = os.getenv('ASSEMBLYAI_API_KEY')
            if not api_key:
                logger.error("AssemblyAI API key not found in environment")
                return jsonify({
                    'success': False,
                    'error': 'Transcription service not configured'
                }), 500
            
            # Initialize transcription service
            voice_service = VoiceTranscriptionService(api_key)
            
            # Transcribe audio
            transcription = voice_service.transcribe_audio(temp_path)
            
            if transcription:
                logger.info("Transcription successful")
                return jsonify({
                    'success': True,
                    'transcription': transcription
                })
            else:
                logger.warning("Transcription returned empty result")
                return jsonify({
                    'success': False,
                    'error': 'Could not transcribe audio. Please ensure you spoke clearly and try again.'
                }), 422
                
        finally:
            # Clean up temp file
            try:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    logger.info(f"Cleaned up temp file: {temp_path}")
            except Exception as cleanup_error:
                logger.warning(f"Failed to cleanup temp file: {cleanup_error}")
        
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        return jsonify({
            'success': False,
            'error': str(ve)
        }), 400
    
    except Exception as e:
        logger.error(f"Unexpected error in voice explanation: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error occurred'
        }), 500

# Test function to verify AssemblyAI connection
def test_assemblyai_connection():
    """
    Test AssemblyAI API connection
    """
    try:
        api_key = os.getenv('ASSEMBLYAI_API_KEY')
        if not api_key:
            return False, "API key not found"
        
        aai.settings.api_key = api_key
        
        # Try to create a transcriber (this validates the API key)
        transcriber = aai.Transcriber()
        
        return True, "Connection successful"
    
    except Exception as e:
        return False, f"Connection failed: {str(e)}"

if __name__ == "__main__":
    # Test the connection
    success, message = test_assemblyai_connection()
    print(f"AssemblyAI Connection Test: {message}")
