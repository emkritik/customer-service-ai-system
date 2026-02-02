import anthropic
import os
import re

class ValidationAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def validate(self, original_question, answer, context):
        """Validate answer quality and return confidence score"""

        prompt = f"""You are a quality assurance agent evaluating customer service answers.

Original Question: {original_question}

Answer Provided:
{answer}

Source Context:
{context}

Evaluate this answer on:
1. Accuracy - Does it match the source documents?
2. Relevance - Does it address the question?
3. Completeness - Are important details included?

Respond with ONLY a confidence score from 0-100 (just the number).

Examples:
- Perfect answer with all details: 95
- Good answer, minor details missing: 80
- Acceptable but vague: 65
- Partially relevant: 40
- Wrong or off-topic: 15

Confidence score:"""

        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=50,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = message.content[0].text.strip()

        # Extract number from response
        match = re.search(r'\d+', response_text)
        confidence_score = int(match.group()) if match else 50

        # Ensure score is in range
        confidence_score = max(0, min(100, confidence_score))

        return {
            "confidence_score": confidence_score,
            "evaluation": "Answer validated against source material"
        }
