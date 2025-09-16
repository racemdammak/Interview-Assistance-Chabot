import asyncio
import websockets
import groq
import os
from dotenv import load_dotenv
import nest_asyncio
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from processing.retriever import retrieve_chunks  

# Load environment variables
load_dotenv()
nest_asyncio.apply()


class Agent:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Agent, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        self.client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))
        self.system_prompt_template = None
        self.retriever = retrieve_chunks

    def getSystemPrompt(self, top_k_chunks, user_question):
        return f"""
            You are a domain-specific chatbot assistant trained to help users prepare for job interviews, 
            answer career-related questions, and provide guidance on resume, skills, and interview techniques.
              Your job is to provide clear, accurate, and actionable answers using only the provided context.

            Follow these rules:
            - Only answer using the information in the context below.
            - If the context does not contain enough information to answer the question, respond with:
              "I’m sorry, the context provided does not contain enough detail about this topic."
            - Explain concepts in simple, professional language, suitable for job seekers preparing for interviews.
            - Include details, examples, and actionable steps if available.
            - Avoid vague summaries. Be specific and informative.
            - Format your response using Markdown.
            - Bold any sources mentioned.
            - Keep responses concise but actionable.

            Context Chunks (Extracted Passages):
            {top_k_chunks}

            User Question:
            {user_question}

            Your Answer (Based on Context Only):
            """
    
    async def handle_connection(self, websocket, path=None):
        print("🤖 Agent ready for queries.")
        messages = [{"role": "system", "content": "You are a helpful interviews assistant."}]

        while True:
            try:
                message = await websocket.recv()
                print(f"📨 Received from client: {message}")

                # Retrieve context
                relevant_chunks = self.retriever(message, top_k=5)
                if not relevant_chunks:
                    await websocket.send("I’m sorry, the context provided does not contain enough detail about this topic.")
                    continue

                # Prepare context string
                context = "\n\n".join([
                    f"[Source: {os.path.basename(chunk['source'])}]\n{chunk['text']}"
                    for chunk in relevant_chunks
                ])

                # Prepare system prompt
                system_prompt = self.getSystemPrompt(context, message)

                # Add messages
                messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": message})

                # Get LLM response safely
                try:
                    response = self.client.chat.completions.create(
                        model=os.getenv("GROQ_MODEL"),
                        messages=messages
                    )
                    llm_reply = response.choices[0].message.content
                except Exception as e:
                    llm_reply = f"❌ Error generating response from LLM: {e}"

                # Send reply to client
                await websocket.send(llm_reply)
                print(f"🤖 Sent: {llm_reply[:80]}...")

                # Append assistant response
                messages.append({"role": "assistant", "content": llm_reply})

            except websockets.ConnectionClosed:
                print("❌ Client disconnected.")
                break
            except Exception as e:
                print(f"⚠️ Unexpected error: {e}")
                await websocket.send(f"❌ Unexpected error: {e}")

    async def start_server(self):
        async with websockets.serve(
            self.handle_connection,
            "localhost",
            8765,
            ping_interval=3600,
            ping_timeout=3600
        ):
            print("WebSocket server started on ws://localhost:8765")
            await asyncio.Future()


if __name__ == "__main__":
    agent = Agent()
    asyncio.run(agent.start_server())
