class CodeInterviewAI {
  constructor() {
    this.initializeApp()
    this.setupEventListeners()
    this.loadUserData()
  }

  initializeApp() {
    this.userId = localStorage.getItem("userId") || this.generateUserId()
    this.currentProblem = null
    this.mediaRecorder = null
    this.audioChunks = []
    this.isRecording = false
    this.audioStream = null

    console.log("CodeInterview AI initialized")
  }

  generateUserId() {
    const userId = "user_" + Math.random().toString(36).substr(2, 9)
    localStorage.setItem("userId", userId)
    return userId
  }

  setupEventListeners() {
    document.addEventListener("DOMContentLoaded", () => {
      this.setupNavigation()
      this.setupProblemFilters()
      this.setupCodeEditor()
      this.setupVoiceRecorder()
      this.setupSubmissionHandler()
    })
  }

  setupNavigation() {
    const currentPath = window.location.pathname
    const navLinks = document.querySelectorAll(".nav-link")

    navLinks.forEach((link) => {
      if (link.getAttribute("href") === currentPath) {
        link.classList.add("active")
      }
    })
  }

  setupProblemFilters() {
    const difficultySelect = document.getElementById("difficulty-select")
    const languageSelect = document.getElementById("language-select")
    const topicSelect = document.getElementById("topic-select")

    if (difficultySelect) {
      difficultySelect.addEventListener("change", this.filterProblems.bind(this))
    }
    if (languageSelect) {
      languageSelect.addEventListener("change", this.updateCodeTemplate.bind(this))
    }
    if (topicSelect) {
      topicSelect.addEventListener("change", this.filterProblems.bind(this))
    }
  }

  setupCodeEditor() {
    const codeInput = document.getElementById("code-input")
    if (codeInput) {
      codeInput.addEventListener("input", this.handleCodeChange.bind(this))
      this.setupCodeHighlighting(codeInput)
    }
  }

  setupCodeHighlighting(editor) {
    editor.addEventListener("keydown", (e) => {
      if (e.key === "Tab") {
        e.preventDefault()
        const start = editor.selectionStart
        const end = editor.selectionEnd
        editor.value = editor.value.substring(0, start) + "    " + editor.value.substring(end)
        editor.selectionStart = editor.selectionEnd = start + 4
      }
    })
  }

  setupVoiceRecorder() {
    const recordBtn = document.getElementById("record-btn")
    if (recordBtn) {
      recordBtn.addEventListener("click", this.toggleRecording.bind(this))
    }
  }

  async toggleRecording() {
    const recordBtn = document.getElementById("record-btn")
    const status = document.getElementById("recorder-status")
    const recorder = document.getElementById("voice-recorder")

    if (!this.isRecording) {
      try {
        // Request microphone access with better constraints
        this.audioStream = await navigator.mediaDevices.getUserMedia({ 
          audio: {
            echoCancellation: true,
            noiseSuppression: true,
            sampleRate: 16000,
            channelCount: 1
          }
        })
        
        // Use proper MIME type for AssemblyAI
        const options = {
          mimeType: 'audio/webm;codecs=opus'
        }
        
        // Fallback for browsers that don't support webm
        if (!MediaRecorder.isTypeSupported(options.mimeType)) {
          options.mimeType = 'audio/wav'
        }
        
        this.mediaRecorder = new MediaRecorder(this.audioStream, options)
        this.audioChunks = [] // Reset chunks

        this.mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            this.audioChunks.push(event.data)
          }
        }

        this.mediaRecorder.onstop = async () => {
          await this.processAudioRecording()
          // Stop all tracks to release microphone
          this.audioStream.getTracks().forEach(track => track.stop())
        }

        this.mediaRecorder.onerror = (event) => {
          console.error("MediaRecorder error:", event.error)
          this.showToast("Recording error occurred", "error")
          this.resetRecordingState()
        }

        this.mediaRecorder.start(1000) // Collect data every second
        this.isRecording = true
        
        if (recordBtn) {
          recordBtn.classList.add("recording")
          recordBtn.textContent = "⏹️ Stop"
        }
        if (recorder) {
          recorder.classList.add("recording")
        }
        if (status) {
          status.textContent = "Recording... Click to stop"
        }
        
      } catch (error) {
        console.error("Error accessing microphone:", error)
        let errorMessage = "Microphone access denied"
        
        if (error.name === 'NotAllowedError') {
          errorMessage = "Please allow microphone access and try again"
        } else if (error.name === 'NotFoundError') {
          errorMessage = "No microphone found"
        } else if (error.name === 'NotReadableError') {
          errorMessage = "Microphone is being used by another application"
        }
        
        this.showToast(errorMessage, "error")
        this.resetRecordingState()
      }
    } else {
      this.stopRecording()
    }
  }

  stopRecording() {
    if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
      this.mediaRecorder.stop()
    }
    this.isRecording = false
    
    const recordBtn = document.getElementById("record-btn")
    const recorder = document.getElementById("voice-recorder")
    const status = document.getElementById("recorder-status")
    
    if (recordBtn) {
      recordBtn.classList.remove("recording")
      recordBtn.textContent = "🎤 Record"
    }
    if (recorder) {
      recorder.classList.remove("recording")
    }
    if (status) {
      status.textContent = "Processing audio..."
    }
  }

  resetRecordingState() {
    this.isRecording = false
    const recordBtn = document.getElementById("record-btn")
    const recorder = document.getElementById("voice-recorder")
    const status = document.getElementById("recorder-status")
    
    if (recordBtn) {
      recordBtn.classList.remove("recording")
      recordBtn.textContent = "🎤 Record"
    }
    if (recorder) {
      recorder.classList.remove("recording")
    }
    if (status) {
      status.textContent = "Click to explain your approach"
    }
  }

  async processAudioRecording() {
    if (this.audioChunks.length === 0) {
      this.showToast("No audio recorded. Please try again.", "error")
      this.resetRecordingState()
      return
    }

    try {
      // Create blob with proper MIME type
      const mimeType = this.mediaRecorder.mimeType || 'audio/webm'
      const audioBlob = new Blob(this.audioChunks, { type: mimeType })
      
      // Check if blob has content
      if (audioBlob.size === 0) {
        throw new Error("Empty audio recording")
      }

      console.log(`Audio blob created: ${audioBlob.size} bytes, type: ${mimeType}`)

      const formData = new FormData()
      formData.append("audio", audioBlob, "recording.webm")
      formData.append("user_id", this.userId)

      const status = document.getElementById("recorder-status")
      if (status) {
        status.textContent = "Transcribing audio..."
      }

      const response = await fetch("/api/voice-explanation", {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(`HTTP ${response.status}: ${errorText}`)
      }

      const result = await response.json()
      
      if (result.success && result.transcription) {
        this.displayTranscription(result.transcription)
        this.showToast("Audio transcribed successfully!", "success")
      } else {
        throw new Error(result.error || "Transcription failed")
      }
      
    } catch (error) {
      console.error("Transcription failed:", error)
      let errorMessage = "Transcription failed. Please try again."
      
      if (error.message.includes("HTTP 413")) {
        errorMessage = "Audio file too large. Please record a shorter message."
      } else if (error.message.includes("HTTP 400")) {
        errorMessage = "Invalid audio format. Please try again."
      } else if (error.message.includes("HTTP 401")) {
        errorMessage = "Authentication failed. Please check API configuration."
      }
      
      this.showToast(errorMessage, "error")
    } finally {
      this.audioChunks = []
      this.resetRecordingState()
    }
  }

  displayTranscription(transcription) {
    const transcriptionDiv = document.getElementById("transcription")
    const textExplanation = document.getElementById("text-explanation")

    if (transcriptionDiv) {
      transcriptionDiv.innerHTML = `<strong>Transcription:</strong> ${transcription}`
      transcriptionDiv.classList.remove("hidden")
    }

    if (textExplanation) {
      // Append to existing text or replace if empty
      const currentText = textExplanation.value.trim()
      if (currentText) {
        textExplanation.value = currentText + "\n\n" + transcription
      } else {
        textExplanation.value = transcription
      }
      
      // Focus and scroll to end
      textExplanation.focus()
      textExplanation.scrollTop = textExplanation.scrollHeight
    }
  }

  setupSubmissionHandler() {
    const submitBtn = document.getElementById("submit-solution")
    if (submitBtn) {
      submitBtn.addEventListener("click", this.submitSolution.bind(this))
    }
  }

  async submitSolution() {
    const code = document.getElementById("code-input")?.value
    const explanation = document.getElementById("text-explanation")?.value
    const language = document.getElementById("language-select")?.value || "python"

    if (!code?.trim()) {
      this.showToast("Please write your solution first", "error")
      return
    }

    if (!explanation?.trim()) {
      this.showToast("Please explain your approach", "error")
      return
    }

    const submitBtn = document.getElementById("submit-solution")
    const originalText = submitBtn.innerHTML
    submitBtn.innerHTML = '<div class="loading"></div> Analyzing...'
    submitBtn.disabled = true

    try {
      const response = await fetch("/api/submit-solution", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          problem_id: this.getCurrentProblemId(),
          code: code,
          explanation: explanation,
          language: language,
          user_id: this.userId
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }

      const result = await response.json()

      if (result.success) {
        this.displayAnalysis(result.analysis)
        this.showToast("Solution submitted successfully!", "success")
        this.updateUserStats()
      } else {
        throw new Error(result.error || "Submission failed")
      }
    } catch (error) {
      console.error("Submission error:", error)
      this.showToast("Submission failed. Please try again.", "error")
    } finally {
      submitBtn.innerHTML = originalText
      submitBtn.disabled = false
    }
  }

  getCurrentProblemId() {
    const urlParams = new URLSearchParams(window.location.search)
    return urlParams.get("problem_id") || "default_problem"
  }

  displayAnalysis(analysis) {
    const panel = document.getElementById("analysis-panel")
    const content = document.getElementById("analysis-content")

    if (!panel || !content) return

    const scores = {
      "Code Quality": analysis.code_quality || 0,
      "Algorithm Efficiency": analysis.algorithm_efficiency || 0,
      Communication: analysis.communication_skills || 0,
      "Problem Solving": analysis.problem_solving || 0,
      "Interview Readiness": analysis.interview_readiness || 0,
    }

    let scoresHtml = '<div class="score-grid">'
    for (const [category, score] of Object.entries(scores)) {
      const scoreClass = score >= 80 ? "score-excellent" : score >= 60 ? "score-good" : "score-needs-work"
      scoresHtml += `
                <div class="score-item">
                    <div class="score-value ${scoreClass}">${score}</div>
                    <div class="score-label">${category}</div>
                </div>
            `
    }
    scoresHtml += "</div>"

    content.innerHTML = `
            ${scoresHtml}
            <div class="mt-6">
                <h4 class="mb-4">Detailed Feedback:</h4>
                <div class="bg-dark-elevated p-4 rounded-lg">
                    ${analysis.feedback || "Analysis completed successfully."}
                </div>
            </div>
            <div class="mt-4">
                <strong>Recommendation:</strong> 
                <span class="text-primary-yellow">${analysis.recommendation || "Keep practicing!"}</span>
            </div>
        `

    panel.classList.remove("hidden")
    panel.scrollIntoView({ behavior: "smooth" })
  }

  async filterProblems() {
    const difficulty = document.getElementById("difficulty-select")?.value || "all"
    const topic = document.getElementById("topic-select")?.value || "all"
    const language = document.getElementById("language-select")?.value || "python"

    try {
      const response = await fetch(`/api/problems?difficulty=${difficulty}&topic=${topic}&language=${language}`)
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }
      
      const problems = await response.json()
      this.displayProblems(problems)
    } catch (error) {
      console.error("Error fetching problems:", error)
      this.showToast("Failed to load problems", "error")
    }
  }

  displayProblems(problems) {
    const container = document.getElementById("problems-container")
    if (!container) return

    if (!Array.isArray(problems) || problems.length === 0) {
      container.innerHTML = '<div class="text-center text-secondary">No problems found</div>'
      return
    }

    container.innerHTML = problems
      .map(
        (problem) => `
            <div class="problem-card">
                <div class="problem-header">
                    <h3 class="problem-title">${problem.title || 'Untitled Problem'}</h3>
                    <div class="problem-meta">
                        <span class="difficulty-badge difficulty-${problem.difficulty || 'medium'}">${problem.difficulty || 'Medium'}</span>
                        <span class="text-secondary">${problem.category || 'General'}</span>
                    </div>
                </div>
                <div class="problem-content">
                    <p class="mb-4">${problem.description || 'No description available'}</p>
                    <a href="/practice?problem_id=${problem.id}" class="btn btn-primary">Solve Problem</a>
                </div>
            </div>
        `,
      )
      .join("")
  }

  updateCodeTemplate() {
    const language = document.getElementById("language-select")?.value
    const codeInput = document.getElementById("code-input")

    if (!codeInput || !language) return

    const templates = {
      python: `def solution(nums):
    # Your solution here
    pass`,
      javascript: `function solution(nums) {
    // Your solution here
}`,
      java: `public class Solution {
    public int[] solution(int[] nums) {
        // Your solution here
        return new int[]{};
    }
}`,
      cpp: `class Solution {
public:
    vector<int> solution(vector<int>& nums) {
        // Your solution here
        return {};
    }
};`,
    }

    codeInput.value = templates[language] || templates.python
  }

  handleCodeChange(event) {
    const code = event.target.value
    localStorage.setItem("currentCode", code)
  }

  loadUserData() {
    const savedCode = localStorage.getItem("currentCode")
    const codeInput = document.getElementById("code-input")

    if (savedCode && codeInput && !codeInput.value.trim()) {
      codeInput.value = savedCode
    }
  }

  async updateUserStats() {
    try {
      const response = await fetch("/api/user-stats", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: this.userId }),
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }

      const stats = await response.json()
      this.updateStatsDisplay(stats)
    } catch (error) {
      console.error("Failed to update user stats:", error)
    }
  }

  updateStatsDisplay(stats) {
    const statElements = {
      "problems-solved": stats.problems_solved,
      "total-submissions": stats.total_submissions,
      "average-score": stats.average_score,
      streak: stats.streak,
    }

    for (const [id, value] of Object.entries(statElements)) {
      const element = document.getElementById(id)
      if (element) {
        element.textContent = value || 0
      }
    }
  }

  showToast(message, type = "info") {
    // Remove existing toasts
    const existingToasts = document.querySelectorAll('.toast')
    existingToasts.forEach(toast => toast.remove())

    const toast = document.createElement("div")
    toast.className = `toast toast-${type} show`
    toast.textContent = message
    
    // Add some basic styling if not defined in CSS
    toast.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 12px 24px;
      border-radius: 6px;
      color: white;
      font-weight: 500;
      z-index: 10000;
      max-width: 400px;
      word-wrap: break-word;
      transition: all 0.3s ease;
    `
    
    // Set background color based on type
    const colors = {
      success: '#10b981',
      error: '#ef4444',
      warning: '#f59e0b',
      info: '#3b82f6'
    }
    toast.style.backgroundColor = colors[type] || colors.info

    document.body.appendChild(toast)

    setTimeout(() => {
      toast.style.opacity = '0'
      toast.style.transform = 'translateX(100%)'
      setTimeout(() => {
        if (document.body.contains(toast)) {
          document.body.removeChild(toast)
        }
      }, 300)
    }, 4000)
  }

  async getSimilarProblems(problemId) {
    try {
      const response = await fetch(`/api/similar-problems?problem_id=${problemId}`)
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }
      
      const similar = await response.json()
      return similar
    } catch (error) {
      console.error("Failed to get similar problems:", error)
      return []
    }
  }
}

// Initialize the app
const app = new CodeInterviewAI()

// Theme toggle functionality
document.addEventListener("DOMContentLoaded", () => {
  const themeToggle = document.getElementById("theme-toggle")
  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      document.body.classList.toggle("light-theme")
      localStorage.setItem("theme", document.body.classList.contains("light-theme") ? "light" : "dark")
    })
  }

  // Load saved theme
  const savedTheme = localStorage.getItem("theme")
  if (savedTheme === "light") {
    document.body.classList.add("light-theme")
  }
})

// Save code before page unload
window.addEventListener("beforeunload", () => {
  const codeInput = document.getElementById("code-input")
  if (codeInput) {
    localStorage.setItem("currentCode", codeInput.value)
  }
})

// Handle page visibility changes to stop recording if page becomes hidden
document.addEventListener("visibilitychange", () => {
  if (document.hidden && app.isRecording) {
    app.stopRecording()
  }
})
