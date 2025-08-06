# This file contains the improved functions that will be integrated into app.py

def get_user_stats_improved(user_id):
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
        print(f"Error getting user stats: {e}")
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


def format_recruiter_feedback(key_insights, recommendation):
    """Format recruiter feedback with proper structure and bold text"""
    formatted_insights = []
    
    for insight in key_insights:
        # Check if insight contains quoted text that should be bold
        if '"' in insight:
            # Split by quotes and format
            parts = insight.split('"')
            formatted_parts = []
            
            for i, part in enumerate(parts):
                if i % 2 == 1:  # Odd indices are inside quotes (should be bold)
                    formatted_parts.append(f"**{part}**")
                else:
                    formatted_parts.append(part)
            
            formatted_insight = ''.join(formatted_parts)
        else:
            formatted_insight = insight
        
        formatted_insights.append(formatted_insight)
    
    # Format recommendation similarly
    if '"' in recommendation:
        parts = recommendation.split('"')
        formatted_parts = []
        
        for i, part in enumerate(parts):
            if i % 2 == 1:  # Odd indices are inside quotes (should be bold)
                formatted_parts.append(f"**{part}**")
            else:
                formatted_parts.append(part)
        
        formatted_recommendation = ''.join(formatted_parts)
    else:
        formatted_recommendation = recommendation
    
    return formatted_insights, formatted_recommendation


def get_file_extension(language):
    """Get appropriate file extension based on programming language"""
    extensions = {
        'python': 'py',
        'javascript': 'js',
        'java': 'java',
        'cpp': 'cpp',
        'c++': 'cpp',
        'c': 'c',
        'go': 'go',
        'rust': 'rs',
        'typescript': 'ts',
        'php': 'php',
        'ruby': 'rb',
        'swift': 'swift',
        'kotlin': 'kt',
        'scala': 'scala',
        'r': 'r',
        'matlab': 'm'
    }
    
    return extensions.get(language.lower(), 'txt')
