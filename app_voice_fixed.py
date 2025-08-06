# Fixed voice explanation endpoint to replace in app.py

import os
import time
import tempfile
import assemblyai as aai
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/voice-explanation', methods=['POST'])
def process_voice_explanation():
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
        logger.info(f"Received audio file: {audio_file.filename}")
        
        # Create temp file with proper extension
        file_extension = '.webm' if 'webm' in str(audio_file.content_type) else '.wav'
        temp_fd, temp_path = tempfile.mkstemp(suffix=file_extension, prefix='audio_')
        
        try:
            # Save audio file
            with os.fdopen(temp_fd, 'wb') as temp_file:
                audio_data = audio_file.read()
                if len(audio_data) == 0:
                    raise ValueError("Audio file contains no data")
                
                temp_file.write(audio_data)
                logger.info(f"Saved audio file: {len(audio_data)} bytes")
            
            # Get and configure AssemblyAI
            api_key = os.getenv('ASSEMBLYAI_API_KEY')
            if not api_key:
                logger.error("AssemblyAI API key not found")
                return jsonify({
                    'success': False,
                    'error': 'Transcription service not configured'
                }), 500
            
            aai.settings.api_key = api_key
            
            # Create transcriber and start transcription
            transcriber = aai.Transcriber()
            logger.info("Starting AssemblyAI transcription...")
            
            transcript = transcriber.transcribe(temp_path)
            logger.info(f"Transcription submitted, ID: {transcript.id}")
            
            # Wait for completion with timeout
            max_wait = 60  # 60 seconds
            start_time = time.time()
            
            while transcript.status in [aai.TranscriptStatus.queued, aai.TranscriptStatus.processing]:
                if time.time() - start_time > max_wait:
                    logger.error("Transcription timeout")
                    return jsonify({
                        'success': False,
                        'error': 'Transcription timeout - please try a shorter recording'
                    }), 408
                
                logger.info(f"Status: {transcript.status}, waiting...")
                time.sleep(3)
                transcript = transcriber.get_transcript(transcript.id)
            
            # Handle final status
            logger.info(f"Final transcription status: {transcript.status}")
            
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
                        'error': 'No speech detected in the audio. Please speak more clearly and try again.'
                    }), 422
            
            # Unexpected status
            logger.error(f"Unexpected transcription status: {transcript.status}")
            return jsonify({
                'success': False,
                'error': f'Unexpected transcription status: {transcript.status}'
            }), 500
                
        finally:
            # Clean up temp file
            try:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    logger.info("Temp file cleaned up")
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
