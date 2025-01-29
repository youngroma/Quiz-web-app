console.log('hilo');
const url = window.location.href;
const quizQuestionBox = document.getElementById('quiz-question-box');
const prevButton = document.getElementById('prev-question');
const nextButton = document.getElementById('next-question');
const submitButton = document.getElementById('submit-quiz');
const timerBox = document.getElementById('timer-box')

let questions = [];
let currentQuestionIndex = 0;
let userAnswers = {};


const activateTimer = (time) => {
    if (time.toString().length < 2) {
        timerBox.innerHTML = `<b>0${time}:00</b>`
    } else {
    timerBox.innerHTML = `<b>${time}:00</b>`
    }

    let minutes = time - 1
    let seconds = 60
    let displaySeconds
    let displayMinutes

    const timer = setInterval(()=>{
        seconds --
        if (seconds < 0) {
            seconds = 59
            minutes --
        }
        if(minutes.toString().length < 2) {
            displayMinutes = '0'+minutes
        } else {
            displayMinutes = minutes
        }
        if (seconds.toString().length < 2) {
            displaySeconds = '0' + seconds
        } else {
            displaySeconds = seconds
        }
        if (minutes === 0 && seconds === 0) {
            timerBox.innerHTML = "<b>00:00</b>"
            setTimeout(()=>{
                clearInterval(timer)
                alert('time over')
                sendData()
            }, 500)

        }

        timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`

    }, 1000)

}

$.ajax({
    type: 'GET',
    url: `${url}data/`,
    success: function (response) {
        console.log('Received questions:', response.data);
        questions = response.data;
        displayQuestion(currentQuestionIndex);
        activateTimer(response.time);
    },
    error: function (error) {
        console.error('Error loading questions:', error);
    }
});

const displayQuestion = (index) => {
    quizQuestionBox.innerHTML = '';

    if (!questions[index] || !Object.keys(questions[index]).length) {
        console.error("No question data available for index:", index);
        quizQuestionBox.innerHTML = `<p>Error: Question not found.</p>`;
        return;
    }

    const questionObj = questions[index];
    const questionText = Object.keys(questionObj)[0];
    const answers = questionObj[questionText];

    if (!Array.isArray(answers) || answers.length === 0) {
        console.error(`No answers found for question: "${questionText}"`);
        quizQuestionBox.innerHTML = `
            <div>
                <h5>${questionText}</h5>
                <p>Error: No answers available.</p>
            </div>`;
        return;
    }

    console.log("Rendering question:", questionText);
    console.log("Answers:", answers);


    quizQuestionBox.innerHTML = `
        <div class="mb-3">
            <h5>${questionText}</h5>
        </div>
        <div class="answers-container">
        ${answers.map(answer => `
            <div class="answer-block">
                <input type="radio" class="ans" id="${encodeURIComponent(questionText)}-${encodeURIComponent(answer)}" name="${encodeURIComponent(questionText)}" value="${answer}">
                <label for="${encodeURIComponent(questionText)}-${encodeURIComponent(answer)}" class="answer-label">${answer}</label>
            </div>`).join('')}
        </div>
    `;


    console.log("Generated HTML:", quizQuestionBox.innerHTML);

    answers.forEach((answer) => {
    const radioInput = document.getElementById(`${encodeURIComponent(questionText)}-${encodeURIComponent(answer)}`);
    const answerBlock = radioInput?.parentElement;

    if (!radioInput || !answerBlock) {
        console.error("Not found elements for:", answer);
        return;
    }

    if (userAnswers[questionText] === answer) {
        answerBlock.classList.add('selected');
        radioInput.checked = true;
    }

    answerBlock.addEventListener('click', () => {
        console.log(`Selected answer: ${answer}`);
        document
            .querySelectorAll(`input[name="${questionText}"]`)
            .forEach((input) => input.parentElement.classList.remove('selected'));

        answerBlock.classList.add('selected');
        radioInput.checked = true;

        userAnswers[questionText] = answer;
        console.log("Updated user's answers:", userAnswers);
    });
});

const updateNavigationButtons = () => {
    prevButton.disabled = currentQuestionIndex === 0;
    nextButton.classList.toggle('d-none', currentQuestionIndex === questions.length - 1);
    submitButton.classList.toggle('d-none', currentQuestionIndex !== questions.length - 1);
};

const saveAnswer = () => {
    const elements = [...document.getElementsByClassName('ans')];
    elements.forEach((el) => {
        if (el.checked) {
            userAnswers[el.name] = el.value;
        }
    });
    console.log('Updated userAnswers:', userAnswers);
};

prevButton.addEventListener('click', (e) => {
    e.preventDefault();
    saveAnswer();
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        displayQuestion(currentQuestionIndex);
    }
});

nextButton.addEventListener('click', (e) => {
    e.preventDefault();
    saveAnswer();
    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        displayQuestion(currentQuestionIndex);
    }
});

submitButton.addEventListener('click', (e) => {
    e.preventDefault();
    saveAnswer();
    console.log('Submitting data:', userAnswers);

    const data = { csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value };
    Object.assign(data, userAnswers);

    console.log('Final data to send:', data);

    $.ajax({
        type: 'POST',
        url: `${url}save/`,
        data: data,
        success: function (response) {
            console.log('Server response:', response);
            window.location.href = response.redirect_url;
        },
        error: function (error) {
            console.error('Error submitting answers:', error);
        }
    });
});}

const questionBlocks = document.querySelectorAll('.question-block');
const answerBlocks = document.querySelectorAll('.answer-block');

questionBlocks.forEach(block => {
    if (block.style.display === 'none') {
        block.style.display = 'block';
    }
});
