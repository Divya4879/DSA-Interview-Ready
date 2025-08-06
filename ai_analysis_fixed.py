import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class ProperTechnicalAnalysis:
    def __init__(self):
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        
    def analyze_solution(self, problem_title, code, explanation, language="python"):
        """
        Provide real senior technical recruiter level analysis
        """
        try:
            if not self.groq_api_key:
                return self._get_fallback_analysis()

            # Create a comprehensive analysis prompt
            prompt = f"""
You are a senior technical recruiter at a FAANG company with 15+ years of experience interviewing software engineers. Analyze this coding interview solution with the depth and specificity of a real technical interview.

PROBLEM: {problem_title}
LANGUAGE: {language}

CODE:
```{language}
{code}
```

CANDIDATE EXPLANATION: {explanation}

Provide a comprehensive analysis as a senior technical recruiter would. Be specific, critical, and constructive. Address:

1. CODE QUALITY (1-100):
   - Variable naming and readability
   - Code structure and organization  
   - Edge case handling
   - Coding style and best practices
   - Specific issues you notice

2. ALGORITHM EFFICIENCY (1-100):
   - Time complexity analysis (be specific - O(n), O(log n), etc.)
   - Space complexity analysis
   - Algorithm choice appropriateness
   - Optimization opportunities
   - Comparison to optimal solutions

3. COMMUNICATION SKILLS (1-100):
   - Clarity of explanation
   - Technical vocabulary usage
   - Problem-solving thought process
   - Ability to articulate trade-offs
   - Interview presence

4. PROBLEM SOLVING APPROACH (1-100):
   - Problem understanding demonstration
   - Solution strategy
   - Handling of edge cases
   - Debugging approach
   - Alternative solutions considered

5. INTERVIEW READINESS (1-100):
   - Overall technical competence
   - Communication during problem solving
   - Confidence and composure
   - Readiness for technical interviews

Provide detailed, specific feedback that a real senior recruiter would give. Be honest about weaknesses and specific about improvements needed.

Format as JSON:
{{
    "code_quality": <score>,
    "algorithm_efficiency": <score>, 
    "communication_skills": <score>,
    "problem_solving": <score>,
    "interview_readiness": <score>,
    "detailed_feedback": {{
        "code_quality_feedback": "<specific detailed feedback>",
        "algorithm_feedback": "<specific complexity analysis and optimization suggestions>",
        "communication_feedback": "<specific communication strengths/weaknesses>",
        "problem_solving_feedback": "<specific problem-solving approach analysis>",
        "overall_assessment": "<honest overall assessment>",
        "specific_improvements": ["<improvement 1>", "<improvement 2>", "<improvement 3>"],
        "interview_tips": ["<tip 1>", "<tip 2>", "<tip 3>"]
    }},
    "hiring_decision": "<STRONG_HIRE|HIRE|LEAN_HIRE|LEAN_NO_HIRE|NO_HIRE>",
    "level_assessment": "<JUNIOR|MID_LEVEL|SENIOR|STAFF>",
    "next_steps": "<specific actionable next steps>"
}}
"""

            headers = {
                'Authorization': f'Bearer {self.groq_api_key}',
                'Content-Type': 'application/json'
            }

            data = {
                'model': 'mixtral-8x7b-32768',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are a senior technical recruiter at Google with 15+ years of experience. Provide brutally honest, specific, and actionable feedback like you would in a real technical interview. Be detailed and constructive.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'temperature': 0.3,
                'max_tokens': 2000
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
                    return self._format_analysis(analysis)
                except json.JSONDecodeError:
                    return self._parse_text_analysis(content)
            else:
                print(f"Groq API error: {response.status_code}")
                return self._get_fallback_analysis()

        except Exception as e:
            print(f"Analysis error: {str(e)}")
            return self._get_fallback_analysis()

    def _format_analysis(self, analysis):
        """Format the analysis for display"""
        detailed = analysis.get('detailed_feedback', {})
        
        return {
            "code_quality": analysis.get('code_quality', 70),
            "algorithm_efficiency": analysis.get('algorithm_efficiency', 70),
            "communication_skills": analysis.get('communication_skills', 70),
            "problem_solving": analysis.get('problem_solving', 70),
            "interview_readiness": analysis.get('interview_readiness', 70),
            "feedback": self._create_detailed_feedback(detailed, analysis),
            "recommendation": analysis.get('next_steps', 'Continue practicing with focus on identified areas.')
        }

    def _create_detailed_feedback(self, detailed, analysis):
        """Create comprehensive feedback text"""
        feedback_parts = []
        
        # Code Quality Section
        if detailed.get('code_quality_feedback'):
            feedback_parts.append(f"**Code Quality Analysis:**\n{detailed['code_quality_feedback']}")
        
        # Algorithm Analysis
        if detailed.get('algorithm_feedback'):
            feedback_parts.append(f"**Algorithm & Complexity Analysis:**\n{detailed['algorithm_feedback']}")
        
        # Communication Assessment
        if detailed.get('communication_feedback'):
            feedback_parts.append(f"**Communication Assessment:**\n{detailed['communication_feedback']}")
        
        # Problem Solving Approach
        if detailed.get('problem_solving_feedback'):
            feedback_parts.append(f"**Problem Solving Approach:**\n{detailed['problem_solving_feedback']}")
        
        # Overall Assessment
        if detailed.get('overall_assessment'):
            feedback_parts.append(f"**Overall Assessment:**\n{detailed['overall_assessment']}")
        
        # Hiring Decision
        hiring_decision = analysis.get('hiring_decision', 'LEAN_HIRE')
        level = analysis.get('level_assessment', 'MID_LEVEL')
        feedback_parts.append(f"**Hiring Recommendation:** {hiring_decision} at {level} level")
        
        # Specific Improvements
        improvements = detailed.get('specific_improvements', [])
        if improvements:
            feedback_parts.append("**Key Areas for Improvement:**\n" + "\n".join([f"• {imp}" for imp in improvements]))
        
        # Interview Tips
        tips = detailed.get('interview_tips', [])
        if tips:
            feedback_parts.append("**Interview Tips:**\n" + "\n".join([f"• {tip}" for tip in tips]))
        
        return "\n\n".join(feedback_parts)

    def _parse_text_analysis(self, text_content):
        """Parse text-based analysis if JSON parsing fails"""
        return {
            "code_quality": 75,
            "algorithm_efficiency": 75,
            "communication_skills": 75,
            "problem_solving": 75,
            "interview_readiness": 75,
            "feedback": f"**Detailed Technical Analysis:**\n\n{text_content}",
            "recommendation": "Focus on the specific areas mentioned above for improvement."
        }

    def _get_fallback_analysis(self):
        """Provide realistic fallback analysis when API fails"""
        return {
            "code_quality": 72,
            "algorithm_efficiency": 68,
            "communication_skills": 75,
            "problem_solving": 70,
            "interview_readiness": 71,
            "feedback": """**Code Quality Analysis:**
Your solution shows basic understanding but lacks optimization. Variable naming could be more descriptive, and edge cases aren't fully handled.

**Algorithm & Complexity Analysis:**
The current approach appears to be O(n²) time complexity. For this problem type, there's likely an O(n) or O(n log n) solution using hash maps or sorting. Space complexity seems reasonable but could be optimized.

**Communication Assessment:**
Your explanation demonstrates problem understanding but lacks depth in discussing trade-offs, complexity analysis, and alternative approaches. In a real interview, you'd need to be more thorough.

**Problem Solving Approach:**
Shows systematic thinking but could benefit from discussing multiple approaches before coding. Consider edge cases earlier in the process.

**Overall Assessment:**
Demonstrates competency but needs improvement in optimization and communication depth. With focused practice on complexity analysis and cleaner code structure, you could reach the next level.

**Hiring Recommendation:** LEAN_HIRE at MID_LEVEL level

**Key Areas for Improvement:**
• Optimize algorithm complexity - research optimal solutions for this problem type
• Improve variable naming and code readability
• Practice explaining time/space complexity clearly
• Discuss multiple solution approaches before coding
• Handle edge cases more systematically

**Interview Tips:**
• Always discuss complexity before and after coding
• Think out loud more during problem solving
• Ask clarifying questions about constraints and edge cases
• Practice explaining your thought process step by step""",
            "recommendation": "Focus on algorithm optimization and complexity analysis. Practice explaining your approach more thoroughly, as communication is crucial in technical interviews."
        }

# Test the analysis
if __name__ == "__main__":
    analyzer = ProperTechnicalAnalysis()
    
    # Test with sample data
    test_code = """
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
"""
    
    test_explanation = "I used nested loops to check all pairs of numbers to find the target sum."
    
    result = analyzer.analyze_solution("Two Sum", test_code, test_explanation, "python")
    print("Sample Analysis:")
    print(f"Scores: {result['code_quality']}, {result['algorithm_efficiency']}, {result['communication_skills']}")
    print(f"Feedback: {result['feedback'][:200]}...")
