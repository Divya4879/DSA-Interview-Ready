from flask import Flask, render_template, request, jsonify, session
import redis
import json
import os
from datetime import datetime
import hashlib
import uuid
import time
from dotenv import load_dotenv
# from redis_ai_fixed import get_redis_ai
from ai_service import AIService

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Redis Cloud setup
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    password=os.getenv('REDIS_PASSWORD', ''),
    username=os.getenv('REDIS_USERNAME', 'default'),
    ssl=False,  # Disable SSL for now
    decode_responses=True
)

# Initialize Redis AI features
redis_ai = get_redis_ai()

# Initialize AI Service
ai_service = AIService()

@app.route('/')
def dashboard():
    user_id = session.get('user_id', 'anonymous')
    stats = get_user_stats(user_id)
    return render_template('dashboard.html', stats=stats)

@app.route('/practice')
def practice():
    difficulty = request.args.get('difficulty', 'medium')
    language = request.args.get('language', 'python')
    topic = request.args.get('topic', 'arrays')
    problem_id = request.args.get('problem_id')  # Direct problem selection
    
    if problem_id:
        # Get specific problem by ID
        problem_data = redis_client.hgetall(f'problem:{problem_id}')
        if problem_data:
            parsed_problem = parse_problem_data(problem_data, language)
            return render_template('practice.html', 
                                 problem=parsed_problem, 
                                 difficulty=parsed_problem.get('difficulty', difficulty), 
                                 language=language, 
                                 topic=parsed_problem.get('topic', topic))
    
    # Get problem by topic and difficulty (deterministic)
    problem = get_problem_by_criteria(difficulty, language, topic)
    return render_template('practice.html', problem=problem, difficulty=difficulty, language=language, topic=topic)

def parse_problem_data(problem_data, language):
    """Parse problem data from Redis"""
    parsed_problem = {}
    for key, value in problem_data.items():
        if key in ['examples', 'constraints', 'hints', 'tags']:
            try:
                parsed_problem[key] = json.loads(value)
            except:
                parsed_problem[key] = []
        else:
            parsed_problem[key] = value
    
    # Add language-specific solution template
    templates = {
        'python': f'def solve():\n    # Your Python solution for {parsed_problem.get("title", "problem")}\n    pass',
        'javascript': f'function solve() {{\n    // Your JavaScript solution for {parsed_problem.get("title", "problem")}\n}}',
        'java': f'public class Solution {{\n    public void solve() {{\n        // Your Java solution for {parsed_problem.get("title", "problem")}\n    }}\n}}',
        'cpp': f'class Solution {{\npublic:\n    void solve() {{\n        // Your C++ solution for {parsed_problem.get("title", "problem")}\n    }}\n}};'
    }
    parsed_problem['solution_template'] = templates.get(language, templates['python'])
    return parsed_problem

def get_problem_by_tag(tag, difficulty, language):
    """Get a random problem by tag"""
    import random
    
    try:
        print(f"🏷️ Getting problem by tag: {tag}, difficulty: {difficulty}")
        
        # Get problems with this tag
        tag_key = f'problems_by_tag:{tag.lower().replace(" ", "_")}'
        problem_ids = redis_client.smembers(tag_key)
        
        if not problem_ids:
            print(f"⚠️ No problems found for tag: {tag}")
            return None
        
        # Filter by difficulty if possible
        filtered_problems = []
        for problem_id in problem_ids:
            problem_data = redis_client.hgetall(f'problem:{problem_id}')
            if problem_data and problem_data.get('difficulty') == difficulty:
                filtered_problems.append(problem_id)
        
        # If no problems match the difficulty, use any problem with the tag
        if not filtered_problems:
            filtered_problems = list(problem_ids)
        
        if filtered_problems:
            # Randomly select a problem
            problem_id = random.choice(filtered_problems)
            print(f"🎲 Selected random problem by tag: {problem_id}")
            
            problem_data = redis_client.hgetall(f'problem:{problem_id}')
            if problem_data:
                parsed_problem = parse_problem_data(problem_data, language)
                print(f"✅ Returning tagged problem: {parsed_problem.get('title', 'Unknown')}")
                return parsed_problem
        
        return None
    except Exception as e:
        print(f"Error getting problem by tag: {e}")
        return None

@app.route('/api/voice-explanation', methods=['POST'])
def process_voice_explanation():
    """
    Fixed voice explanation endpoint with proper AssemblyAI integration
    """
    try:
        print("Processing voice explanation request")
        
        # Validate request
        if 'audio' not in request.files:
            print("No audio file in request")
            return jsonify({
                'success': False,
                'error': 'No audio file provided'
            }), 400
        
        audio_file = request.files['audio']
        if not audio_file or audio_file.filename == '':
            print("Empty audio file")
            return jsonify({
                'success': False,
                'error': 'No audio file selected'
            }), 400
        
        # Log file info
        print(f"Received audio file: {audio_file.filename}")
        
        # Create temp file with proper extension
        import tempfile
        file_extension = '.webm' if 'webm' in str(audio_file.content_type) else '.wav'
        temp_fd, temp_path = tempfile.mkstemp(suffix=file_extension, prefix='audio_')
        
        try:
            # Save audio file
            with os.fdopen(temp_fd, 'wb') as temp_file:
                audio_data = audio_file.read()
                if len(audio_data) == 0:
                    raise ValueError("Audio file contains no data")
                
                temp_file.write(audio_data)
                print(f"Saved audio file: {len(audio_data)} bytes")
            
            # Get and configure AssemblyAI
            import assemblyai as aai
            api_key = os.getenv('ASSEMBLYAI_API_KEY')
            if not api_key:
                print("AssemblyAI API key not found")
                return jsonify({
                    'success': False,
                    'error': 'Transcription service not configured'
                }), 500
            
            aai.settings.api_key = api_key
            
            # Create transcriber and start transcription
            transcriber = aai.Transcriber()
            print("Starting AssemblyAI transcription...")
            
            transcript = transcriber.transcribe(temp_path)
            print(f"Transcription submitted, ID: {transcript.id}")
            
            # Wait for completion with timeout
            max_wait = 60  # 60 seconds
            start_time = time.time()
            
            while transcript.status in [aai.TranscriptStatus.queued, aai.TranscriptStatus.processing]:
                if time.time() - start_time > max_wait:
                    print("Transcription timeout")
                    return jsonify({
                        'success': False,
                        'error': 'Transcription timeout - please try a shorter recording'
                    }), 408
                
                print(f"Status: {transcript.status}, waiting...")
                time.sleep(3)
                transcript = transcriber.get_transcript(transcript.id)
            
            # Handle final status
            print(f"Final transcription status: {transcript.status}")
            
            if transcript.status == aai.TranscriptStatus.error:
                print(f"Transcription failed: {transcript.error}")
                return jsonify({
                    'success': False,
                    'error': f'Transcription failed: {transcript.error}'
                }), 422
            
            if transcript.status == aai.TranscriptStatus.completed:
                if transcript.text and transcript.text.strip():
                    transcription_text = transcript.text.strip()
                    print(f"Transcription successful: {len(transcription_text)} characters")
                    
                    return jsonify({
                        'success': True,
                        'transcription': transcription_text
                    })
                else:
                    print("Transcription completed but no text found")
                    return jsonify({
                        'success': False,
                        'error': 'No speech detected in the audio. Please speak more clearly and try again.'
                    }), 422
            
            # Unexpected status
            print(f"Unexpected transcription status: {transcript.status}")
            return jsonify({
                'success': False,
                'error': f'Unexpected transcription status: {transcript.status}'
            }), 500
                
        finally:
            # Clean up temp file
            try:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    print("Temp file cleaned up")
            except Exception as cleanup_error:
                print(f"Failed to cleanup temp file: {cleanup_error}")
        
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return jsonify({
            'success': False,
            'error': str(ve)
        }), 400
    
    except Exception as e:
        print(f"Unexpected error in voice explanation: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error occurred'
        }), 500

@app.route('/api/submit-solution', methods=['POST'])
def submit_solution():
    data = request.json
    user_id = session.get('user_id', str(uuid.uuid4()))
    session['user_id'] = user_id
    
    problem_id = data.get('problem_id')
    code = data.get('code')
    explanation = data.get('explanation')
    language = data.get('language', 'python')
    
    print(f"🔍 DEBUG: Received submission for {problem_id}")
    print(f"🔍 DEBUG: Code length: {len(code) if code else 0}")
    print(f"🔍 DEBUG: Explanation: {explanation[:50] if explanation else 'None'}...")
    
    if not code or not explanation:
        return jsonify({'success': False, 'error': 'Code and explanation required'}), 400
    
    try:
        print("🔍 DEBUG: Using SeniorRecruiterAnalysis")
        # Use comprehensive senior recruiter analysis
        from senior_recruiter_analysis import SeniorRecruiterAnalysis
        analyzer = SeniorRecruiterAnalysis()
        
        analysis = analyzer.analyze_solution(problem_id, code, explanation, language)
        print(f"🔍 DEBUG: Analysis scores - Code: {analysis['code_quality']}, Algo: {analysis['algorithm_efficiency']}")
        
        # Extract scores
        scores = {
            'code_quality': analysis['code_quality'],
            'algorithm_efficiency': analysis['algorithm_efficiency'],
            'communication_skills': analysis['communication_skills'],
            'problem_solving': analysis['problem_solving'],
            'interview_readiness': analysis['interview_readiness']
        }
        
        # Store submission with proper tracking
        submission_key = f"submission:{user_id}:{int(time.time())}"
        redis_client.hset(submission_key, mapping={
            'problem_id': problem_id,
            'code': code,
            'explanation': explanation,
            'language': language,
            'timestamp': int(time.time()),
            'scores': json.dumps(scores)
        })
        
        # Add to unique problems set
        user_problems_key = f"user:{user_id}:solved_problems"
        redis_client.sadd(user_problems_key, problem_id)
        
        print("🔍 DEBUG: Returning comprehensive senior recruiter analysis")
        # Return formatted analysis
        return jsonify({
            'success': True,
            'analysis': {
                'code_quality': scores['code_quality'],
                'algorithm_efficiency': scores['algorithm_efficiency'],
                'communication_skills': scores['communication_skills'],
                'problem_solving': scores['problem_solving'],
                'interview_readiness': scores['interview_readiness'],
                'feedback': analysis['feedback'],  # Already formatted HTML
                'recommendation': analysis.get('recommendation', 'Continue practicing!')
            }
        })
        
    except Exception as e:
        print(f"❌ DEBUG: Submission error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': 'Analysis failed'
        }), 500

@app.route('/api/user-stats', methods=['GET', 'POST'])
def user_stats():
    if request.method == 'POST':
        data = request.json
        user_id = data.get('user_id', 'anonymous')
    else:
        user_id = session.get('user_id', 'anonymous')
    
    stats = get_user_stats(user_id)
    return jsonify(stats)

@app.route('/api/platform-data')
def get_platform_data():
    try:
        # Count problems safely
        problem_keys = list(redis_client.scan_iter(match='problem:*'))
        total_problems = len(problem_keys)
        
        # Get topics and difficulties from sets
        topics = list(redis_client.smembers('topics'))
        difficulties = list(redis_client.smembers('difficulties'))
        
        # Get platform stats safely
        try:
            stats = redis_client.hgetall('platform_stats')
            if not stats:
                stats = {
                    'total_problems': total_problems,
                    'total_users': 0,
                    'total_submissions': 0
                }
        except:
            stats = {
                'total_problems': total_problems,
                'total_users': 0,
                'total_submissions': 0
            }
        
        return jsonify({
            'topics': sorted(topics) if topics else ['arrays', 'strings', 'linked-lists', 'trees', 'graphs', 'dynamic-programming', 'stacks', 'heaps'],
            'difficulties': sorted(difficulties, key=lambda x: {'easy': 1, 'medium': 2, 'hard': 3}.get(x, 4)) if difficulties else ['easy', 'medium', 'hard'],
            'stats': {
                'total_problems': total_problems,
                'total_topics': len(topics) if topics else 8,
                'total_users': stats.get('total_users', 0),
                'total_submissions': stats.get('total_submissions', 0)
            }
        })
    except Exception as e:
        print(f"Platform data error: {e}")
        return jsonify({
            'topics': ['arrays', 'strings', 'linked-lists', 'trees', 'graphs', 'dynamic-programming', 'stacks', 'heaps'],
            'difficulties': ['easy', 'medium', 'hard'],
            'stats': {
                'total_problems': 80,
                'total_topics': 8,
                'total_users': 0,
                'total_submissions': 0
            }
        })

@app.route('/api/solved-problems')
def get_solved_problems():
    """Get previously solved problems for the user"""
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

@app.route('/api/problems')
def get_problems():
    difficulty = request.args.get('difficulty', 'all')
    topic = request.args.get('topic', 'all')
    language = request.args.get('language', 'python')
    
    problems = fetch_problems_from_redis(difficulty, topic, language)
    return jsonify(problems)

@app.route('/api/recommendations')
def get_recommendations():
    user_id = session.get('user_id', 'anonymous')
    recommendations = redis_ai.get_problem_recommendations(user_id)
    return jsonify(recommendations)

@app.route('/api/trending')
def get_trending():
    trending = redis_ai.get_trending_problems()
    return jsonify(trending)

# Removed similar problems API - replaced with direct navigation links

@app.route('/api/analytics/realtime')
def get_realtime_analytics():
    try:
        now = int(time.time() * 1000)
        hour_ago = now - (60 * 60 * 1000)
        
        analytics = {
            "user_activity": len(redis_client.execute_command("TS.RANGE", "user_activity", hour_ago, now) or []),
            "ai_searches": len(redis_client.execute_command("TS.RANGE", "similarity_searches", hour_ago, now) or []),
            "vector_index_size": len(list(redis_client.scan_iter(match="vector:*"))),
            "problems_indexed": len(list(redis_client.scan_iter(match="problem:*"))),
            "redis_modules": ["JSON", "Search", "TimeSeries", "VectorSet", "Bloom"]
        }
        return jsonify(analytics)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/recruiter-assessment')
def get_recruiter_assessment():
    """Get real recruiter assessment based on actual user submissions"""
    user_id = session.get('user_id', 'anonymous')
    
    try:
        # Get actual submission data
        submission_keys = redis_client.keys(f"submission:{user_id}:*")
        
        if not submission_keys:
            return jsonify({
                'has_submissions': False,
                'message': 'No submissions found. Complete coding problems to receive assessment.'
            })
        
        # Analyze real submissions
        total_scores = {
            'code_quality': 0,
            'algorithm_efficiency': 0,
            'communication_skills': 0,
            'problem_solving': 0,
            'interview_readiness': 0
        }
        
        submission_count = 0
        problem_types = {}
        
        for key in submission_keys:
            submission_data = redis_client.hgetall(key)
            if submission_data and 'scores' in submission_data:
                try:
                    scores = json.loads(submission_data['scores'])
                    for metric, value in scores.items():
                        if metric in total_scores:
                            total_scores[metric] += value
                    submission_count += 1
                    
                    # Track problem types
                    problem_id = submission_data.get('problem_id', 'unknown')
                    problem_types[problem_id] = problem_types.get(problem_id, 0) + 1
                    
                except (json.JSONDecodeError, KeyError):
                    continue
        
        if submission_count == 0:
            return jsonify({
                'has_submissions': False,
                'message': 'No valid submissions found.'
            })
        
        # Calculate averages
        avg_scores = {k: round(v / submission_count) for k, v in total_scores.items()}
        overall_avg = sum(avg_scores.values()) / len(avg_scores)
        
        # Generate real insights based on actual performance with better formatting
        key_insights = []
        
        if avg_scores['code_quality'] >= 70:
            key_insights.append("**Code Quality**: Demonstrates strong code organization and readability\n• Clean, well-structured solutions with proper naming conventions")
        elif avg_scores['code_quality'] < 50:
            key_insights.append("**Code Quality**: Structure and organization need significant improvement\n• Focus on readable code, proper indentation, and meaningful variable names")
        else:
            key_insights.append("**Code Quality**: Shows room for improvement in structure and clarity\n• Work on consistent formatting and code organization")
            
        if avg_scores['algorithm_efficiency'] >= 70:
            key_insights.append("**Algorithm Efficiency**: Shows good understanding of algorithmic optimization\n• Demonstrates awareness of time and space complexity considerations")
        elif avg_scores['algorithm_efficiency'] < 50:
            key_insights.append("**Algorithm Efficiency**: Critical area requiring focused improvement\n• Study common algorithms and data structures for optimization")
        else:
            key_insights.append("**Algorithm Efficiency**: Skills are developing but need strengthening\n• Practice analyzing time/space complexity of solutions")
            
        if avg_scores['communication_skills'] >= 70:
            key_insights.append("**Communication Skills**: Technical communication skills are well-developed\n• Clear explanations of thought process and solution approach")
        elif avg_scores['communication_skills'] < 50:
            key_insights.append("**Communication Skills**: Technical explanation abilities need substantial work\n• Practice verbalizing problem-solving approach and solution reasoning")
        else:
            key_insights.append("**Communication Skills**: Show potential but require more practice\n• Work on clearly explaining technical concepts and decision-making")
        
        # Add submission-specific insights with better formatting
        key_insights.append(f"**Assessment Basis**: Analysis of **{submission_count}** actual coding submissions\n• Evaluated **{len(problem_types)}** unique problem types for comprehensive assessment")
        
        # Determine hiring decision based on real performance
        if overall_avg >= 80:
            hiring_decision = "Strong Hire"
            interview_readiness = "Senior Level"
        elif overall_avg >= 65:
            hiring_decision = "Hire"
            interview_readiness = "Mid Level"
        elif overall_avg >= 50:
            hiring_decision = "Lean Hire"
            interview_readiness = "Junior Level"
        else:
            hiring_decision = "No Hire"
            interview_readiness = "Entry Level"
        
        # Generate specific recommendation based on weakest areas with better formatting
        weak_areas = [k.replace('_', ' ').title() for k, v in avg_scores.items() if v < 60]
        if weak_areas:
            recommendation = f"**Priority Areas for Improvement**: {', '.join(weak_areas)}\n\n"
            recommendation += f"**Interview Readiness**: Current performance suggests **{interview_readiness.lower()}** interview readiness.\n\n"
            recommendation += "**Next Steps**: Focus on targeted practice in identified weak areas to improve overall interview performance."
        else:
            recommendation = f"**Strong Performance**: Continue practicing to maintain excellent standards.\n\n"
            recommendation += f"**Interview Readiness**: Current performance suggests **{interview_readiness.lower()}** interview readiness.\n\n"
            recommendation += "**Next Steps**: Ready for technical interviews at your current level. Consider tackling more challenging problems to advance further."
        
        return jsonify({
            'has_submissions': True,
            'overall_rating': round(overall_avg / 10, 1),
            'hiring_decision': hiring_decision,
            'interview_readiness': interview_readiness,
            'key_insights': key_insights,
            'recommendation': recommendation,
            'submission_count': submission_count,
            'problems_attempted': len(problem_types),
            'performance_breakdown': avg_scores
        })
        
    except Exception as e:
        print(f"Error in recruiter assessment: {e}")
        return jsonify({
            'has_submissions': False,
            'error': 'Unable to generate assessment'
        }), 500

def get_user_stats(user_id):
    """Get accurate user statistics with averaged metrics from all submissions"""
    try:
        # Get unique problems solved
        user_problems_key = f"user:{user_id}:solved_problems"
        unique_problems = redis_client.scard(user_problems_key)
        
        # Get all submissions for this user
        submission_keys = redis_client.keys(f"submission:{user_id}:*")
        total_submissions = len(submission_keys)
        
        if total_submissions == 0:
            return {
                'problems_solved': 0,
                'total_submissions': 0,
                'average_score': 0,
                'streak': 0,
                'rank': 'Beginner',
                'code_quality': 0,
                'algorithm_efficiency': 0,
                'communication_skills': 0,
                'problem_solving': 0,
                'interview_readiness': 0,
                'strengths': [],
                'weaknesses': []
            }
        
        # Initialize metric totals for averaging
        metric_totals = {
            'code_quality': 0,
            'algorithm_efficiency': 0,
            'communication_skills': 0,
            'problem_solving': 0,
            'interview_readiness': 0
        }
        
        valid_submissions = 0
        submission_dates = []
        
        # Process all submissions to calculate averages
        for key in submission_keys:
            submission_data = redis_client.hgetall(key)
            if submission_data and 'scores' in submission_data:
                try:
                    score_data = json.loads(submission_data['scores'])
                    
                    # Add each metric to totals
                    for metric in metric_totals:
                        if metric in score_data:
                            metric_totals[metric] += score_data[metric]
                    
                    valid_submissions += 1
                    
                    # Track submission date for streak calculation
                    if 'timestamp' in submission_data:
                        submission_dates.append(int(submission_data['timestamp']))
                        
                except (json.JSONDecodeError, KeyError):
                    continue
        
        # Calculate averages for each metric
        if valid_submissions > 0:
            averaged_metrics = {
                metric: round(total / valid_submissions) 
                for metric, total in metric_totals.items()
            }
            
            # Calculate overall average score
            average_score = round(sum(averaged_metrics.values()) / len(averaged_metrics))
        else:
            averaged_metrics = {metric: 0 for metric in metric_totals}
            average_score = 0
        
        # Calculate streak (consecutive days with submissions)
        streak = calculate_streak(submission_dates)
        
        # Determine interview level based on average score and problems solved
        rank = determine_interview_level(average_score, unique_problems)
        
        # Calculate strengths and weaknesses based on averaged metrics
        strengths = []
        weaknesses = []
        
        for metric, score in averaged_metrics.items():
            metric_name = metric.replace('_', ' ').title()
            if score >= 75:
                strengths.append(metric_name)
            elif score < 50:
                weaknesses.append(metric_name)
        
        return {
            'problems_solved': unique_problems,
            'total_submissions': total_submissions,
            'average_score': average_score,
            'streak': streak,
            'rank': rank,
            'code_quality': averaged_metrics['code_quality'],
            'algorithm_efficiency': averaged_metrics['algorithm_efficiency'],
            'communication_skills': averaged_metrics['communication_skills'],
            'problem_solving': averaged_metrics['problem_solving'],
            'interview_readiness': averaged_metrics['interview_readiness'],
            'strengths': strengths,
            'weaknesses': weaknesses
        }
        
    except Exception as e:
        print(f"Error calculating stats: {e}")
        return {
            'problems_solved': 0,
            'total_submissions': 0,
            'average_score': 0,
            'streak': 0,
            'rank': 'Beginner',
            'code_quality': 0,
            'algorithm_efficiency': 0,
            'communication_skills': 0,
            'problem_solving': 0,
            'interview_readiness': 0,
            'strengths': [],
            'weaknesses': []
        }

def calculate_strengths_weaknesses(submission_keys):
    """Calculate real strengths and weaknesses based on submission data"""
    if not submission_keys:
        return [], []
    
    # Aggregate scores by category
    category_scores = {
        'code_quality': [],
        'algorithm_efficiency': [],
        'communication_skills': [],
        'problem_solving': [],
        'interview_readiness': []
    }
    
    for key in submission_keys:
        submission_data = redis_client.hgetall(key)
        if submission_data and 'scores' in submission_data:
            try:
                scores = json.loads(submission_data['scores'])
                for category, score in scores.items():
                    if category in category_scores:
                        category_scores[category].append(score)
            except (json.JSONDecodeError, KeyError):
                continue
    
    # Calculate averages
    category_averages = {}
    for category, scores in category_scores.items():
        if scores:
            category_averages[category] = sum(scores) / len(scores)
        else:
            category_averages[category] = 0
    
    # Determine strengths (>= 70) and weaknesses (< 50)
    strengths = []
    weaknesses = []
    
    category_names = {
        'code_quality': 'Code organization and structure',
        'algorithm_efficiency': 'Algorithm optimization and complexity analysis',
        'communication_skills': 'Technical explanation and communication',
        'problem_solving': 'Problem-solving methodology',
        'interview_readiness': 'Overall interview preparedness'
    }
    
    for category, avg_score in category_averages.items():
        category_name = category_names.get(category, category.replace('_', ' '))
        
        if avg_score >= 70:
            strengths.append(category_name)
        elif avg_score < 50:
            weaknesses.append(category_name)
    
    return strengths, weaknesses

def calculate_streak(submission_timestamps):
    """Calculate consecutive days streak"""
    if not submission_timestamps:
        return 0
    
    from datetime import datetime, timedelta
    
    # Convert timestamps to dates
    dates = []
    for timestamp in submission_timestamps:
        date = datetime.fromtimestamp(timestamp).date()
        dates.append(date)
    
    # Remove duplicates and sort
    unique_dates = sorted(set(dates), reverse=True)
    
    if not unique_dates:
        return 0
    
    # Check if today or yesterday has a submission
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    # Start streak calculation
    streak = 0
    current_date = today
    
    # If no submission today, start from yesterday
    if today not in unique_dates:
        if yesterday not in unique_dates:
            return 0
        current_date = yesterday
        streak = 1
    else:
        streak = 1
    
    # Count consecutive days backwards
    for i in range(1, len(unique_dates)):
        expected_date = current_date - timedelta(days=i)
        if expected_date in unique_dates:
            streak += 1
        else:
            break
    
    return streak

def determine_interview_level(average_score, problems_solved):
    """Determine interview readiness level"""
    if average_score >= 85 and problems_solved >= 50:
        return 'Expert'
    elif average_score >= 75 and problems_solved >= 25:
        return 'Advanced'
    elif average_score >= 65 and problems_solved >= 10:
        return 'Intermediate'
    elif average_score >= 50 and problems_solved >= 5:
        return 'Developing'
    else:
        return 'Beginner'

def update_user_progress(user_id, problem_id, score):
    current_stats = get_user_stats(user_id)
    
    new_stats = {
        'problems_solved': int(current_stats.get('problems_solved', 0)) + 1,
        'total_submissions': int(current_stats.get('total_submissions', 0)) + 1,
        'last_activity': datetime.now().isoformat(),
        'latest_score': score
    }
    
    redis_client.hset(f'user:{user_id}:stats', mapping=new_stats)
    # Track user progress for analysis instead of leaderboard
    redis_client.zadd(f'user:{user_id}:progress', {problem_id: score})

def get_problem_by_criteria(difficulty, language, topic):
    """Get the specific problem based on topic and difficulty - deterministic, not random"""
    
    print(f"🎯 Getting problem: difficulty={difficulty}, topic={topic}")
    
    try:
        # Get the specific problem for this topic and difficulty combination
        if difficulty != 'all' and topic != 'all':
            # Get intersection of difficulty and topic
            diff_problems = redis_client.smembers(f'problems_by_difficulty:{difficulty}')
            topic_problems = redis_client.smembers(f'problems_by_topic:{topic}')
            problem_ids = diff_problems.intersection(topic_problems)
        elif difficulty != 'all':
            # Get problems by difficulty only
            problem_ids = redis_client.smembers(f'problems_by_difficulty:{difficulty}')
        elif topic != 'all':
            # Get problems by topic only
            problem_ids = redis_client.smembers(f'problems_by_topic:{topic}')
        else:
            # Get all problems
            problem_ids = redis_client.smembers('all_problems')
        
        problem_ids = list(problem_ids)
        print(f"📊 Found {len(problem_ids)} matching problems")
        
        if problem_ids:
            # Get the first (and likely only) problem for this specific combination
            # Since we have exactly 1 problem per topic per difficulty, this is deterministic
            problem_id = problem_ids[0]
            print(f"✅ Selected problem: {problem_id}")
            
            problem_data = redis_client.hgetall(f'problem:{problem_id}')
            
            if problem_data:
                parsed_problem = parse_problem_data(problem_data, language)
                print(f"✅ Returning: {parsed_problem.get('title', 'Unknown')}")
                return parsed_problem
        
        print("⚠️ No problems found, returning default")
        
    except Exception as e:
        print(f"❌ Error in get_problem_by_criteria: {e}")
    
    # Return default problem if none found
    return {
        'id': 'two_sum',
        'title': 'Two Sum',
        'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.',
        'difficulty': difficulty,
        'topic': topic,
        'examples': [
            {'input': 'nums = [2,7,11,15], target = 9', 'output': '[0,1]', 'explanation': 'Because nums[0] + nums[1] = 2 + 7 = 9'}
        ],
        'hints': [
            'Try using a hash map to store numbers you\'ve seen',
            'For each number, check if its complement exists',
            'The complement is target - current_number'
        ],
        'constraints': [
            '2 ≤ nums.length ≤ 10⁴',
            '-10⁹ ≤ nums[i] ≤ 10⁹'
        ],
        'tags': ['Array', 'Hash Table']
    }

def fetch_problems_from_redis(difficulty, topic, language):
    """Fetch problems from Redis based on filters"""
    try:
        print(f"🔍 Fetching problems: difficulty={difficulty}, topic={topic}")
        
        if difficulty == 'all' and topic == 'all':
            # Get all problems
            problems = list(redis_client.scan_iter(match='problem:*'))
        else:
            # Use sets (not sorted sets) for filtering
            problem_ids = set()
            
            if difficulty != 'all' and topic != 'all':
                # Get intersection of difficulty and topic
                diff_problems = redis_client.smembers(f'problems_by_difficulty:{difficulty}')
                topic_problems = redis_client.smembers(f'problems_by_topic:{topic}')
                problem_ids = diff_problems.intersection(topic_problems)
            elif difficulty != 'all':
                # Get problems by difficulty only
                problem_ids = redis_client.smembers(f'problems_by_difficulty:{difficulty}')
            elif topic != 'all':
                # Get problems by topic only
                problem_ids = redis_client.smembers(f'problems_by_topic:{topic}')
            else:
                # Fallback to all problems
                problem_ids = redis_client.smembers('all_problems')
            
            # Convert to problem keys
            problems = [f'problem:{pid}' for pid in problem_ids]
        
        print(f"📊 Found {len(problems)} problems matching filters")
        
        # Convert to problem data
        problem_list = []
        for problem_key in problems:  # Show all problems (removed 20 limit)
            if isinstance(problem_key, bytes):
                problem_key = problem_key.decode('utf-8')
            
            if not problem_key.startswith('problem:'):
                problem_key = f'problem:{problem_key}'
                
            problem_data = redis_client.hgetall(problem_key)
            if problem_data:
                problem_list.append({
                    'id': problem_key.replace('problem:', ''),
                    'title': problem_data.get('title', 'Unknown Problem'),
                    'difficulty': problem_data.get('difficulty', 'Medium'),
                    'category': problem_data.get('category', 'General'),
                    'description': problem_data.get('description', 'No description available'),
                    'examples': problem_data.get('examples', '[]'),
                    'constraints': problem_data.get('constraints', '[]'),
                    'topic': problem_data.get('topic', 'general'),
                    'leetcode_url': problem_data.get('leetcode_url', ''),
                    'companies': problem_data.get('companies', '[]'),
                    'time_complexity': problem_data.get('time_complexity', 'Unknown'),
                    'space_complexity': problem_data.get('space_complexity', 'Unknown'),
                    'hints': problem_data.get('hints', '[]'),
                    'solution_template': problem_data.get('solution_template', ''),
                    'test_cases': problem_data.get('test_cases', '[]')
                })
        
        print(f"✅ Returning {len(problem_list)} formatted problems")
        
        # Randomize the order so users get different problems on "New Problem"
        import random
        random.shuffle(problem_list)
        
        return problem_list
        
    except Exception as e:
        print(f"❌ Error fetching problems: {e}")
        # Return some default problems as fallback
        return [
            {
                'id': 'two-sum',
                'title': 'Two Sum',
                'difficulty': 'Easy',
                'category': 'Arrays',
                'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.',
                'examples': '[{"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]"}]',
                'constraints': '["2 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9"]',
                'topic': 'arrays',
                'leetcode_url': 'https://leetcode.com/problems/two-sum/',
                'companies': '["Amazon", "Google", "Microsoft"]',
                'time_complexity': 'O(n)',
                'space_complexity': 'O(n)',
                'hints': '[]',
                'solution_template': '',
                'test_cases': '[]'
            }
        ]
        
    except Exception as e:
        print(f"Error fetching problems: {e}")
        # Return some default problems
        return [
            {
                'id': 'two-sum',
                'title': 'Two Sum',
                'difficulty': 'Easy',
                'category': 'Arrays',
                'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.',
                'examples': '[{"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]"}]',
                'constraints': '["2 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9"]'
            },
            {
                'id': 'reverse-string',
                'title': 'Reverse String',
                'difficulty': 'Easy',
                'category': 'Strings',
                'description': 'Write a function that reverses a string. The input string is given as an array of characters s.',
                'examples': '[{"input": "s = [\\"h\\",\\"e\\",\\"l\\",\\"l\\",\\"o\\"]", "output": "[\\"o\\",\\"l\\",\\"l\\",\\"e\\",\\"h\\"]"}]',
                'constraints': '["1 <= s.length <= 10^5"]'
            }
        ]

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
