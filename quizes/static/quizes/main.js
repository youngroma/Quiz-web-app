console.log("hello")

const modalButtons = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')
const startButton = document.getElementById('start-button')
const url = "quiz/"


modalButtons.forEach(Button => Button.addEventListener('click', ()=> {
    const pk = Button.getAttribute('data-pk')
    const user = Button.getAttribute('data-user')
    const name = Button.getAttribute('data-name')
    const description = Button.getAttribute('data-description')
    const topic = Button.getAttribute('data-topic')
    const numQuestions = Button.getAttribute('data-questions')
    const difficulty = Button.getAttribute('data-difficulty')
    const time = Button.getAttribute('data-time')
    const scoreToPass = Button.getAttribute('data-pass')

    modalBody.innerHTML = `
        <div class="mb-3">
            <h5>Are you sure you want to begin "<b>${name}</b>"</h5>
        </div>

        <div class="text-muted">
            <p>${description}</p>
            <ul>
                <p>Autor: <b>${user}</b></p>
                <p>Difficulty: <b>${difficulty}</b></p>
                <p>Number of questions: <b>${numQuestions}</b></p>
                <p>Time available: <b>${time} minutes</b></p>
                <p>Score needed to pass: <b>${scoreToPass} %</b></p>
            </ul>
        </div>
        `

    startButton.addEventListener('click', ()=>{
        window.location.href = url + pk // Takes the user to the detail view
    })
}))