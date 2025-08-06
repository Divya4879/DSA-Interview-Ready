# Fixes to apply to app.py

# 1. Fix voice explanation endpoint - remove placeholder text
@app.route('/api/voice-explanation', methods=['POST'])
def process_voice_explanation():
    """
    Clean voice explanation endpoint - no placeholder text
    """
    try:
        print("Processing voice explanation request")
        
        if 'audio' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No audio file provided'
            }), 400
        
        audio_file = request.files['audio']
        if not audio_file or audio_file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No audio file selected'
            }), 400
        
        print(f"Received audio file: {audio_file.filename}")
        
        import tempfile
        file_extension = '.webm' if 'webm' in str(audio_file.content_type) else '.wav'
        temp_fd, temp_path = tempfile.mkstemp(suffix=file_extension, prefix='audio_')
        
        try:
            with os.fdopen(temp_fd, 'wb') as temp_file:
                audio_data = audio_file.read()
                if len(audio_data) == 0:
                    # Return failure - no placeholder text
                    return jsonify({
                        'success': False,
                        'error': 'Empty audio file'
                    }), 400
                
                temp_file.write(audio_data)
                print(f"Saved audio file: {len(audio_data)} bytes")
            
            import assemblyai as aai
            api_key = os.getenv('ASSEMBLYAI_API_KEY')
            if not api_key:
                return jsonify({
                    'success': False,
                    'error': 'Transcription service not available'
                }), 503
            
            aai.settings.api_key = api_key
            transcriber = aai.Transcriber()
            print("Starting transcription...")
            
            transcript = transcriber.transcribe(temp_path)
            
            # Wait for completion
            max_wait = 45
            start_time = time.time()
            
            while transcript.status in [aai.TranscriptStatus.queued, aai.TranscriptStatus.processing]:
                if time.time() - start_time > max_wait:
                    return jsonify({
                        'success': False,
                        'error': 'Transcription timeout'
                    }), 408
                
                time.sleep(2)
                transcript = transcriber.get_transcript(transcript.id)
            
            print(f"Final status: {transcript.status}")
            
            if transcript.status == aai.TranscriptStatus.error:
                return jsonify({
                    'success': False,
                    'error': 'Transcription failed'
                }), 422
            
            if transcript.status == aai.TranscriptStatus.completed:
                if transcript.text and transcript.text.strip():
                    # Return actual transcription - no placeholder
                    return jsonify({
                        'success': True,
                        'transcription': transcript.text.strip()
                    })
                else:
                    # No speech detected - return failure, no placeholder
                    return jsonify({
                        'success': False,
                        'error': 'No speech detected'
                    }), 422
            
            return jsonify({
                'success': False,
                'error': 'Transcription failed'
            }), 500
                
        finally:
            try:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
            except:
                pass
        
    except Exception as e:
        print(f"Voice processing error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Processing failed'
        }), 500

# 2. Fix submit solution to use proper analysis
@app.route('/api/submit-solution', methods=['POST'])
def submit_solution():
    data = request.json
    user_id = session.get('user_id', str(uuid.uuid4()))
    session['user_id'] = user_id
    
    problem_id = data.get('problem_id')
    code = data.get('code')
    explanation = data.get('explanation')
    language = data.get('language', 'python')
    
    if not code or not explanation:
        return jsonify({'success': False, 'error': 'Code and explanation required'}), 400
    
    try:
        # Use proper technical analysis
        from ai_analysis_fixed import ProperTechnicalAnalysis
        analyzer = ProperTechnicalAnalysis()
        
        analysis = analyzer.analyze_solution(problem_id, code, explanation, language)
        
        # Store submission (count unique problems only)
        submission_key = f"submission:{user_id}:{int(time.time())}"
        redis_client.hset(submission_key, mapping={
            'problem_id': problem_id,
            'code': code,
            'explanation': explanation,
            'language': language,
            'timestamp': int(time.time()),
            'scores': json.dumps({
                'code_quality': analysis['code_quality'],
                'algorithm_efficiency': analysis['algorithm_efficiency'],
                'communication_skills': analysis['communication_skills'],
                'problem_solving': analysis['problem_solving'],
                'interview_readiness': analysis['interview_readiness']
            })
        })
        
        # Update user stats (unique problems only)
        user_problems_key = f"user:{user_id}:solved_problems"
        if not redis_client.sismember(user_problems_key, problem_id):
            redis_client.sadd(user_problems_key, problem_id)
            redis_client.hincrby(f"user:{user_id}:stats", "problems_solved", 1)
        
        # Always increment total submissions
        redis_client.hincrby(f"user:{user_id}:stats", "total_submissions", 1)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        print(f"Submission error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Analysis failed'
        }), 500

# 3. Remove Redis branding from templates (except footer)
# This would need to be applied to HTML templates to remove Redis mentions
# and replace with generic "AI Analysis" or "Technical Analysis"
