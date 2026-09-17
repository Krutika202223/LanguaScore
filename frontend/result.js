const result = JSON.parse(sessionStorage.getItem('languaScoreResult') || 'null');
if (!result) { window.location.href = 'index.html'; } else {
  document.querySelector('#overall-score').innerHTML = `${result.overall_score}<small>%</small>`;
  document.querySelector('#grammar-score').textContent = `${result.grammar_score}%`;
  document.querySelector('#writing-score').textContent = `${result.writing_score}%`;
  document.querySelector('#level').textContent = result.level;
  document.querySelector('#grammar-copy').textContent = `Combined quiz and model score: ${result.grammar_score}%. Model classification: ${result.grammar_category}.`;
  document.querySelector('#writing-copy').textContent = `Your writing response scored ${result.writing_score}% across language-use features.`;
  document.querySelector('#strengths').innerHTML = (result.strengths.length ? result.strengths : ['Keep building consistency across the assessment.']).map((item) => `<li>${item}</li>`).join('');
  document.querySelector('#areas').innerHTML = (result.areas_to_improve.length ? result.areas_to_improve : ['Continue extending your language range.']).map((item) => `<li>${item}</li>`).join('');
  document.querySelector('#recommendations').innerHTML = result.recommendations.map((item) => `<li>${item}</li>`).join('');
  document.querySelector('#model-status').textContent = `Scoring status: ${result.model_status}`;
  document.querySelector('#score-ring').style.background = `conic-gradient(var(--coral) ${result.overall_score * 3.6}deg, #9ed5c4 0deg)`;
}
