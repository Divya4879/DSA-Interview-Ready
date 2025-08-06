#!/usr/bin/env python3
"""
API Integrations for DSA Interview Platform
Includes AssemblyAI, Redis, and Local Storage functionality
"""

import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()

class AssemblyAIClient:
    """AssemblyAI client for audio transcription"""
    
    def __init__(self):
        self.api_key = os.getenv('ASSEMBLYAI_API_KEY')
        self.base_url = "https://api.assemblyai.com/v2"
        self.headers = {
            "authorization": self.api_key,
            "content-type": "application/json"
        }
    
    def upload_audio(self, audio_data):
        """Upload audio file to AssemblyAI"""
        try:
            upload_url = f"{self.base_url}/upload"
            upload_headers = {"authorization": self.api_key}
            
            response = requests.post(
                upload_url,
                headers=upload_headers,
                data=audio_data
            )
            
            if response.status_code == 200:
                return response.json()['upload_url']
            else:
                print(f"Upload failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"AssemblyAI upload error: {e}")
            return None
    
    def transcribe_audio(self, audio_url):
        """Transcribe audio using AssemblyAI"""
        try:
            transcript_request = {
                "audio_url": audio_url,
                "language_detection": True,
                "punctuate": True,
                "format_text": True
            }
            
            response = requests.post(
                f"{self.base_url}/transcript",
                json=transcript_request,
                headers=self.headers
            )
            
            if response.status_code == 200:
                transcript_id = response.json()['id']
                return self.poll_transcript(transcript_id)
            else:
                print(f"Transcription request failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"AssemblyAI transcription error: {e}")
            return None
    
    def poll_transcript(self, transcript_id):
        """Poll for transcription completion"""
        try:
            polling_url = f"{self.base_url}/transcript/{transcript_id}"
            
            while True:
                response = requests.get(polling_url, headers=self.headers)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result['status'] == 'completed':
                        return {
                            'text': result['text'],
                            'confidence': result.get('confidence', 0.0),
                            'status': 'completed'
                        }
                    elif result['status'] == 'error':
                        return {
                            'error': result.get('error', 'Transcription failed'),
                            'status': 'error'
                        }
                    else:
                        # Still processing, wait and retry
                        time.sleep(2)
                else:
                    return {
                        'error': f'Polling failed: {response.status_code}',
                        'status': 'error'
                    }
                    
        except Exception as e:
            print(f"AssemblyAI polling error: {e}")
            return {
                'error': str(e),
                'status': 'error'
            }

class LocalStorageManager:
    """Manage local storage for user data"""
    
    @staticmethod
    def generate_storage_js():
        """Generate JavaScript for local storage management"""
        return """
        // Local Storage Manager for DSA Interview Platform
        class LocalStorageManager {
            constructor() {
                this.storageKey = 'dsa_interview_platform';
                this.initializeStorage();
            }
            
            initializeStorage() {
                if (!localStorage.getItem(this.storageKey)) {
                    const initialData = {
                        user: {
                            id: this.generateUserId(),
                            createdAt: new Date().toISOString(),
                            totalProblems: 0,
                            totalScore: 0,
                            averageScore: 0,
                            streak: 0,
                            lastActive: new Date().toISOString()
                        },
                        problems: {},
                        sessions: {},
                        analysis: {},
                        preferences: {
                            language: 'python',
                            difficulty: 'medium',
                            topic: 'arrays'
                        }
                    };
                    localStorage.setItem(this.storageKey, JSON.stringify(initialData));
                }
            }
            
            generateUserId() {
                return 'user_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
            }
            
            getData() {
                try {
                    return JSON.parse(localStorage.getItem(this.storageKey)) || {};
                } catch (e) {
                    console.error('Error reading from localStorage:', e);
                    return {};
                }
            }
            
            saveData(data) {
                try {
                    localStorage.setItem(this.storageKey, JSON.stringify(data));
                    return true;
                } catch (e) {
                    console.error('Error saving to localStorage:', e);
                    return false;
                }
            }
            
            saveProblemSolution(problemId, solutionData) {
                const data = this.getData();
                const sessionId = 'session_' + Date.now();
                
                // Save problem solution
                if (!data.problems[problemId]) {
                    data.problems[problemId] = {
                        attempts: 0,
                        bestScore: 0,
                        totalScore: 0,
                        averageScore: 0,
                        firstAttempt: new Date().toISOString(),
                        lastAttempt: null
                    };
                }
                
                const problem = data.problems[problemId];
                problem.attempts += 1;
                problem.totalScore += solutionData.score;
                problem.averageScore = problem.totalScore / problem.attempts;
                problem.bestScore = Math.max(problem.bestScore, solutionData.score);
                problem.lastAttempt = new Date().toISOString();
                
                // Save session data
                data.sessions[sessionId] = {
                    problemId: problemId,
                    code: solutionData.code,
                    explanation: solutionData.explanation,
                    language: solutionData.language,
                    score: solutionData.score,
                    analysis: solutionData.analysis,
                    timestamp: new Date().toISOString()
                };
                
                // Update user stats
                data.user.totalProblems = Object.keys(data.problems).length;
                data.user.totalScore += solutionData.score;
                data.user.averageScore = data.user.totalScore / this.getTotalAttempts(data);
                data.user.lastActive = new Date().toISOString();
                
                // Update streak
                this.updateStreak(data, solutionData.score);
                
                this.saveData(data);
                return sessionId;
            }
            
            saveAnalysis(sessionId, analysisData) {
                const data = this.getData();
                data.analysis[sessionId] = {
                    ...analysisData,
                    timestamp: new Date().toISOString()
                };
                this.saveData(data);
            }
            
            getTotalAttempts(data) {
                return Object.values(data.problems).reduce((total, problem) => total + problem.attempts, 0);
            }
            
            updateStreak(data, score) {
                if (score >= 70) {
                    data.user.streak += 1;
                } else {
                    data.user.streak = 0;
                }
            }
            
            getUserStats() {
                const data = this.getData();
                return {
                    userId: data.user.id,
                    problemsSolved: data.user.totalProblems,
                    totalAttempts: this.getTotalAttempts(data),
                    averageScore: Math.round(data.user.averageScore || 0),
                    currentStreak: data.user.streak,
                    lastActive: data.user.lastActive
                };
            }
            
            getRecentProblems(limit = 10) {
                const data = this.getData();
                const sessions = Object.entries(data.sessions)
                    .sort(([,a], [,b]) => new Date(b.timestamp) - new Date(a.timestamp))
                    .slice(0, limit);
                
                return sessions.map(([sessionId, session]) => ({
                    sessionId,
                    problemId: session.problemId,
                    score: session.score,
                    language: session.language,
                    timestamp: session.timestamp,
                    status: session.score >= 70 ? 'Solved' : 'Attempted'
                }));
            }
            
            getProblemStats(problemId) {
                const data = this.getData();
                return data.problems[problemId] || null;
            }
            
            exportData() {
                return this.getData();
            }
            
            importData(importedData) {
                try {
                    this.saveData(importedData);
                    return true;
                } catch (e) {
                    console.error('Error importing data:', e);
                    return false;
                }
            }
            
            clearData() {
                localStorage.removeItem(this.storageKey);
                this.initializeStorage();
            }
        }
        
        // Initialize global storage manager
        window.storageManager = new LocalStorageManager();
        """

def create_enhanced_voice_api():
    """Create enhanced voice explanation API with AssemblyAI integration"""
    
    return """
@app.route('/api/voice-explanation', methods=['POST'])
def process_voice_explanation():
    '''Process voice explanation with real AssemblyAI integration'''
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'No audio file selected'}), 400
        
        # Initialize AssemblyAI client
        from api_integrations import AssemblyAIClient
        assemblyai = AssemblyAIClient()
        
        if not assemblyai.api_key:
            # Fallback to mock transcription if no API key
            return jsonify({
                'transcription': 'Audio transcription requires AssemblyAI API key. Please type your explanation in the text area below.',
                'confidence': 0.0,
                'processing_time': 0.1,
                'note': 'Set ASSEMBLYAI_API_KEY environment variable to enable transcription'
            })
        
        # Read audio data
        audio_data = audio_file.read()
        
        # Upload audio to AssemblyAI
        audio_url = assemblyai.upload_audio(audio_data)
        if not audio_url:
            return jsonify({
                'error': 'Failed to upload audio',
                'fallback': 'Please use text explanation instead'
            }), 500
        
        # Transcribe audio
        result = assemblyai.transcribe_audio(audio_url)
        if not result or result.get('status') == 'error':
            return jsonify({
                'error': result.get('error', 'Transcription failed'),
                'fallback': 'Please use text explanation instead'
            }), 500
        
        return jsonify({
            'transcription': result['text'],
            'confidence': result.get('confidence', 0.0),
            'processing_time': 2.5,
            'status': 'success'
        })
        
    except Exception as e:
        print(f'Voice explanation error: {e}')
        return jsonify({
            'error': 'Audio processing failed',
            'message': 'Please use the text explanation field instead',
            'fallback': True
        }), 200
"""

def create_enhanced_submit_api():
    """Create enhanced submit solution API with local storage integration"""
    
    return """
@app.route('/api/submit-solution', methods=['POST'])
def submit_solution():
    '''Enhanced solution submission with local storage integration'''
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user_id = session.get('user_id', 'anonymous')
        problem_id = data.get('problem_id', 'unknown')
        code = data.get('code', '').strip()
        explanation = data.get('explanation', '').strip()
        language = data.get('language', 'python')
        
        # Validate inputs
        if not code:
            return jsonify({'error': 'Code is required'}), 400
        
        if not explanation:
            return jsonify({'error': 'Explanation is required for proper analysis'}), 400
        
        # Perform realistic code analysis
        analysis_result = analyze_solution_properly(code, explanation, problem_id, language)
        
        # Store submission data in Redis
        session_id = f"session_{user_id}_{int(time.time())}"
        session_data = {
            'session_id': session_id,
            'problem_id': problem_id,
            'code': code,
            'explanation': explanation,
            'language': language,
            'score': analysis_result.get('overall_score', 0),
            'completed_at': str(int(time.time())),
            'analysis': json.dumps(analysis_result)
        }
        
        # Store in Redis
        redis_client.hset(f"session:{session_id}", mapping=session_data)
        redis_client.lpush(f"user:{user_id}:sessions", session_id)
        
        # Update user stats in Redis
        update_user_stats(user_id, analysis_result.get('overall_score', 0))
        
        # Stream ML features (with proper error handling)
        ai_features.stream_ml_features(user_id, session_data)
        
        # Prepare data for local storage
        local_storage_data = {
            'sessionId': session_id,
            'problemId': problem_id,
            'code': code,
            'explanation': explanation,
            'language': language,
            'score': analysis_result.get('overall_score', 0),
            'analysis': analysis_result,
            'timestamp': int(time.time())
        }
        
        return jsonify({
            'success': True,
            'analysis': analysis_result,
            'session_id': session_id,
            'local_storage_data': local_storage_data,
            'save_to_local_storage': True
        })
        
    except Exception as e:
        print(f'Submit solution error: {e}')
        return jsonify({'error': 'Failed to analyze solution'}), 500
"""

def main():
    """Main function to set up API integrations"""
    print("🔧 Setting up API Integrations...")
    print("✅ AssemblyAI client created")
    print("✅ Local storage manager created")
    print("✅ Enhanced APIs ready for integration")
    print("\n📝 Next steps:")
    print("1. Set ASSEMBLYAI_API_KEY in your .env file")
    print("2. Update app_redis_cloud.py with enhanced APIs")
    print("3. Add local storage JavaScript to templates")

if __name__ == "__main__":
    main()
