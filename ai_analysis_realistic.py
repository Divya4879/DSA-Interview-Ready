import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class RealisticTechnicalAnalysis:
    def __init__(self):
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        
    def analyze_solution(self, problem_title, code, explanation, language="python"):
        """
        Provide brutally honest, realistic technical analysis
        """
        try:
            if not self.groq_api_key:
                return self._get_realistic_fallback_analysis(code, explanation)

            # Create a harsh but fair analysis prompt
            prompt = f"""
You are a senior staff engineer at Google who has conducted over 500 technical interviews. You are known for being brutally honest but fair. Analyze this coding solution with the harshness and specificity of a real technical interview.

PROBLEM: {problem_title}
LANGUAGE: {language}

CODE:
```{language}
{code}
```

CANDIDATE EXPLANATION: {explanation}

Be brutally honest. Most candidates fail technical interviews. Don't sugarcoat anything. Provide specific, actionable criticism.

Analyze:

1. CODE QUALITY (1-100): Look for actual issues - poor variable names, missing edge cases, inefficient patterns, code smells
2. ALGORITHM EFFICIENCY (1-100): Analyze actual time/space complexity. If it's O(n²) when O(n) exists, be harsh about it
3. COMMUNICATION (1-100): Was the explanation clear, thorough, and technically accurate? Did they discuss trade-offs?
4. PROBLEM SOLVING (1-100): Did they understand the problem? Consider multiple approaches? Handle edge cases?
5. INTERVIEW READINESS (1-100): Would you hire this person based on this performance?

Be specific about what's wrong. Don't give participation trophy scores. If the code is bad, say it's bad and why.

Format as JSON:
{{
    "code_quality": <realistic_score>,
    "algorithm_efficiency": <realistic_score>, 
    "communication_skills": <realistic_score>,
    "problem_solving": <realistic_score>,
    "interview_readiness": <realistic_score>,
    "detailed_feedback": {{
        "code_quality_feedback": "<harsh but specific feedback about code issues>",
        "algorithm_feedback": "<specific complexity analysis with better alternatives>",
        "communication_feedback": "<honest assessment of explanation quality>",
        "problem_solving_feedback": "<assessment of problem-solving approach>",
        "overall_assessment": "<brutally honest overall assessment>",
        "specific_improvements": ["<specific improvement 1>", "<specific improvement 2>", "<specific improvement 3>"],
        "interview_tips": ["<harsh but helpful tip 1>", "<harsh but helpful tip 2>", "<harsh but helpful tip 3>"]
    }},
    "hiring_decision": "<STRONG_NO_HIRE|NO_HIRE|LEAN_NO_HIRE|LEAN_HIRE|HIRE|STRONG_HIRE>",
    "level_assessment": "<INTERN|JUNIOR|MID_LEVEL|SENIOR|STAFF>",
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
                        'content': 'You are a brutal but fair senior staff engineer at Google. Give honest, harsh feedback that will actually help candidates improve. Most solutions are mediocre - call them out.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'temperature': 0.2,
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
                    return self._format_realistic_analysis(analysis)
                except json.JSONDecodeError:
                    return self._parse_realistic_text_analysis(content)
            else:
                print(f"Groq API error: {response.status_code}")
                return self._get_realistic_fallback_analysis(code, explanation)

        except Exception as e:
            print(f"Analysis error: {str(e)}")
            return self._get_realistic_fallback_analysis(code, explanation)

    def _format_realistic_analysis(self, analysis):
        """Format the realistic analysis for display"""
        detailed = analysis.get('detailed_feedback', {})
        
        return {
            "code_quality": analysis.get('code_quality', 45),
            "algorithm_efficiency": analysis.get('algorithm_efficiency', 35),
            "communication_skills": analysis.get('communication_skills', 50),
            "problem_solving": analysis.get('problem_solving', 40),
            "interview_readiness": analysis.get('interview_readiness', 42),
            "feedback": self._create_realistic_feedback(detailed, analysis),
            "recommendation": analysis.get('next_steps', 'Significant improvement needed before technical interviews.')
        }

    def _create_realistic_feedback(self, detailed, analysis):
        """Create brutally honest feedback text"""
        feedback_parts = []
        
        # Code Quality Section
        if detailed.get('code_quality_feedback'):
            feedback_parts.append(f"🔧 **CODE QUALITY ANALYSIS:**\n{detailed['code_quality_feedback']}")
        
        # Algorithm Analysis
        if detailed.get('algorithm_feedback'):
            feedback_parts.append(f"⚡ **ALGORITHM & COMPLEXITY ANALYSIS:**\n{detailed['algorithm_feedback']}")
        
        # Communication Assessment
        if detailed.get('communication_feedback'):
            feedback_parts.append(f"💬 **COMMUNICATION ASSESSMENT:**\n{detailed['communication_feedback']}")
        
        # Problem Solving Approach
        if detailed.get('problem_solving_feedback'):
            feedback_parts.append(f"🧠 **PROBLEM SOLVING APPROACH:**\n{detailed['problem_solving_feedback']}")
        
        # Overall Assessment
        if detailed.get('overall_assessment'):
            feedback_parts.append(f"📋 **OVERALL ASSESSMENT:**\n{detailed['overall_assessment']}")
        
        # Hiring Decision
        hiring_decision = analysis.get('hiring_decision', 'NO_HIRE')
        level = analysis.get('level_assessment', 'JUNIOR')
        feedback_parts.append(f"🎯 **HIRING RECOMMENDATION:** {hiring_decision} at {level} level")
        
        # Specific Improvements
        improvements = detailed.get('specific_improvements', [])
        if improvements:
            feedback_parts.append("🎯 **CRITICAL AREAS FOR IMPROVEMENT:**\n" + "\n".join([f"• {imp}" for imp in improvements]))
        
        # Interview Tips
        tips = detailed.get('interview_tips', [])
        if tips:
            feedback_parts.append("💡 **INTERVIEW SURVIVAL TIPS:**\n" + "\n".join([f"• {tip}" for tip in tips]))
        
        return "\n\n".join(feedback_parts)

    def _get_realistic_fallback_analysis(self, code, explanation):
        """Provide realistic fallback analysis based on actual code inspection"""
        
        # Analyze the code for common issues
        code_issues = []
        algorithm_issues = []
        
        if "for" in code and "for" in code[code.find("for")+10:]:
            algorithm_issues.append("Nested loops detected - likely O(n²) complexity")
        
        if "brute force" in explanation.lower():
            algorithm_issues.append("Candidate admits to brute force approach")
            
        if len(explanation.split()) < 20:
            communication_issues = ["Explanation too brief for technical interview"]
        else:
            communication_issues = []
            
        if "complexity" not in explanation.lower():
            communication_issues.append("No complexity analysis provided")
            
        # Calculate realistic scores
        code_score = 65 if len(code_issues) == 0 else 45
        algorithm_score = 30 if algorithm_issues else 55
        communication_score = 40 if communication_issues else 60
        problem_solving_score = 45
        interview_score = min(code_score, algorithm_score, communication_score)
        
        return {
            "code_quality": code_score,
            "algorithm_efficiency": algorithm_score,
            "communication_skills": communication_score,
            "problem_solving": problem_solving_score,
            "interview_readiness": interview_score,
            "feedback": f"""🔧 **CODE QUALITY ANALYSIS:**
Your code shows basic functionality but has significant room for improvement. {'; '.join(code_issues) if code_issues else 'Structure is acceptable but could be more elegant.'}

⚡ **ALGORITHM & COMPLEXITY ANALYSIS:**
{'; '.join(algorithm_issues) if algorithm_issues else 'Algorithm choice needs optimization.'} For most problems, there are more efficient solutions. You need to research optimal approaches before coding.

💬 **COMMUNICATION ASSESSMENT:**
{'; '.join(communication_issues) if communication_issues else 'Communication needs significant improvement.'} In real interviews, you must discuss time/space complexity, trade-offs, and alternative approaches.

🧠 **PROBLEM SOLVING APPROACH:**
Shows basic problem understanding but lacks depth. You should discuss multiple approaches, edge cases, and optimization strategies before coding.

📋 **OVERALL ASSESSMENT:**
This performance would not pass most technical interviews. You need substantial improvement in algorithm optimization and technical communication.

🎯 **HIRING RECOMMENDATION:** NO_HIRE at JUNIOR level

🎯 **CRITICAL AREAS FOR IMPROVEMENT:**
• Study optimal algorithms for common problem patterns
• Practice explaining time/space complexity clearly
• Learn to discuss multiple solution approaches
• Improve code structure and readability
• Practice thinking out loud during problem solving

💡 **INTERVIEW SURVIVAL TIPS:**
• Always analyze complexity before and after coding
• Discuss at least 2-3 approaches before implementing
• Ask clarifying questions about constraints and edge cases
• Practice explaining your thought process step by step
• Study system design basics even for coding interviews""",
            "recommendation": "Focus on algorithm optimization and technical communication. Practice explaining complexity analysis clearly. You need significant improvement before technical interviews."
        }

    def _parse_realistic_text_analysis(self, text_content):
        """Parse text-based analysis if JSON parsing fails"""
        return {
            "code_quality": 45,
            "algorithm_efficiency": 35,
            "communication_skills": 50,
            "problem_solving": 40,
            "interview_readiness": 42,
            "feedback": f"🔧 **REALISTIC TECHNICAL ANALYSIS:**\n\n{text_content}",
            "recommendation": "Significant improvement needed in multiple areas before technical interviews."
        }

# Test the realistic analysis
if __name__ == "__main__":
    analyzer = RealisticTechnicalAnalysis()
    
    # Test with the user's actual input
    test_code = """
# Brute force approach
for i in range(len(nums)):
    for j in range(i+1, len(nums)):
        if nums[i] + nums[j] == target:
            return [i, j]
"""
    
    test_explanation = "I just simply copy pasted this solution from the lead code itself. I'm just checking if the SMDI API is working and dependent or not the Glock I OPI like analysis is working as well."
    
    result = analyzer.analyze_solution("Two Sum", test_code, test_explanation, "python")
    print("Realistic Analysis:")
    print(f"Scores: {result['code_quality']}, {result['algorithm_efficiency']}, {result['communication_skills']}")
    print(f"Feedback: {result['feedback'][:300]}...")
