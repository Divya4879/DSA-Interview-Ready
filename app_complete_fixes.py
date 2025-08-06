# Complete fixes to add to app.py

# 1. Add analysis endpoint
@app.route('/analysis')
def analysis_page():
    """Analysis page to show user's progress and insights"""
    user_id = session.get('user_id', 'anonymous')
    
    # Get user stats
    from stats_fix import calculate_user_stats
    stats = calculate_user_stats(redis_client, user_id)
    
    # Get recent submissions
    submission_keys = redis_client.keys(f"submission:{user_id}:*")
    recent_submissions = []
    
    for key in sorted(submission_keys, reverse=True)[:10]:  # Last 10 submissions
        submission_data = redis_client.hgetall(key)
        if submission_data:
            try:
                scores = json.loads(submission_data.get('scores', '{}'))
                recent_submissions.append({
                    'problem_id': submission_data.get('problem_id', 'Unknown'),
                    'timestamp': int(submission_data.get('timestamp', 0)),
                    'scores': scores
                })
            except:
                continue
    
    return render_template('analysis.html', 
                         stats=stats, 
                         recent_submissions=recent_submissions)

# 2. Fix user stats endpoint
@app.route('/api/user-stats', methods=['GET', 'POST'])
def user_stats():
    if request.method == 'POST':
        data = request.json
        user_id = data.get('user_id', session.get('user_id', 'anonymous'))
    else:
        user_id = session.get('user_id', 'anonymous')
    
    from stats_fix import calculate_user_stats
    stats = calculate_user_stats(redis_client, user_id)
    return jsonify(stats)

# 3. Fix submit solution with proper stats tracking
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
        
        # Extract scores
        scores = {
            'code_quality': analysis['code_quality'],
            'algorithm_efficiency': analysis['algorithm_efficiency'],
            'communication_skills': analysis['communication_skills'],
            'problem_solving': analysis['problem_solving'],
            'interview_readiness': analysis['interview_readiness']
        }
        
        # Update user submission with proper tracking
        from stats_fix import update_user_submission
        update_user_submission(redis_client, user_id, problem_id, scores)
        
        # Format the feedback properly
        from analysis_formatter import format_analysis_text
        formatted_feedback = format_analysis_text(analysis)
        
        # Return formatted analysis
        return jsonify({
            'success': True,
            'analysis': {
                'code_quality': scores['code_quality'],
                'algorithm_efficiency': scores['algorithm_efficiency'],
                'communication_skills': scores['communication_skills'],
                'problem_solving': scores['problem_solving'],
                'interview_readiness': scores['interview_readiness'],
                'feedback': formatted_feedback,
                'recommendation': analysis.get('recommendation', 'Continue practicing!')
            }
        })
        
    except Exception as e:
        print(f"Submission error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Analysis failed'
        }), 500

# 4. Add endpoint to get previously solved problems
@app.route('/api/solved-problems')
def get_solved_problems():
    user_id = session.get('user_id', 'anonymous')
    
    # Get solved problem IDs
    user_problems_key = f"user:{user_id}:solved_problems"
    solved_problem_ids = redis_client.smembers(user_problems_key)
    
    # Get problem details
    solved_problems = []
    for problem_id in solved_problem_ids:
        problem_key = f"problem:{problem_id}"
        problem_data = redis_client.hgetall(problem_key)
        
        if problem_data:
            solved_problems.append({
                'id': problem_id,
                'title': problem_data.get('title', 'Unknown Problem'),
                'difficulty': problem_data.get('difficulty', 'Medium'),
                'category': problem_data.get('category', 'General'),
                'solved': True
            })
    
    return jsonify(solved_problems)

# 5. Dashboard stats fix
@app.route('/')
def dashboard():
    user_id = session.get('user_id', str(uuid.uuid4()))
    session['user_id'] = user_id
    
    # Get accurate user stats
    from stats_fix import calculate_user_stats
    stats = calculate_user_stats(redis_client, user_id)
    
    # Get recent problems
    recent_problems = []
    try:
        all_problems = redis_client.smembers('all_problems')
        for problem_id in list(all_problems)[:6]:  # Show 6 recent problems
            problem_data = redis_client.hgetall(f'problem:{problem_id}')
            if problem_data:
                recent_problems.append({
                    'id': problem_id,
                    'title': problem_data.get('title', 'Problem'),
                    'difficulty': problem_data.get('difficulty', 'Medium'),
                    'category': problem_data.get('category', 'General')
                })
    except:
        pass
    
    return render_template('dashboard.html', 
                         stats=stats, 
                         recent_problems=recent_problems)
