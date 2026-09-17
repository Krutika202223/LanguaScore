const API_BASE = 'http://127.0.0.1:8001/api';
const form = document.querySelector('#assessment-form');
const questionsContainer = document.querySelector('#questions-container');
const writingInput = document.querySelector('#writing-response');
const writingPrompt = document.querySelector('#writing-prompt');
const wordCount = document.querySelector('#word-count');
const errorBox = document.querySelector('#form-error');
const language = sessionStorage.getItem('languaScoreLanguage') || 'English';
let questions = [];

document.querySelector('#assessment-language').textContent = `${language} assessment`;
document.querySelector('#assessment-title').textContent = `Show us your ${language}.`;

async function loadQuestions() {
  try {
    const response = await fetch(`${API_BASE}/assessment/questions?language=${encodeURIComponent(language)}`);
    if (!response.ok) {
      const details = await response.json().catch(() => ({}));
      throw new Error(details.detail || `Question service returned ${response.status}`);
    }
    const assessment = await response.json();
    if (!Array.isArray(assessment.questions) || assessment.questions.length === 0) {
      throw new Error(`No questions are available for ${language}.`);
    }
    questions = assessment.questions;
    writingPrompt.textContent = assessment.writing_question?.prompt || 'Write 100-150 words about your daily routine.';
    questionsContainer.innerHTML = questions.map((question, index) => `
      <article class="question-card"><span class="question-number">${String(index + 1).padStart(2, '0')} / ${question.topic}</span>
      <p class="question-prompt">${question.prompt}</p><div class="options">
      ${Object.entries(question.options).map(([key, text]) => `<label class="option-label"><input type="radio" name="${question.id}" value="${key}"><span><strong>${key}.</strong> ${text}</span></label>`).join('')}
      </div></article>`).join('');
    updateProgress();
  } catch (error) {
    questionsContainer.innerHTML = '<p class="form-error">Questions could not be loaded.</p>';
    writingPrompt.textContent = 'Writing question unavailable. Please refresh after starting the FastAPI server.';
    errorBox.textContent = `${error.message} Start the FastAPI server, then refresh this page.`;
  }
}

function updateProgress() {
  const answered = questions.filter((question) => document.querySelector(`input[name="${question.id}"]:checked`)).length;
  const writingWords = writingInput.value.trim().split(/\s+/).filter(Boolean).length;
  const total = questions.length + 1;
  const completed = answered + (writingWords >= 100 ? 1 : 0);
  document.querySelector('#progress-count').textContent = `${completed} / ${total}`;
  document.querySelector('#progress-bar').style.width = `${completed / total * 100}%`;
  wordCount.textContent = `${writingWords} word${writingWords === 1 ? '' : 's'}`;
}

document.addEventListener('change', updateProgress);
writingInput.addEventListener('input', updateProgress);
form.addEventListener('submit', async (event) => {
  event.preventDefault(); errorBox.textContent = '';
  const grammarAnswers = questions.map((question) => ({ question_id: question.id, answer: document.querySelector(`input[name="${question.id}"]:checked`)?.value || '' }));
  if (grammarAnswers.some((item) => !item.answer)) { errorBox.textContent = 'Please answer every grammar question before submitting.'; return; }
  const writingWords = writingInput.value.trim().split(/\s+/).filter(Boolean).length;
  if (writingWords < 100 || writingWords > 150) { errorBox.textContent = 'Please write between 100 and 150 words for the writing task.'; return; }
  const button = document.querySelector('#submit-button'); button.disabled = true; button.textContent = 'Assessing...';
  try {
    const response = await fetch(`${API_BASE}/assessment`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ language, grammar_answers: grammarAnswers, writing_response: writingInput.value }) });
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail?.[0]?.msg || result.detail || 'Assessment failed');
    sessionStorage.setItem('languaScoreResult', JSON.stringify(result)); window.location.href = 'result.html';
  } catch (error) { errorBox.textContent = error.message; button.disabled = false; button.innerHTML = 'Submit assessment <span aria-hidden="true">&#8594;</span>'; }
});
loadQuestions();
