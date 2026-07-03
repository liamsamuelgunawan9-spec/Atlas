const API_BASE = "http://127.0.0.1:8000";

const questionInput = document.getElementById("questionInput");
const searchButton = document.getElementById("searchButton");

const loadingSection = document.getElementById("loadingSection");
const progressSection = document.getElementById("progressSection");
const answerSection = document.getElementById("answerSection");

const answerText = document.getElementById("answerText");
const modelBadge = document.getElementById("modelBadge");

const researchId = document.getElementById("researchId");

const planningStatus = document.getElementById("planningStatus");
const searchStatus = document.getElementById("searchStatus");
const writerStatus = document.getElementById("writerStatus");

const copyButton = document.getElementById("copyButton");

function generateResearchId() {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    let id = "#";

    for (let i = 0; i < 8; i++) {
        id += chars[Math.floor(Math.random() * chars.length)];
    }

    return id;
}

function showLoading(show) {
    if (show) {
        loadingSection.classList.remove("hidden");
    } else {
        loadingSection.classList.add("hidden");
    }
}

function resetProgress() {
    planningStatus.textContent = "Waiting...";
    searchStatus.textContent = "Waiting...";
    writerStatus.textContent = "Waiting...";
}

async function research() {

    const question = questionInput.value.trim();

    if (question.length === 0) {
        alert("Please enter a question.");
        return;
    }

    answerSection.classList.add("hidden");
    progressSection.classList.remove("hidden");

    showLoading(true);

    researchId.textContent = generateResearchId();

    resetProgress();

    planningStatus.textContent = "Creating research plan...";

    try {

        // Small delay so the UI feels alive
        await new Promise(resolve => setTimeout(resolve, 400));

        searchStatus.textContent = "Contacting Atlas backend...";

        const response = await fetch(`${API_BASE}/search/`);

        if (!response.ok) {
            throw new Error("Backend returned " + response.status);
        }

        const data = await response.json();

        planningStatus.textContent = "Research plan complete.";
        searchStatus.textContent = "Backend responded.";
        writerStatus.textContent = "Writing final response...";

        await new Promise(resolve => setTimeout(resolve, 300));

        answerText.textContent =
            data.content ??
            data.message ??
            JSON.stringify(data, null, 2);

        modelBadge.textContent = data.model ?? "Backend";

        writerStatus.textContent = "Done.";

        answerSection.classList.remove("hidden");

    } catch (error) {

        answerText.textContent =
            "❌ Failed to contact backend.\n\n" +
            error;

        modelBadge.textContent = "Error";

        writerStatus.textContent = "Failed.";

        answerSection.classList.remove("hidden");

    }

    showLoading(false);

}

questionInput.addEventListener("input", () => {

    questionInput.style.height = "auto";
    questionInput.style.height =
        questionInput.scrollHeight + "px";

});

questionInput.addEventListener("keydown", (event) => {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        research();

    }

});

searchButton.addEventListener("click", research);

copyButton.addEventListener("click", async () => {

    if (!answerText.textContent) return;

    try {

        await navigator.clipboard.writeText(
            answerText.textContent
        );

        copyButton.textContent = "Copied!";

        setTimeout(() => {

            copyButton.textContent = "Copy";

        }, 1500);

    } catch {

        copyButton.textContent = "Failed";

    }

});