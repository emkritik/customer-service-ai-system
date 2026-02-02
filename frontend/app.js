const API_URL = 'http://localhost:8000';

async function submitQuery() {
    const repName = document.getElementById('repName').value.trim();
    const question = document.getElementById('question').value.trim();

    if (!repName) {
        alert('Please enter your name');
        return;
    }

    if (!question) {
        alert('Please enter a question');
        return;
    }

    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    document.getElementById('submitBtn').disabled = true;

    try {
        const response = await fetch(`${API_URL}/api/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                user_name: repName
            })
        });

        // Check if HTTP request was successful
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        if (result.success) {
            displayResults(result);
        } else {
            alert('Error: ' + (result.message || 'Unknown error occurred'));
        }

    } catch (error) {
        console.error('Error:', error);
        alert('Failed to get answer. Error: ' + error.message + '\n\nMake sure the backend is running with the API key set.');
    } finally {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('submitBtn').disabled = false;
    }
}

function displayResults(result) {
    // Show results section
    document.getElementById('results').style.display = 'block';

    // Display reformulated query
    document.getElementById('reformulatedQuery').textContent = result.reformulated_query;

    // Display answer (convert markdown to clean HTML)
    const answerElement = document.getElementById('answer');
    let formattedAnswer = result.answer
        // Convert headers (###, ##, #) to proper HTML headers
        .replace(/^### (.*?)$/gm, '<h3>$1</h3>')
        .replace(/^## (.*?)$/gm, '<h2>$1</h2>')
        .replace(/^# (.*?)$/gm, '<h1>$1</h1>')
        // Convert bold **text** to <strong>
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        // Convert bullet points
        .replace(/^- (.*?)$/gm, '<li>$1</li>')
        // Convert numbered lists
        .replace(/^\d+\. (.*?)$/gm, '<li>$1</li>')
        // Convert line breaks
        .replace(/\n\n/g, '<br><br>')
        .replace(/\n/g, '<br>');

    // Wrap consecutive <li> items in <ul>
    formattedAnswer = formattedAnswer.replace(/(<li>.*?<\/li>(?:<br>)?)+/gs, match => {
        return '<ul>' + match.replace(/<br>/g, '') + '</ul>';
    });

    answerElement.innerHTML = formattedAnswer;

    // Display confidence badge
    const confidence = result.confidence_score;
    let badgeClass, badgeText;

    if (confidence >= 90) {
        badgeClass = 'badge-green';
        badgeText = `${confidence}% - High Confidence`;
    } else if (confidence >= 70) {
        badgeClass = 'badge-yellow';
        badgeText = `${confidence}% - Medium Confidence`;
    } else {
        badgeClass = 'badge-red';
        badgeText = `${confidence}% - Low Confidence - Verify Carefully`;
    }

    document.getElementById('confidenceBadge').innerHTML =
        `<span class="badge ${badgeClass}">${badgeText}</span>`;

    // Display sources (clickable)
    const sourcesDiv = document.getElementById('sources');
    sourcesDiv.innerHTML = result.sources.map((source, index) => `
        <div class="source-item" onclick="openPDF('${source.document}', ${source.page})" data-source-index="${index}">
            <strong>${source.document}</strong> (Page ${source.page})
            <span style="float: right; color: #1a5490;">📄 Click to open</span>
        </div>
    `).join('');

    // Scroll to results
    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

function openPDF(filename, page) {
    // Open PDF in new tab
    const pdfUrl = `${API_URL}/api/pdf/${filename}#page=${page}`;
    window.open(pdfUrl, '_blank');
}
