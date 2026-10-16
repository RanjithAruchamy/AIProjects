# memory_chat.py
# Block 10 — Version 2: memory that builds ITSELF (nothing hardcoded).
# A real chat loop: after every turn we append the new question + answer.
# Run:  python memory_chat.py   (type 'quit' to stop)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly assistant. Use the conversation history to stay consistent."),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])
chain = prompt | model | StrOutputParser()

history = []                                   # ① starts EMPTY — nothing hardcoded

print("Chat with the bot (type 'quit' to exit).")
while True:                                     # ② one loop = one chat turn
    question = input("You: ")
    if question.strip().lower() in {"quit", "exit"}:
        break

    answer = chain.invoke(
        {"history": history, "question": question})   # ③ send history so far
    print("Bot:", answer)

    history.append(HumanMessage(question))      # ④ remember what you said...
    history.append(AIMessage(answer))           # ⑤ ...and what it replied
    # print(f"   (history now has {len(history)} messages)")
