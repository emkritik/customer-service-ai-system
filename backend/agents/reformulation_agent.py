import anthropic
import os

class ReformulationAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def reformulate(self, question):
        """Reformulate customer question into optimized search query"""

        prompt = f"""You are a banking query reformulation specialist. Your job is to analyze customer service questions and reformulate them into optimized search queries for a knowledge base.

Given this question from a customer service representative:
"{question}"

Analyze what the customer's actual problem is and what banking policies/procedures are relevant.

Respond with ONLY a concise, optimized search query (5-15 words) that will retrieve the most relevant policy documents. No explanation, just the query.

Example:
Input: "Customer is yelling that money was stolen from his card"
Output: "unauthorized credit card charge dispute process refund policy"

Your optimized search query:"""

        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=100,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        reformulated = message.content[0].text.strip()

        return {
            "original_question": question,
            "reformulated_query": reformulated,
            "reasoning": "Identified key intent and optimized for knowledge base search"
        }
