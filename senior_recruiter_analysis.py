import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()

class SeniorRecruiterAnalysis:
    def __init__(self):
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        
    def analyze_solution(self, problem_title, code, explanation, language="python"):
        """
        Analyze solution like a renowned senior technical recruiter from FAANG companies
        """
        try:
            if not self.groq_api_key:
                return self._get_detailed_code_analysis(code, explanation, problem_title)

            # Create comprehensive analysis prompt
            prompt = f"""
You are Sarah Chen, a Senior Technical Recruiter at Google with 12 years of experience conducting over 2,000 technical interviews. You've hired engineers for teams like Search, YouTube, and Cloud Platform. You're known for your detailed, constructive feedback that actually helps candidates improve.

CANDIDATE SUBMISSION:
Problem: {problem_title}
Language: {language}

CODE:
```{language}
{code}
```

CANDIDATE EXPLANATION: 
{explanation}

Provide a comprehensive technical interview analysis as you would after a real Google technical interview. Be specific, constructive, and helpful.

Analyze these areas with specific scores (1-100):

1. CODE QUALITY: Look at structure, readability, variable naming, edge cases, error handling
2. ALGORITHM EFFICIENCY: Analyze time/space complexity, optimization opportunities
3. COMMUNICATION: How well did they explain their approach, complexity, trade-offs?
4. PROBLEM SOLVING: Did they understand the problem, consider alternatives, handle edge cases?
5. INTERVIEW READINESS: Overall assessment for technical interviews

For each area, provide:
- Specific score (realistic, not inflated)
- Detailed feedback explaining the score
- Specific improvement suggestions

Also provide:
- Overall hiring recommendation (STRONG_NO_HIRE, NO_HIRE, LEAN_NO_HIRE, LEAN_HIRE, HIRE, STRONG_HIRE)
- Level assessment (INTERN, NEW_GRAD, L3_JUNIOR, L4_MID, L5_SENIOR, L6_STAFF)
- Specific next steps for improvement

Format as JSON:
{{
    "code_quality": <score>,
    "algorithm_efficiency": <score>,
    "communication_skills": <score>,
    "problem_solving": <score>,
    "interview_readiness": <score>,
    "detailed_feedback": {{
        "code_quality_analysis": "<detailed analysis of code structure, naming, edge cases>",
        "algorithm_analysis": "<specific complexity analysis with optimization suggestions>",
        "communication_analysis": "<assessment of explanation quality and technical communication>",
        "problem_solving_analysis": "<evaluation of approach and methodology>",
        "overall_assessment": "<comprehensive summary from senior recruiter perspective>"
    }},
    "hiring_decision": "<recommendation>",
    "level_assessment": "<level>",
    "specific_improvements": [
        "<specific actionable improvement 1>",
        "<specific actionable improvement 2>",
        "<specific actionable improvement 3>"
    ],
    "interview_tips": [
        "<specific interview tip 1>",
        "<specific interview tip 2>",
        "<specific interview tip 3>"
    ],
    "next_steps": "<detailed next steps for candidate improvement>"
}}
"""

            headers = {
                'Authorization': f'Bearer {self.groq_api_key}',
                'Content-Type': 'application/json'
            }

            data = {
                'model': 'llama3-8b-8192',  # Use a working model
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are Sarah Chen, a Senior Technical Recruiter at Google with 12 years of experience. Provide detailed, constructive feedback that helps candidates improve. Be specific and realistic in your assessments.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'temperature': 0.3,
                'max_tokens': 2000  # Reduced token limit
            }

            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                try:
                    analysis = json.loads(content)
                    return self._format_senior_recruiter_analysis(analysis)
                except json.JSONDecodeError:
                    print("⚠️ JSON parsing failed, using text analysis")
                    return self._parse_text_analysis(content, code, explanation)
            else:
                print(f"Groq API error: {response.status_code} - {response.text}")
                return self._get_detailed_code_analysis(code, explanation, problem_title)

        except Exception as e:
            print(f"Analysis error: {str(e)}")
            return self._get_detailed_code_analysis(code, explanation, problem_title)

    def _format_senior_recruiter_analysis(self, analysis):
        """Format the analysis for display"""
        return {
            "code_quality": analysis.get('code_quality', 50),
            "algorithm_efficiency": analysis.get('algorithm_efficiency', 45),
            "communication_skills": analysis.get('communication_skills', 55),
            "problem_solving": analysis.get('problem_solving', 50),
            "interview_readiness": analysis.get('interview_readiness', 48),
            "feedback": self._create_formatted_feedback(analysis),
            "recommendation": analysis.get('next_steps', 'Focus on algorithm optimization and technical communication.')
        }

    def _create_formatted_feedback(self, analysis):
        """Create well-structured HTML feedback"""
        detailed = analysis.get('detailed_feedback', {})
        
        feedback_html = []
        
        # Code Quality Analysis
        if detailed.get('code_quality_analysis'):
            feedback_html.append(f"""
            <div class="analysis-section mb-6">
                <div class="section-header bg-blue-50 border-l-4 border-blue-500 p-4 mb-3">
                    <h4 class="text-lg font-semibold text-blue-700 flex items-center">
                        <span class="mr-2">🔧</span> Code Quality Analysis
                        <span class="ml-auto text-sm bg-blue-100 px-2 py-1 rounded">{analysis.get('code_quality', 0)}/100</span>
                    </h4>
                </div>
                <div class="section-content bg-white p-4 border border-gray-200 rounded">
                    <p class="text-gray-700 leading-relaxed">{detailed['code_quality_analysis']}</p>
                </div>
            </div>
            """)
        
        # Algorithm Analysis
        if detailed.get('algorithm_analysis'):
            feedback_html.append(f"""
            <div class="analysis-section mb-6">
                <div class="section-header bg-orange-50 border-l-4 border-orange-500 p-4 mb-3">
                    <h4 class="text-lg font-semibold text-orange-700 flex items-center">
                        <span class="mr-2">⚡</span> Algorithm & Complexity Analysis
                        <span class="ml-auto text-sm bg-orange-100 px-2 py-1 rounded">{analysis.get('algorithm_efficiency', 0)}/100</span>
                    </h4>
                </div>
                <div class="section-content bg-white p-4 border border-gray-200 rounded">
                    <p class="text-gray-700 leading-relaxed">{detailed['algorithm_analysis']}</p>
                </div>
            </div>
            """)
        
        # Communication Analysis
        if detailed.get('communication_analysis'):
            feedback_html.append(f"""
            <div class="analysis-section mb-6">
                <div class="section-header bg-green-50 border-l-4 border-green-500 p-4 mb-3">
                    <h4 class="text-lg font-semibold text-green-700 flex items-center">
                        <span class="mr-2">💬</span> Technical Communication
                        <span class="ml-auto text-sm bg-green-100 px-2 py-1 rounded">{analysis.get('communication_skills', 0)}/100</span>
                    </h4>
                </div>
                <div class="section-content bg-white p-4 border border-gray-200 rounded">
                    <p class="text-gray-700 leading-relaxed">{detailed['communication_analysis']}</p>
                </div>
            </div>
            """)
        
        # Problem Solving Analysis
        if detailed.get('problem_solving_analysis'):
            feedback_html.append(f"""
            <div class="analysis-section mb-6">
                <div class="section-header bg-purple-50 border-l-4 border-purple-500 p-4 mb-3">
                    <h4 class="text-lg font-semibold text-purple-700 flex items-center">
                        <span class="mr-2">🧠</span> Problem Solving Approach
                        <span class="ml-auto text-sm bg-purple-100 px-2 py-1 rounded">{analysis.get('problem_solving', 0)}/100</span>
                    </h4>
                </div>
                <div class="section-content bg-white p-4 border border-gray-200 rounded">
                    <p class="text-gray-700 leading-relaxed">{detailed['problem_solving_analysis']}</p>
                </div>
            </div>
            """)
        
        # Overall Assessment
        if detailed.get('overall_assessment'):
            feedback_html.append(f"""
            <div class="analysis-section mb-6">
                <div class="section-header bg-gray-50 border-l-4 border-gray-500 p-4 mb-3">
                    <h4 class="text-lg font-semibold text-gray-700 flex items-center">
                        <span class="mr-2">📋</span> Senior Recruiter Assessment
                        <span class="ml-auto text-sm bg-gray-100 px-2 py-1 rounded">{analysis.get('interview_readiness', 0)}/100</span>
                    </h4>
                </div>
                <div class="section-content bg-white p-4 border border-gray-200 rounded">
                    <p class="text-gray-700 leading-relaxed">{detailed['overall_assessment']}</p>
                </div>
            </div>
            """)
        
        # Hiring Decision
        hiring_decision = analysis.get('hiring_decision', 'LEAN_NO_HIRE')
        level = analysis.get('level_assessment', 'L3_JUNIOR')
        
        decision_colors = {
            'STRONG_HIRE': 'green',
            'HIRE': 'green',
            'LEAN_HIRE': 'yellow',
            'LEAN_NO_HIRE': 'orange',
            'NO_HIRE': 'red',
            'STRONG_NO_HIRE': 'red'
        }
        
        color = decision_colors.get(hiring_decision, 'gray')
        
        feedback_html.append(f"""
        <div class="analysis-section mb-6">
            <div class="section-header bg-{color}-50 border-l-4 border-{color}-500 p-4 mb-3">
                <h4 class="text-lg font-semibold text-{color}-700 flex items-center">
                    <span class="mr-2">🎯</span> Hiring Recommendation
                </h4>
            </div>
            <div class="section-content bg-white p-4 border border-gray-200 rounded">
                <div class="flex items-center space-x-4 mb-3">
                    <span class="px-4 py-2 bg-{color}-100 text-{color}-800 rounded-lg font-semibold">
                        {hiring_decision.replace('_', ' ')}
                    </span>
                    <span class="px-3 py-1 bg-gray-100 text-gray-700 rounded-lg">
                        {level.replace('_', ' ')}
                    </span>
                </div>
            </div>
        </div>
        """)
        
        # Specific Improvements
        improvements = analysis.get('specific_improvements', [])
        if improvements:
            improvement_items = ''.join([
                f'<li class="mb-3 p-3 bg-red-50 border-l-3 border-red-300 rounded"><strong>•</strong> {imp}</li>' 
                for imp in improvements
            ])
            feedback_html.append(f"""
            <div class="analysis-section mb-6">
                <div class="section-header bg-red-50 border-l-4 border-red-500 p-4 mb-3">
                    <h4 class="text-lg font-semibold text-red-700 flex items-center">
                        <span class="mr-2">🎯</span> Priority Improvements
                    </h4>
                </div>
                <div class="section-content bg-white p-4 border border-gray-200 rounded">
                    <ul class="space-y-2">{improvement_items}</ul>
                </div>
            </div>
            """)
        
        # Interview Tips
        tips = analysis.get('interview_tips', [])
        if tips:
            tip_items = ''.join([
                f'<li class="mb-3 p-3 bg-indigo-50 border-l-3 border-indigo-300 rounded"><strong>💡</strong> {tip}</li>' 
                for tip in tips
            ])
            feedback_html.append(f"""
            <div class="analysis-section mb-6">
                <div class="section-header bg-indigo-50 border-l-4 border-indigo-500 p-4 mb-3">
                    <h4 class="text-lg font-semibold text-indigo-700 flex items-center">
                        <span class="mr-2">💡</span> Interview Success Tips
                    </h4>
                </div>
                <div class="section-content bg-white p-4 border border-gray-200 rounded">
                    <ul class="space-y-2">{tip_items}</ul>
                </div>
            </div>
            """)
        
        return ''.join(feedback_html)

    def _get_detailed_code_analysis(self, code, explanation, problem_title):
        """Provide detailed analysis when API is not available"""
        
        # Analyze code characteristics
        code_issues = []
        algorithm_issues = []
        communication_issues = []
        
        # Code quality analysis
        if len(code.split('\n')) < 5:
            code_issues.append("Solution appears too brief - may be missing edge case handling")
        
        if not re.search(r'def\s+\w+', code):
            code_issues.append("No function definition found - code structure unclear")
            
        if 'for' in code and 'for' in code[code.find('for')+10:]:
            algorithm_issues.append("Nested loops detected - O(n²) time complexity")
            
        if not any(word in code.lower() for word in ['return', 'result']):
            code_issues.append("No clear return statement or result handling")
        
        # Algorithm analysis
        if 'sort' in code.lower():
            algorithm_issues.append("Sorting used - consider if O(n log n) is optimal")
        elif any(pattern in code for pattern in ['for i in range', 'while']):
            if 'for' in code and 'for' in code[code.find('for')+10:]:
                algorithm_issues.append("Nested iteration - likely suboptimal complexity")
        
        # Communication analysis
        if len(explanation.split()) < 15:
            communication_issues.append("Explanation too brief for technical interview standards")
            
        if 'complexity' not in explanation.lower():
            communication_issues.append("No time/space complexity analysis provided")
            
        if 'approach' not in explanation.lower() and 'algorithm' not in explanation.lower():
            communication_issues.append("Missing discussion of algorithmic approach")
            
        if any(phrase in explanation.lower() for phrase in ['copy', 'paste', 'copied']):
            communication_issues.append("Indicates solution was copied rather than developed")
        
        # Calculate realistic scores
        code_score = max(20, 75 - len(code_issues) * 15)
        algorithm_score = max(15, 70 - len(algorithm_issues) * 20)
        communication_score = max(25, 80 - len(communication_issues) * 15)
        problem_solving_score = (code_score + algorithm_score) // 2
        interview_readiness = min(code_score, algorithm_score, communication_score)
        
        # Determine hiring decision
        avg_score = (code_score + algorithm_score + communication_score + problem_solving_score + interview_readiness) / 5
        
        if avg_score >= 75:
            hiring_decision = "HIRE"
            level = "L4_MID"
        elif avg_score >= 60:
            hiring_decision = "LEAN_HIRE"
            level = "L3_JUNIOR"
        elif avg_score >= 45:
            hiring_decision = "LEAN_NO_HIRE"
            level = "L3_JUNIOR"
        else:
            hiring_decision = "NO_HIRE"
            level = "NEW_GRAD"
        
        return {
            "code_quality": code_score,
            "algorithm_efficiency": algorithm_score,
            "communication_skills": communication_score,
            "problem_solving": problem_solving_score,
            "interview_readiness": interview_readiness,
            "feedback": self._create_detailed_fallback_feedback(
                code_issues, algorithm_issues, communication_issues, 
                code_score, algorithm_score, communication_score,
                hiring_decision, level
            ),
            "recommendation": f"Focus on {'algorithm optimization, ' if algorithm_score < 60 else ''}{'code structure, ' if code_score < 60 else ''}{'technical communication' if communication_score < 60 else 'continued practice'}."
        }

    def _create_detailed_fallback_feedback(self, code_issues, algorithm_issues, communication_issues, 
                                         code_score, algorithm_score, communication_score, 
                                         hiring_decision, level):
        """Create detailed fallback feedback when API is unavailable"""
        
        feedback_sections = []
        
        # Code Quality Section
        code_feedback = "Strong code structure with clear logic flow." if code_score >= 70 else \
                       "Code shows basic functionality but needs improvement in structure and clarity."
        if code_issues:
            code_feedback += f" Specific issues: {'; '.join(code_issues)}."
            
        feedback_sections.append(f"""
        <div class="analysis-section mb-6">
            <div class="section-header bg-blue-50 border-l-4 border-blue-500 p-4 mb-3">
                <h4 class="text-lg font-semibold text-blue-700 flex items-center">
                    <span class="mr-2">🔧</span> Code Quality Analysis
                    <span class="ml-auto text-sm bg-blue-100 px-2 py-1 rounded">{code_score}/100</span>
                </h4>
            </div>
            <div class="section-content bg-white p-4 border border-gray-200 rounded">
                <p class="text-gray-700 leading-relaxed">{code_feedback}</p>
            </div>
        </div>
        """)
        
        # Algorithm Analysis
        algorithm_feedback = "Efficient algorithmic approach with good complexity." if algorithm_score >= 70 else \
                           "Algorithm needs optimization for better time/space complexity."
        if algorithm_issues:
            algorithm_feedback += f" Areas for improvement: {'; '.join(algorithm_issues)}."
            
        feedback_sections.append(f"""
        <div class="analysis-section mb-6">
            <div class="section-header bg-orange-50 border-l-4 border-orange-500 p-4 mb-3">
                <h4 class="text-lg font-semibold text-orange-700 flex items-center">
                    <span class="mr-2">⚡</span> Algorithm & Complexity Analysis
                    <span class="ml-auto text-sm bg-orange-100 px-2 py-1 rounded">{algorithm_score}/100</span>
                </h4>
            </div>
            <div class="section-content bg-white p-4 border border-gray-200 rounded">
                <p class="text-gray-700 leading-relaxed">{algorithm_feedback}</p>
            </div>
        </div>
        """)
        
        # Communication Analysis
        communication_feedback = "Clear technical communication with good explanation of approach." if communication_score >= 70 else \
                                "Technical communication needs significant improvement for interview success."
        if communication_issues:
            communication_feedback += f" Key gaps: {'; '.join(communication_issues)}."
            
        feedback_sections.append(f"""
        <div class="analysis-section mb-6">
            <div class="section-header bg-green-50 border-l-4 border-green-500 p-4 mb-3">
                <h4 class="text-lg font-semibold text-green-700 flex items-center">
                    <span class="mr-2">💬</span> Technical Communication
                    <span class="ml-auto text-sm bg-green-100 px-2 py-1 rounded">{communication_score}/100</span>
                </h4>
            </div>
            <div class="section-content bg-white p-4 border border-gray-200 rounded">
                <p class="text-gray-700 leading-relaxed">{communication_feedback}</p>
            </div>
        </div>
        """)
        
        # Hiring Decision
        decision_colors = {
            'HIRE': 'green',
            'LEAN_HIRE': 'yellow',
            'LEAN_NO_HIRE': 'orange',
            'NO_HIRE': 'red'
        }
        
        color = decision_colors.get(hiring_decision, 'gray')
        
        feedback_sections.append(f"""
        <div class="analysis-section mb-6">
            <div class="section-header bg-{color}-50 border-l-4 border-{color}-500 p-4 mb-3">
                <h4 class="text-lg font-semibold text-{color}-700 flex items-center">
                    <span class="mr-2">🎯</span> Senior Recruiter Recommendation
                </h4>
            </div>
            <div class="section-content bg-white p-4 border border-gray-200 rounded">
                <div class="flex items-center space-x-4 mb-3">
                    <span class="px-4 py-2 bg-{color}-100 text-{color}-800 rounded-lg font-semibold">
                        {hiring_decision.replace('_', ' ')}
                    </span>
                    <span class="px-3 py-1 bg-gray-100 text-gray-700 rounded-lg">
                        {level.replace('_', ' ')}
                    </span>
                </div>
                <p class="text-gray-700">Based on code quality, algorithm efficiency, and technical communication assessment.</p>
            </div>
        </div>
        """)
        
        return ''.join(feedback_sections)

    def _parse_text_analysis(self, text_content, code, explanation):
        """Parse text-based analysis if JSON parsing fails"""
        return {
            "code_quality": 50,
            "algorithm_efficiency": 45,
            "communication_skills": 55,
            "problem_solving": 50,
            "interview_readiness": 48,
            "feedback": f"""
            <div class="analysis-section mb-6">
                <div class="section-header bg-gray-50 border-l-4 border-gray-500 p-4 mb-3">
                    <h4 class="text-lg font-semibold text-gray-700 flex items-center">
                        <span class="mr-2">📋</span> Senior Technical Recruiter Analysis
                    </h4>
                </div>
                <div class="section-content bg-white p-4 border border-gray-200 rounded">
                    <div class="text-gray-700 leading-relaxed">{text_content}</div>
                </div>
            </div>
            """,
            "recommendation": "Continue practicing with focus on algorithm optimization and technical communication."
        }
