const task = document.getElementById("task");

const level = document.getElementById("level");

const inputText = document.getElementById("input-text");

const weeks = document.getElementById("weeks");

const weeksContainer =
    document.getElementById("weeks-container");

const levelContainer =
    document.getElementById("level-container");

const generateButton =
    document.getElementById("generate-btn");

const clearButton =
    document.getElementById("clear-btn");

const result =
    document.getElementById("result");

const status =
    document.getElementById("status");


// --------------------------------------------------
// TASK CHANGE
// --------------------------------------------------

task.addEventListener("change", () => {

    const selectedTask = task.value;

    if (selectedTask === "qa") {

        levelContainer.classList.add("hidden");

    } else {

        levelContainer.classList.remove("hidden");

    }


    if (selectedTask === "learn") {

        weeksContainer.classList.remove("hidden");

    } else {

        weeksContainer.classList.add("hidden");

    }


    updatePlaceholder();

});


function updatePlaceholder() {

    const selectedTask = task.value;

    if (selectedTask === "qa") {

        inputText.placeholder =
            "Example: What is photosynthesis?";

    }

    else if (selectedTask === "explain") {

        inputText.placeholder =
            "Example: Explain Artificial Intelligence";

    }

    else if (selectedTask === "quiz") {

        inputText.placeholder =
            "Paste the topic or study material here...";

    }

    else if (selectedTask === "summarize") {

        inputText.placeholder =
            "Paste a long paragraph here...";

    }

    else if (selectedTask === "learn") {

        inputText.placeholder =
            "Example: Python Programming";

    }
}


// --------------------------------------------------
// GENERATE
// --------------------------------------------------

generateButton.addEventListener(
    "click",
    generateContent
);


async function generateContent() {

    const selectedTask = task.value;

    const text = inputText.value.trim();

    if (!text) {

        showError(
            "Please enter some text first."
        );

        return;
    }


    status.textContent =
        "Generating... Please wait.";

    result.innerHTML = "";


    let endpoint = "";

    let body = {};


    if (selectedTask === "qa") {

        endpoint = "/qa";

        body = {
            question: text
        };

    }


    else if (selectedTask === "explain") {

        endpoint = "/explain";

        body = {
            topic: text,
            level: level.value
        };

    }


    else if (selectedTask === "quiz") {

        endpoint = "/quiz";

        body = {
            text: text,
            level: level.value,
            count: 3
        };

    }


    else if (selectedTask === "summarize") {

        endpoint = "/summarize";

        body = {
            text: text,
            max_words: 150
        };

    }


    else if (selectedTask === "learn") {

        endpoint =
            "/learn/recommendations";

        body = {
            topic: text,
            level: level.value,
            weeks: Number(weeks.value)
        };

    }


    try {

        const response = await fetch(
            endpoint,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(body)
            }
        );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Something went wrong."
            );
        }


        status.textContent =
            "Completed successfully.";


        renderResult(
            selectedTask,
            data
        );

    }

    catch (error) {

        showError(
            error.message
        );

    }
}


// --------------------------------------------------
// RESULT RENDERING
// --------------------------------------------------

function renderResult(
    selectedTask,
    data
) {

    if (selectedTask === "qa") {

        result.innerHTML = `
            <h3>Answer</h3>
            <p>${formatText(data.answer)}</p>
        `;

    }


    else if (selectedTask === "explain") {

        result.innerHTML = `
            <h3>Explanation</h3>
            <p>${formatText(data.answer)}</p>
        `;

    }


    else if (selectedTask === "summarize") {

        result.innerHTML = `
            <h3>Summary</h3>
            <p>${formatText(data.summary)}</p>
        `;

    }


    else if (selectedTask === "quiz") {

        renderQuiz(data.quiz);

    }


    else if (selectedTask === "learn") {

        renderLearningPath(
            data.recommendations
        );

    }
}


// --------------------------------------------------
// QUIZ
// --------------------------------------------------

function renderQuiz(quiz) {

    if (!quiz || quiz.length === 0) {

        result.innerHTML =
            "<p>No quiz questions were generated.</p>";

        return;
    }


    let html =
        "<h3>Quiz</h3>";


    quiz.forEach(
        (question, questionIndex) => {

            html += `
                <div class="quiz-question">

                    <strong>
                        ${questionIndex + 1}.
                        ${escapeHtml(question.question)}
                    </strong>
            `;


            question.options.forEach(
                option => {

                    html += `
                        <button
                            class="quiz-option"
                            onclick="checkAnswer(
                                this,
                                '${escapeAttribute(option)}',
                                '${escapeAttribute(question.answer)}',
                                '${escapeAttribute(question.explanation)}'
                            )"
                        >
                            ${escapeHtml(option)}
                        </button>
                    `;

                }
            );


            html += `
                </div>
            `;

        }
    );


    result.innerHTML = html;
}


// --------------------------------------------------
// CHECK ANSWER
// --------------------------------------------------

function checkAnswer(
    button,
    selected,
    correct,
    explanation
) {

    const parent =
        button.parentElement;


    const buttons =
        parent.querySelectorAll(
            ".quiz-option"
        );


    buttons.forEach(
        item => {
            item.disabled = true;
        }
    );


    if (selected === correct) {

        button.classList.add(
            "correct"
        );

        const message =
            document.createElement("p");

        message.innerHTML =
            `<strong>Correct!</strong>
             ${escapeHtml(explanation)}`;

        parent.appendChild(message);

    }

    else {

        button.classList.add(
            "incorrect"
        );


        buttons.forEach(
            item => {

                if (
                    item.textContent.trim()
                    === correct
                ) {

                    item.classList.add(
                        "correct"
                    );

                }

            }
        );


        const message =
            document.createElement("p");

        message.innerHTML =
            `<strong>Correct answer:</strong>
             ${escapeHtml(correct)}
             <br>
             ${escapeHtml(explanation)}`;

        parent.appendChild(message);
    }
}


// --------------------------------------------------
// LEARNING PATH
// --------------------------------------------------

function renderLearningPath(
    recommendations
) {

    if (
        !recommendations ||
        recommendations.length === 0
    ) {

        result.innerHTML =
            "<p>No learning path was generated.</p>";

        return;
    }


    let html =
        "<h3>Personalized Learning Path</h3>";


    recommendations.forEach(
        week => {

            html += `
                <div class="learning-week">

                    <h3>
                        Week ${week.week}:
                        ${escapeHtml(week.title || "")}
                    </h3>

                    <strong>Topics</strong>

                    <ul>
            `;


            (week.topics || []).forEach(
                topic => {

                    html += `
                        <li>
                            ${escapeHtml(topic)}
                        </li>
                    `;

                }
            );


            html += `
                    </ul>

                    <strong>Activities</strong>

                    <ul>
            `;


            (week.activities || []).forEach(
                activity => {

                    html += `
                        <li>
                            ${escapeHtml(activity)}
                        </li>
                    `;

                }
            );


            html += `
                    </ul>

                    <strong>Resources</strong>

                    <ul>
            `;


            (week.resources || []).forEach(
                resource => {

                    html += `
                        <li>
                            ${escapeHtml(resource)}
                        </li>
                    `;

                }
            );


            html += `
                    </ul>

                </div>
            `;

        }
    );


    result.innerHTML = html;
}


// --------------------------------------------------
// CLEAR
// --------------------------------------------------

clearButton.addEventListener(
    "click",
    () => {

        inputText.value = "";

        result.innerHTML = "";

        status.textContent = "";

    }
);


// --------------------------------------------------
// ERROR
// --------------------------------------------------

function showError(message) {

    status.textContent = "";

    result.innerHTML = `
        <div class="error">
            ${escapeHtml(message)}
        </div>
    `;
}


// --------------------------------------------------
// TEXT FORMAT
// --------------------------------------------------

function formatText(text) {

    if (!text) {
        return "";
    }

    return escapeHtml(text)
        .replace(/\n/g, "<br>");
}


// --------------------------------------------------
// SECURITY HELPERS
// --------------------------------------------------

function escapeHtml(value) {

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


function escapeAttribute(value) {

    return String(value)
        .replace(/\\/g, "\\\\")
        .replace(/'/g, "\\'")
        .replace(/"/g, "&quot;")
        .replace(/\n/g, "\\n");
}


// --------------------------------------------------
// INITIAL SETUP
// --------------------------------------------------

updatePlaceholder();

task.dispatchEvent(
    new Event("change")
);