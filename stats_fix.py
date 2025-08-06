import json
import time
from datetime import datetime, timedelta

def calculate_user_stats(redis_client, user_id):
    """
    Calculate accurate user statistics
    """
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
                'interview_level': 'Beginner'
            }
        
        # Calculate average score from all submissions
        total_score = 0
        scores = []
        submission_dates = []
        
        for key in submission_keys:
            submission_data = redis_client.hgetall(key)
            if submission_data and 'scores' in submission_data:
                try:
                    score_data = json.loads(submission_data['scores'])
                    # Calculate overall score as average of all metrics
                    overall_score = sum([
                        score_data.get('code_quality', 0),
                        score_data.get('algorithm_efficiency', 0),
                        score_data.get('communication_skills', 0),
                        score_data.get('problem_solving', 0),
                        score_data.get('interview_readiness', 0)
                    ]) / 5
                    
                    scores.append(overall_score)
                    total_score += overall_score
                    
                    # Track submission date for streak calculation
                    if 'timestamp' in submission_data:
                        submission_dates.append(int(submission_data['timestamp']))
                        
                except (json.JSONDecodeError, KeyError, ZeroDivisionError):
                    continue
        
        # Calculate average score
        average_score = round(total_score / len(scores)) if scores else 0
        
        # Calculate streak (consecutive days with submissions)
        streak = calculate_streak(submission_dates)
        
        # Determine interview level based on average score and problems solved
        interview_level = determine_interview_level(average_score, unique_problems)
        
        return {
            'problems_solved': unique_problems,
            'total_submissions': total_submissions,
            'average_score': average_score,
            'streak': streak,
            'interview_level': interview_level
        }
        
    except Exception as e:
        print(f"Error calculating stats: {e}")
        return {
            'problems_solved': 0,
            'total_submissions': 0,
            'average_score': 0,
            'streak': 0,
            'interview_level': 'Beginner'
        }

def calculate_streak(submission_timestamps):
    """
    Calculate consecutive days streak
    """
    if not submission_timestamps:
        return 0
    
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
    """
    Determine interview readiness level
    """
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

def update_user_submission(redis_client, user_id, problem_id, scores):
    """
    Update user submission with proper tracking
    """
    try:
        # Store submission with timestamp
        submission_key = f"submission:{user_id}:{int(time.time())}"
        redis_client.hset(submission_key, mapping={
            'problem_id': problem_id,
            'timestamp': int(time.time()),
            'scores': json.dumps(scores)
        })
        
        # Add to unique problems set (only if not already solved)
        user_problems_key = f"user:{user_id}:solved_problems"
        redis_client.sadd(user_problems_key, problem_id)
        
        # Set expiration for submissions (optional - keep for 30 days)
        redis_client.expire(submission_key, 30 * 24 * 3600)
        
        return True
        
    except Exception as e:
        print(f"Error updating user submission: {e}")
        return False
