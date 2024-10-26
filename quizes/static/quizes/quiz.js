console.log('hilo')
const url = window.location.href
const quizBox = document.getElementById('quiz-box')
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')
const timerBox = document.getElementById('timer-box')

const backButton = document.getElementById('back-button')
    backButton.addEventListener('click', ()=>{
        window.location.href = '/'
    })

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
        console.log(response)
        const data = response.data
        data.forEach(el => {
            for (const [question, answers] of Object.entries(el)){
                quizBox.innerHTML  += `
                    <hr>
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>
                `
                answers.forEach(answer=> {
                    quizBox.innerHTML += `
                        <div>
                            <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                            <label for="${question}">${answer}</label>
                        </div>
                    `
                })
            }
        })
        activateTimer(response.time)
    },
    error: function (error) {
        console.log(error)
    }
})

const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

const sendData = () => {

    const elements = [...document.getElementsByClassName('ans')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value;
    elements.forEach(el => {
        if (el.checked) {
            data[el.name] = el.value
        } else {
            if (!data[el.name]){
                data[el.name] = null
            }
        }
    })

   $.ajax({
    type: 'POST',
    url: `${url}save/`,
    data: data,
    success: function(response){
        const results = response.results
        const n_correct_answers = response.score
        const score = response.score.toFixed(2)
        const passed = response.passed
        console.log("Response:", response);
        window.location.href = response.redirect_url;

        // Removes the form
        quizForm.remove()

        let scoreDiv = document.createElement('div')
        // scoreDiv.classList.add(...['container', 'my-auto', 'text-secondary'])


        scoreDiv.innerHTML += `
                           <p> ${passed ? 'Congrats you passed the test!' : 'Sorry, you did not pass the test!'} Your result is ${score} %</p>
                           <p> Answered correctly: ${n_correct_answers}</p>
                           `

        scoreBox.append(scoreDiv)

        results.forEach(res =>{
            let resDiv = document.createElement('div')

            for (const [question, resp] of Object.entries(res)){
                resDiv.innerHTML += question

                const classes = ['container', 'p-3', 'text-light', 'h4']
                resDiv.classList.add(...classes)

                if (resp == 'not answered'){
                    resDiv.innerHTML += ' — Not answered'
                    resDiv.classList.add('bg-danger')
                } else{
                    const answer = resp['answered']
                    const correct = resp['correct_answer']

                    if (answer == correct){
                        resDiv.classList.add('bg-success')
                        resDiv.innerHTML += ` Answered: ${answer}`
                    } else {
                        resDiv.classList.add('bg-danger')
                        resDiv.innerHTML += `| Answered: ${answer}`
                        resDiv.innerHTML += `| Correct answer: ${correct}`
                    }
                }
            }
            resultBox.append(resDiv)
        })
    },
    error: function(error){
        console.log(error)
    }
})
}

quizForm.addEventListener('submit', e=> {
    e.preventDefault()

    sendData()
})