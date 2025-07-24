# PlainTest - Simple Online Exam Platform

A minimalistic black and white exam platform where students can take tests anonymously and download their results.

## 🎯 Features

- ✅ **Anonymous Testing** - No login required for students
- ✅ **Multiple Choice Questions** - Easy to answer format
- ✅ **Timer Functionality** - Auto-submit when time expires
- ✅ **Instant Results** - Immediate scoring and feedback
- ✅ **Downloadable Reports** - HTML format for easy printing
- ✅ **Responsive Design** - Works on desktop and mobile
- ✅ **Clean UI** - Black and white minimalistic design

## 📁 File Structure

```
PlainTest/
├── index.html          # Main student portal
├── script.js           # Core exam functionality (add your exams here)
├── styles.css          # Styling (black & white theme)
├── deploy_to_git.py    # Git deployment automation
├── tests/
│   └── test_template.html  # Template for creating new exams
└── README.md           # This file
```

## 🚀 Quick Start

1. **Add exam data**: Edit `script.js` to add your exam questions
2. **Open the platform**: Open `index.html` in a web browser
3. **Take a test**: Click on any available exam
4. **Complete exam**: Answer questions and submit
5. **Download results**: Get your detailed report

## 📝 Available Tests

**No tests are currently configured.** Follow the instructions below to add your own exams.

## 🔧 Adding New Tests

### Method 1: Add to script.js (Recommended)
1. Open `script.js`
2. Add your exam data to the `examData` object following this format:

```javascript
const examData = {
    'your-exam-id': {
        title: 'Your Exam Title',
        duration: 30, // minutes
        questions: [
            {
                question: "Your question here?",
                options: ["Option A", "Option B", "Option C", "Option D"],
                correct: 0 // Index of correct answer (0=A, 1=B, 2=C, 3=D)
            }
            // Add more questions...
        ]
    }
    // Add more exams...
};
```

3. Add an exam item to `index.html` in the exam-list section:

```html
<div class="exam-item" data-exam="your-exam-id">
    <h3>Your Exam Title</h3>
    <p>Duration: 30 minutes | Questions: 10</p>
    <button onclick="startExam('your-exam-id')">Start Exam</button>
</div>
```

### Method 2: Create Standalone Test Files
1. Copy `tests/test_template.html`
2. Rename it to your test name
3. Replace all `[PLACEHOLDERS]` with your content
4. Add the exam data in the script section
5. Add a link in main `index.html`:

```html
<div class="exam-item">
    <h3>Your Test Name</h3>
    <p>Duration: X minutes | Questions: Y</p>
    <button onclick="window.open('tests/your-test.html', '_blank')">Start Test</button>
</div>
```

## 🚀 Git Deployment

Use the automated Git deployment script:

```bash
python deploy_to_git.py
```

### Features:
- ✅ **Auto Git Setup** - Initializes repository if needed
- ✅ **Smart Commits** - Auto-generates commit messages
- ✅ **Remote Management** - Handles GitHub and other Git providers
- ✅ **Conflict Resolution** - Handles merge conflicts
- ✅ **Quick Deploy** - One-click deployment option

### Deployment Options:
1. **Full Deploy** - Interactive with custom commit message
2. **Quick Deploy** - Auto-commit with timestamp
3. **Status Check** - View current Git status

## 🎨 Customization

### Styling
- Edit `styles.css` to change colors or layout
- Current theme: Black text on white background
- Minimalistic design with clean borders

### Functionality
- Edit `script.js` to modify exam behavior
- Add new question types or features
- Customize timer or scoring logic

## 📱 Browser Compatibility

- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers

## 🛡️ Security Notes

- No server-side processing required
- Client-side only (can be hosted anywhere)
- No personal data collected
- Anonymous usage

## 📊 Example Usage

1. **Student visits website**
2. **Selects "Advanced Physics Test"**
3. **Reads instructions and starts exam**
4. **Answers 25 questions within 60 minutes**
5. **Submits exam automatically or manually**
6. **Views instant results with explanations**
7. **Downloads HTML report for records**

## 🔧 Technical Details

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Storage**: LocalStorage for temporary data
- **Timer**: JavaScript setInterval
- **Reports**: Blob API for file downloads
- **Deployment**: Python script for Git automation

## 🎯 Perfect For

- Educational institutions
- Online training programs
- Self-assessment tools
- Quick knowledge testing
- Practice exams

---

**Simple. Clean. Effective.**

No complex setup, no databases, no user management - just pure exam functionality that works everywhere.
