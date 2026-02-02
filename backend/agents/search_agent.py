import anthropic
import os
from rag.vectorstore import search_knowledge_base

class SearchAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def search(self, reformulated_query):
        """Search knowledge base and generate answer"""

        # Retrieve relevant chunks
        results = search_knowledge_base(reformulated_query, k=3)

        # Build context
        context = "\n\n".join([
            f"Source: {doc.metadata['source']} (Page {doc.metadata['page']})\n{doc.page_content}"
            for doc in results
        ])

        # Generate answer using Claude
        prompt = f"""You are a helpful banking customer service assistant. Use the following retrieved information to answer the question accurately and professionally.

Question: {reformulated_query}

Retrieved Information:
{context}

Provide a clear, accurate answer that a customer service representative can use to help their customer. Include specific details like fees, timelines, and phone numbers when available. Be concise but complete.

Answer:"""

        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        answer = message.content[0].text.strip()

        # Extract sources
        sources = [
            {
                "document": doc.metadata['source'],
                "page": doc.metadata['page']
            }
            for doc in results
        ]

        return {
            "query": reformulated_query,
            "answer": answer,
            "sources": sources,
            "context": context
        }
