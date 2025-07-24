// PlainTest - Exam Platform JavaScript

// Exam data - Add your exam data here
const examData = {
    // Example structure:
    // 'exam-id': {
    //     title: 'Exam Title',
    //     duration: 30, // minutes
    //     questions: [
    //         {
    //             question: "Your question here?",
    //             options: ["Option A", "Option B", "Option C", "Option D"],
    //             correct: 0 // Index of correct answer (0-3)
    //         }
    //     ]
    // }
};

// Global variables
let currentExam = null;
let currentQuestionIndex = 0;
let userAnswers = [];
let examTimer = null;
let timeRemaining = 0;
let examResults = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Show exam selection by default
    showSection('exam-selection');
});

function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => section.classList.add('hidden'));
    
    // Show the requested section
    document.getElementById(sectionId).classList.remove('hidden');
}

function startExam(examId) {
    currentExam = examData[examId];
    currentQuestionIndex = 0;
    userAnswers = new Array(currentExam.questions.length).fill(null);
    timeRemaining = currentExam.duration * 60; // Convert to seconds
    
    showSection('exam-interface');
    setupExamInterface();
    startTimer();
}

function setupExamInterface() {
    document.getElementById('exam-title').textContent = currentExam.title;
    updateQuestionDisplay();
    updateNavigationButtons();
}

function updateQuestionDisplay() {
    const question = currentExam.questions[currentQuestionIndex];
    
    document.getElementById('question-text').textContent = question.question;
    document.getElementById('question-counter').textContent = 
        `Question ${currentQuestionIndex + 1} of ${currentExam.questions.length}`;
    
    // Create options
    const optionsContainer = document.getElementById('options-container');
    optionsContainer.innerHTML = '';
    
    question.options.forEach((option, index) => {
        const optionDiv = document.createElement('div');
        optionDiv.className = 'option';
        optionDiv.innerHTML = `
            <input type="radio" name="answer" value="${index}" id="option${index}">
            <label for="option${index}">${option}</label>
        `;
        
        // Check if this option was previously selected
        if (userAnswers[currentQuestionIndex] === index) {
            optionDiv.querySelector('input').checked = true;
            optionDiv.classList.add('selected');
        }
        
        optionDiv.addEventListener('click', function() {
            selectOption(index);
        });
        
        optionsContainer.appendChild(optionDiv);
    });
}

function selectOption(optionIndex) {
    userAnswers[currentQuestionIndex] = optionIndex;
    
    // Update visual selection
    const options = document.querySelectorAll('.option');
    options.forEach((option, index) => {
        option.classList.remove('selected');
        if (index === optionIndex) {
            option.classList.add('selected');
            option.querySelector('input').checked = true;
        }
    });
}

function updateNavigationButtons() {
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const submitBtn = document.getElementById('submit-btn');
    
    prevBtn.disabled = currentQuestionIndex === 0;
    
    if (currentQuestionIndex === currentExam.questions.length - 1) {
        nextBtn.classList.add('hidden');
        submitBtn.classList.remove('hidden');
    } else {
        nextBtn.classList.remove('hidden');
        submitBtn.classList.add('hidden');
    }
}

function previousQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        updateQuestionDisplay();
        updateNavigationButtons();
    }
}

function nextQuestion() {
    if (currentQuestionIndex < currentExam.questions.length - 1) {
        currentQuestionIndex++;
        updateQuestionDisplay();
        updateNavigationButtons();
    }
}

function startTimer() {
    examTimer = setInterval(function() {
        timeRemaining--;
        updateTimerDisplay();
        
        if (timeRemaining <= 0) {
            clearInterval(examTimer);
            submitExam();
        }
    }, 1000);
}

function updateTimerDisplay() {
    const minutes = Math.floor(timeRemaining / 60);
    const seconds = timeRemaining % 60;
    document.getElementById('timer').textContent = 
        `Time Remaining: ${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

function submitExam() {
    clearInterval(examTimer);
    
    // Calculate score
    let correctAnswers = 0;
    const results = [];
    
    currentExam.questions.forEach((question, index) => {
        const userAnswer = userAnswers[index];
        const correctAnswer = question.correct;
        const isCorrect = userAnswer === correctAnswer;
        
        if (isCorrect) {
            correctAnswers++;
        }
        
        results.push({
            question: question.question,
            options: question.options,
            userAnswer: userAnswer,
            correctAnswer: correctAnswer,
            isCorrect: isCorrect
        });
    });
    
    displayResults(correctAnswers, results);
}

function displayResults(correctAnswers, results) {
    const totalQuestions = currentExam.questions.length;
    const percentage = Math.round((correctAnswers / totalQuestions) * 100);
    
    // Store results for download
    examResults = {
        examTitle: currentExam.title,
        totalQuestions: totalQuestions,
        correctAnswers: correctAnswers,
        percentage: percentage,
        results: results,
        completedAt: new Date().toLocaleString()
    };
    
    document.getElementById('final-score').textContent = 
        `Score: ${correctAnswers} out of ${totalQuestions}`;
    document.getElementById('score-percentage').textContent = 
        `Percentage: ${percentage}%`;
    
    // Display answer review
    const reviewContent = document.getElementById('review-content');
    reviewContent.innerHTML = '';
    
    results.forEach((result, index) => {
        const reviewItem = document.createElement('div');
        reviewItem.className = `review-item ${result.isCorrect ? 'correct' : 'incorrect'}`;
        
        const userAnswerText = result.userAnswer !== null ? 
            result.options[result.userAnswer] : 'No answer';
        const correctAnswerText = result.options[result.correctAnswer];
        
        reviewItem.innerHTML = `
            <div class="review-question">Question ${index + 1}: ${result.question}</div>
            <div class="review-answer">Your answer: ${userAnswerText}</div>
            <div class="review-answer correct-answer">Correct answer: ${correctAnswerText}</div>
            <div class="answer-status">${result.isCorrect ? 'Correct' : 'Incorrect'}</div>
        `;
        
        reviewContent.appendChild(reviewItem);
    });
    
    showSection('results-section');
}

function backToExams() {
    // Reset exam state
    currentExam = null;
    currentQuestionIndex = 0;
    userAnswers = [];
    examResults = null;
    
    showSection('exam-selection');
}

function downloadReport() {
    if (!examResults) {
        alert('No exam results available to download.');
        return;
    }
    
    // Create HTML content for the report
    let reportHTML = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PlainTest - Exam Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; color: black; }
        .header { text-align: center; border-bottom: 2px solid black; padding-bottom: 20px; margin-bottom: 30px; }
        .score-summary { border: 2px solid black; padding: 20px; margin-bottom: 30px; text-align: center; }
        .question-review { border: 1px solid black; padding: 15px; margin-bottom: 15px; }
        .correct { border-left: 4px solid black; }
        .incorrect { border-left: 4px solid #666; }
        .question { font-weight: bold; margin-bottom: 10px; }
        .answer { margin-bottom: 5px; }
        .status { font-weight: bold; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>PlainTest - Exam Report</h1>
        <h2>${examResults.examTitle}</h2>
        <p>Completed on: ${examResults.completedAt}</p>
    </div>
    
    <div class="score-summary">
        <h2>Final Score: ${examResults.correctAnswers} out of ${examResults.totalQuestions}</h2>
        <h3>Percentage: ${examResults.percentage}%</h3>
    </div>
    
    <h2>Detailed Answer Review</h2>
`;

    examResults.results.forEach((result, index) => {
        const userAnswerText = result.userAnswer !== null ? 
            result.options[result.userAnswer] : 'No answer provided';
        const correctAnswerText = result.options[result.correctAnswer];
        
        reportHTML += `
    <div class="question-review ${result.isCorrect ? 'correct' : 'incorrect'}">
        <div class="question">Question ${index + 1}: ${result.question}</div>
        <div class="answer">Your answer: ${userAnswerText}</div>
        <div class="answer">Correct answer: ${correctAnswerText}</div>
        <div class="status">${result.isCorrect ? 'Correct' : 'Incorrect'}</div>
    </div>
`;
    });

    reportHTML += `
</body>
</html>
`;

    // Create and download the file
    const blob = new Blob([reportHTML], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `PlainTest_${examResults.examTitle.replace(/\s+/g, '_')}_Report_${new Date().toISOString().split('T')[0]}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}
