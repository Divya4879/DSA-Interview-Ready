def format_analysis_feedback(analysis):
    """
    Format the analysis feedback with proper structure and readability
    """
    detailed = analysis.get('detailed_feedback', {})
    
    # Create well-structured HTML feedback
    feedback_html = []
    
    # Header with overall scores
    scores = {
        'Code Quality': analysis.get('code_quality', 0),
        'Algorithm Efficiency': analysis.get('algorithm_efficiency', 0),
        'Communication': analysis.get('communication_skills', 0),
        'Problem Solving': analysis.get('problem_solving', 0),
        'Interview Readiness': analysis.get('interview_readiness', 0)
    }
    
    # Code Quality Section
    if detailed.get('code_quality_feedback'):
        feedback_html.append(f"""
        <div class="analysis-section">
            <h4 class="section-title">🔧 Code Quality Analysis</h4>
            <div class="section-content">
                <div class="score-badge score-{get_score_class(scores['Code Quality'])}">{scores['Code Quality']}/100</div>
                <p>{detailed['code_quality_feedback']}</p>
            </div>
        </div>
        """)
    
    # Algorithm Analysis
    if detailed.get('algorithm_feedback'):
        feedback_html.append(f"""
        <div class="analysis-section">
            <h4 class="section-title">⚡ Algorithm & Complexity Analysis</h4>
            <div class="section-content">
                <div class="score-badge score-{get_score_class(scores['Algorithm Efficiency'])}">{scores['Algorithm Efficiency']}/100</div>
                <p>{detailed['algorithm_feedback']}</p>
            </div>
        </div>
        """)
    
    # Communication Assessment
    if detailed.get('communication_feedback'):
        feedback_html.append(f"""
        <div class="analysis-section">
            <h4 class="section-title">💬 Communication Assessment</h4>
            <div class="section-content">
                <div class="score-badge score-{get_score_class(scores['Communication'])}">{scores['Communication']}/100</div>
                <p>{detailed['communication_feedback']}</p>
            </div>
        </div>
        """)
    
    # Problem Solving Approach
    if detailed.get('problem_solving_feedback'):
        feedback_html.append(f"""
        <div class="analysis-section">
            <h4 class="section-title">🧠 Problem Solving Approach</h4>
            <div class="section-content">
                <div class="score-badge score-{get_score_class(scores['Problem Solving'])}">{scores['Problem Solving']}/100</div>
                <p>{detailed['problem_solving_feedback']}</p>
            </div>
        </div>
        """)
    
    # Overall Assessment
    if detailed.get('overall_assessment'):
        feedback_html.append(f"""
        <div class="analysis-section">
            <h4 class="section-title">📋 Overall Assessment</h4>
            <div class="section-content">
                <div class="score-badge score-{get_score_class(scores['Interview Readiness'])}">{scores['Interview Readiness']}/100</div>
                <p>{detailed['overall_assessment']}</p>
            </div>
        </div>
        """)
    
    # Hiring Decision
    hiring_decision = analysis.get('hiring_decision', 'LEAN_HIRE')
    level = analysis.get('level_assessment', 'MID_LEVEL')
    decision_class = get_decision_class(hiring_decision)
    
    feedback_html.append(f"""
    <div class="analysis-section hiring-decision">
        <h4 class="section-title">🎯 Hiring Recommendation</h4>
        <div class="section-content">
            <div class="decision-badge {decision_class}">{hiring_decision}</div>
            <div class="level-badge">Level: {level}</div>
        </div>
    </div>
    """)
    
    # Key Areas for Improvement
    improvements = detailed.get('specific_improvements', [])
    if improvements:
        improvement_items = ''.join([f'<li class="improvement-item">{imp}</li>' for imp in improvements])
        feedback_html.append(f"""
        <div class="analysis-section">
            <h4 class="section-title">🎯 Key Areas for Improvement</h4>
            <div class="section-content">
                <ul class="improvement-list">{improvement_items}</ul>
            </div>
        </div>
        """)
    
    # Interview Tips
    tips = detailed.get('interview_tips', [])
    if tips:
        tip_items = ''.join([f'<li class="tip-item">{tip}</li>' for tip in tips])
        feedback_html.append(f"""
        <div class="analysis-section">
            <h4 class="section-title">💡 Interview Tips</h4>
            <div class="section-content">
                <ul class="tips-list">{tip_items}</ul>
            </div>
        </div>
        """)
    
    return ''.join(feedback_html)

def get_score_class(score):
    """Get CSS class based on score"""
    if score >= 80:
        return 'excellent'
    elif score >= 60:
        return 'good'
    else:
        return 'needs-work'

def get_decision_class(decision):
    """Get CSS class based on hiring decision"""
    if decision in ['STRONG_HIRE', 'HIRE']:
        return 'hire'
    elif decision == 'LEAN_HIRE':
        return 'lean-hire'
    else:
        return 'no-hire'

# Fallback for plain text formatting
def format_analysis_text(analysis):
    """
    Format analysis as clean HTML with proper structure
    """
    detailed = analysis.get('detailed_feedback', {})
    
    sections = []
    
    # Code Quality
    if detailed.get('code_quality_feedback'):
        sections.append(f"""
        <div class="analysis-section mb-6">
            <h4 class="text-lg font-semibold text-blue-600 mb-3 flex items-center">
                <span class="mr-2">🔧</span> Code Quality Analysis
            </h4>
            <div class="bg-blue-50 border-l-4 border-blue-400 p-4 rounded">
                <p class="text-gray-700 leading-relaxed">{detailed['code_quality_feedback']}</p>
            </div>
        </div>
        """)
    
    # Algorithm Analysis  
    if detailed.get('algorithm_feedback'):
        sections.append(f"""
        <div class="analysis-section mb-6">
            <h4 class="text-lg font-semibold text-orange-600 mb-3 flex items-center">
                <span class="mr-2">⚡</span> Algorithm & Complexity Analysis
            </h4>
            <div class="bg-orange-50 border-l-4 border-orange-400 p-4 rounded">
                <p class="text-gray-700 leading-relaxed">{detailed['algorithm_feedback']}</p>
            </div>
        </div>
        """)
    
    # Communication
    if detailed.get('communication_feedback'):
        sections.append(f"""
        <div class="analysis-section mb-6">
            <h4 class="text-lg font-semibold text-green-600 mb-3 flex items-center">
                <span class="mr-2">💬</span> Communication Assessment
            </h4>
            <div class="bg-green-50 border-l-4 border-green-400 p-4 rounded">
                <p class="text-gray-700 leading-relaxed">{detailed['communication_feedback']}</p>
            </div>
        </div>
        """)
    
    # Problem Solving
    if detailed.get('problem_solving_feedback'):
        sections.append(f"""
        <div class="analysis-section mb-6">
            <h4 class="text-lg font-semibold text-purple-600 mb-3 flex items-center">
                <span class="mr-2">🧠</span> Problem Solving Approach
            </h4>
            <div class="bg-purple-50 border-l-4 border-purple-400 p-4 rounded">
                <p class="text-gray-700 leading-relaxed">{detailed['problem_solving_feedback']}</p>
            </div>
        </div>
        """)
    
    # Overall Assessment
    if detailed.get('overall_assessment'):
        sections.append(f"""
        <div class="analysis-section mb-6">
            <h4 class="text-lg font-semibold text-gray-700 mb-3 flex items-center">
                <span class="mr-2">📋</span> Overall Assessment
            </h4>
            <div class="bg-gray-50 border-l-4 border-gray-400 p-4 rounded">
                <p class="text-gray-700 leading-relaxed">{detailed['overall_assessment']}</p>
            </div>
        </div>
        """)
    
    # Hiring Decision
    hiring_decision = analysis.get('hiring_decision', 'LEAN_HIRE')
    level = analysis.get('level_assessment', 'MID_LEVEL')
    decision_color = 'red' if 'NO_HIRE' in hiring_decision else 'yellow' if 'LEAN' in hiring_decision else 'green'
    
    sections.append(f"""
    <div class="analysis-section mb-6">
        <h4 class="text-lg font-semibold text-{decision_color}-600 mb-3 flex items-center">
            <span class="mr-2">🎯</span> Hiring Recommendation
        </h4>
        <div class="bg-{decision_color}-50 border-l-4 border-{decision_color}-400 p-4 rounded">
            <div class="flex items-center space-x-4">
                <span class="px-3 py-1 bg-{decision_color}-100 text-{decision_color}-800 rounded-full font-semibold">
                    {hiring_decision}
                </span>
                <span class="px-3 py-1 bg-gray-100 text-gray-700 rounded-full">
                    Level: {level}
                </span>
            </div>
        </div>
    </div>
    """)
    
    # Improvements
    improvements = detailed.get('specific_improvements', [])
    if improvements:
        improvement_items = ''.join([f'<li class="mb-2 text-gray-700">• {imp}</li>' for imp in improvements])
        sections.append(f"""
        <div class="analysis-section mb-6">
            <h4 class="text-lg font-semibold text-red-600 mb-3 flex items-center">
                <span class="mr-2">🎯</span> Critical Areas for Improvement
            </h4>
            <div class="bg-red-50 border-l-4 border-red-400 p-4 rounded">
                <ul class="space-y-1">{improvement_items}</ul>
            </div>
        </div>
        """)
    
    # Tips
    tips = detailed.get('interview_tips', [])
    if tips:
        tip_items = ''.join([f'<li class="mb-2 text-gray-700">• {tip}</li>' for tip in tips])
        sections.append(f"""
        <div class="analysis-section mb-6">
            <h4 class="text-lg font-semibold text-indigo-600 mb-3 flex items-center">
                <span class="mr-2">💡</span> Interview Survival Tips
            </h4>
            <div class="bg-indigo-50 border-l-4 border-indigo-400 p-4 rounded">
                <ul class="space-y-1">{tip_items}</ul>
            </div>
        </div>
        """)
    
    return ''.join(sections)
