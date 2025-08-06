import os
import time
import tempfile
import assemblyai as aai
from flask import request, jsonify
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_voice_explanation_fixed():
    """
    Fixed voice explanation endpoint with proper AssemblyAI integration
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
        logger.info(f"Received audio file: {audio_file.filename}, Content-Type: {audio_file.content_type}")
        
        # Create secure temp file with proper extension
        file_extension = '.webm' if 'webm' in str(audio_file.content_type) else '.wav'
        temp_fd, temp_path = tempfile.mkstemp(suffix=file_extension, prefix='audio_')
        
        try:
            # Save audio file
            with os.fdopen(temp_fd, 'wb') as temp_file:
                audio_data = audio_file.read()
                if len(audio_data) == 0:
                    raise ValueError("Audio file contains no data")
                
                temp_file.write(audio_data)
                logger.info(f"Saved audio file: {len(audio_data)} bytes to {temp_path}")
            
            # Get AssemblyAI API key
            api_key = os.getenv('ASSEMBLYAI_API_KEY')
            if not api_key:
                logger.error("AssemblyAI API key not found")
                return jsonify({
                    'success': False,
                    'error': 'Transcription service not configured'
                }), 500
            
            # Configure AssemblyAI
            aai.settings.api_key = api_key
            
            # Enhanced transcription config for better accuracy
            config = aai.TranscriptionConfig(
                speech_model=aai.SpeechModel.best,
                language_code="en",
                punctuate=True,
                format_text=True,
                filter_profanity=False,
                boost_param="algorithm data structure coding programming interview",
                word_boost=[
                    "algorithm", "complexity", "runtime", "space", "time", 
                    "array", "string", "tree", "graph", "hash", "sort", "search",
                    "dynamic programming", "greedy", "divide conquer", "recursion"
                ]
            )
            
            # Create transcriber
            transcriber = aai.Transcriber(config=config)
            
            logger.info("Starting AssemblyAI transcription...")
            transcript = transcriber.transcribe(temp_path)
            
            # Wait for completion with timeout
            max_wait = 60  # 60 seconds max
            start_time = time.time()
            
            while transcript.status not in [aai.TranscriptStatus.completed, aai.TranscriptStatus.error]:
                if time.time() - start_time > max_wait:
                    logger.error("Transcription timeout")
                    return jsonify({
                        'success': False,
                        'error': 'Transcription timeout - please try a shorter recording'
                    }), 408
                
                logger.info(f"Transcription status: {transcript.status}")
                time.sleep(2)
                # Refresh transcript status
                transcript = transcriber.get_transcript(transcript.id)
            
            # Handle results
            if transcript.status == aai.TranscriptStatus.error:
                logger.error(f"Transcription failed: {transcript.error}")
                return jsonify({
                    'success': False,
                    'error': f'Transcription failed: {transcript.error}'
                }), 422
            
            if transcript.status == aai.TranscriptStatus.completed:
                if transcript.text and transcript.text.strip():
                    transcription_text = transcript.text.strip()
                    logger.info(f"Transcription successful: {len(transcription_text)} characters")
                    
                    return jsonify({
                        'success': True,
                        'transcription': transcription_text
                    })
                else:
                    logger.warning("Transcription completed but no text found")
                    return jsonify({
                        'success': False,
                        'error': 'No speech detected in the audio. Please speak clearly and try again.'
                    }), 422
            
            logger.error(f"Unexpected transcription status: {transcript.status}")
            return jsonify({
                'success': False,
                'error': 'Transcription failed with unexpected status'
            }), 500
                
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

# Test function
def test_assemblyai_direct():
    """
    Test AssemblyAI with a sample audio file
    """
    try:
        api_key = os.getenv('ASSEMBLYAI_API_KEY')
        if not api_key:
            return False, "API key not found"
        
        aai.settings.api_key = api_key
        
        # Test with AssemblyAI's sample audio
        audio_url = "https://storage.googleapis.com/aai-docs-samples/nbc.wav"
        
        config = aai.TranscriptionConfig(
            speech_model=aai.SpeechModel.best,
            language_code="en"
        )
        
        transcriber = aai.Transcriber(config=config)
        transcript = transcriber.transcribe(audio_url)
        
        if transcript.status == aai.TranscriptStatus.completed:
            return True, f"Success: {transcript.text[:100]}..."
        elif transcript.status == aai.TranscriptStatus.error:
            return False, f"Error: {transcript.error}"
        else:
            return False, f"Unexpected status: {transcript.status}"
            
    except Exception as e:
        return False, f"Exception: {str(e)}"
