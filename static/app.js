const analyzeBtn = document.getElementById('analyzeBtn');
const logInput = document.getElementById('logInput');
const feedContainer = document.getElementById('feedContainer');
const diagnosisCard = document.getElementById('diagnosisCard');
const rootCauseText = document.getElementById('rootCauseText');
const confidenceBar = document.getElementById('confidenceBar');
const confidenceValue = document.getElementById('confidenceValue');
const actionCard = document.getElementById('actionCard');
const fixCode = document.getElementById('fixCode');
const validationStatus = document.getElementById('validationStatus');

analyzeBtn.addEventListener('click', async () => {
    const logVal = logInput.value.trim();
    if (!logVal) return;

    // Reset UI
    feedContainer.innerHTML = '';
    diagnosisCard.classList.add('hidden');
    actionCard.classList.add('hidden');
    addFeedItem('Initialization', 'Sending logs to Neural Core...', 'system');

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ log_content: logVal })
        });

        const data = await response.json();

        // Replay history as feed
        if (data.history) {
            data.history.forEach((entry, index) => {
                setTimeout(() => {
                    let type = 'system';
                    if (entry.includes('Analyzed')) type = 'agent';
                    if (entry.incudes && entry.includes('Queried')) type = 'tool';

                    addFeedItem('Agent Activity', entry, type);
                }, index * 500); // Stagger for effect
            });
        }

        // Show Result after delay
        setTimeout(() => {
            showDiagnosis(data);
        }, (data.history ? data.history.length : 1) * 500 + 500);

    } catch (e) {
        addFeedItem('Error', 'Connection failed: ' + e.message, 'error');
    }
});

function addFeedItem(title, message, type) {
    const div = document.createElement('div');
    div.className = `feed-item ${type}`;
    div.innerHTML = `<strong>[${title}]</strong> ${message}`;
    feedContainer.appendChild(div);
    feedContainer.scrollTop = feedContainer.scrollHeight;
}

function showDiagnosis(data) {
    diagnosisCard.classList.remove('hidden');

    // Typewriter effect for root cause
    let i = 0;
    rootCauseText.innerHTML = '';
    const text = data.root_cause_analysis || "No diagnosis found.";
    const typeWriter = setInterval(() => {
        if (i < text.length) {
            rootCauseText.innerHTML += text.charAt(i);
            i++;
        } else {
            clearInterval(typeWriter);

            // Show Action Card if fix exists
            if (data.proposed_fix_diff) {
                actionCard.classList.remove('hidden');
                fixCode.textContent = data.proposed_fix_diff;
                validationStatus.textContent = `Validation Status: ${data.validation_status}`;
                validationStatus.style.color = data.validation_status === 'PASSED' || data.validation_status === 'EXECUTED' ? '#00ff9d' : '#ff0055';
            }
        }
    }, 20);

    // Confidence
    const conf = (data.confidence_score || 0) * 100;
    confidenceBar.style.width = `${conf}%`;
    confidenceValue.textContent = `${conf}%`;
}
