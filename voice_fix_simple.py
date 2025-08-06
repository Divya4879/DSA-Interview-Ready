import os
import time
import tempfile
import assemblyai as aai
from flask import request, jsonify
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_voice_explanation_simple():
    """
    Simple, working voice explanation endpoint
    """
    try:
        logger.info("Processing voice explanation request")
        
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
        logger.info(f"Received audio file: {audio_file.filename}")
        
        # Create temp file
        temp_fd, temp_path = tempfile.mkstemp(suffix='.webm', prefix='audio_')
        
        try:
            # Save audio file
            with os.fdopen(temp_fd, 'wb') as temp_file:
                audio_data = audio_file.read()
                if len(audio_data) == 0:
                    raise ValueError("Audio file contains no data")
                
                temp_file.write(audio_data)
                logger.info(f"Saved audio file: {len(audio_data)} bytes")
            
            # Get and set API key
            api_key = os.getenv('ASSEMBLYAI_API_KEY')
            if not api_key:
                logger.error("AssemblyAI API key not found")
                return jsonify({
                    'success': False,
                    'error': 'Transcription service not configured'
                }), 500
            
            aai.settings.api_key = api_key
            logger.info("API key configured")
            
            # Simple transcription
            transcriber = aai.Transcriber()
            logger.info("Starting transcription...")
            
            transcript = transcriber.transcribe(temp_path)
            logger.info(f"Initial status: {transcript.status}")
            
            # Wait for completion
            max_wait = 60
            start_time = time.time()
            
            while transcript.status == aai.TranscriptStatus.queued or transcript.status == aai.TranscriptStatus.processing:
                if time.time() - start_time > max_wait:
                    logger.error("Transcription timeout")
                    return jsonify({
                        'success': False,
                        'error': 'Transcription timeout - please try again with a shorter recording'
                    }), 408
                
                logger.info(f"Status: {transcript.status}, waiting...")
                time.sleep(3)
                transcript = transcriber.get_transcript(transcript.id)
            
            # Check final status
            logger.info(f"Final status: {transcript.status}")
            
            if transcript.status == aai.TranscriptStatus.error:
                logger.error(f"Transcription error: {transcript.error}")
                return jsonify({
                    'success': False,
                    'error': f'Transcription failed: {transcript.error}'
                }), 422
            
            if transcript.status == aai.TranscriptStatus.completed:
                if transcript.text and transcript.text.strip():
                    transcription_text = transcript.text.strip()
                    logger.info(f"Transcription successful: '{transcription_text[:50]}...'")
                    
                    return jsonify({
                        'success': True,
                        'transcription': transcription_text
                    })
                else:
                    logger.warning("No text in completed transcription")
                    return jsonify({
                        'success': False,
                        'error': 'No speech detected. Please speak clearly and try again.'
                    }), 422
            
            # Unexpected status
            logger.error(f"Unexpected status: {transcript.status}")
            return jsonify({
                'success': False,
                'error': f'Unexpected transcription status: {transcript.status}'
            }), 500
                
        finally:
            # Cleanup
            try:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    logger.info("Temp file cleaned up")
            except Exception as e:
                logger.warning(f"Cleanup failed: {e}")
        
    except Exception as e:
        logger.error(f"Voice processing error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Processing failed: {str(e)}'
        }), 500

def test_simple_transcription():
    """
    Test basic AssemblyAI functionality
    """
    try:
        # Load environment
        load_dotenv()
        api_key = os.getenv('ASSEMBLYAI_API_KEY')
        
        if not api_key:
            return False, "API key not found"
        
        # Set API key
        aai.settings.api_key = api_key
        
        # Test with sample URL
        audio_url = "https://storage.googleapis.com/aai-docs-samples/nbc.wav"
        
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_url)
        
        # Wait for completion
        while transcript.status in [aai.TranscriptStatus.queued, aai.TranscriptStatus.processing]:
            time.sleep(2)
            transcript = transcriber.get_transcript(transcript.id)
        
        if transcript.status == aai.TranscriptStatus.completed:
            return True, f"Success: {transcript.text[:100]}..."
        elif transcript.status == aai.TranscriptStatus.error:
            return False, f"Error: {transcript.error}"
        else:
            return False, f"Status: {transcript.status}"
            
    except Exception as e:
        return False, f"Exception: {str(e)}"

if __name__ == "__main__":
    success, message = test_simple_transcription()
    print(f"Test result: {'✅ PASS' if success else '❌ FAIL'} - {message}")
