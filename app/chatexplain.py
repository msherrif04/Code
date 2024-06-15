import os
from langchain_groq import ChatGroq

from dotenv import load_dotenv, find_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# load_dotenv(".env")

# Using Groq model
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# print(GROQ_API_KEY)
# model = ChatGroq(model="llama3-8b-8192", api_key=GROQ_API_KEY)


# GROQ_API_KEY
api_key = "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"


## Prompt template
def get_explanation(question, answer, api_key):
    model = ChatGroq(model="llama3-8b-8192", api_key=api_key)

    template = """You are a helpful scientist and mathematician assistant. You explain scientific and mathematical answers to questions
    to the best of your ability in a clear and concise manner maintaining a scientific and educational tone.
    If you don't know the answer, simply state that you don't know instead of attempting to fabricate a response.
    User question: {user_question}
    Answer: {answer}
  """
    prompt = ChatPromptTemplate.from_template(template)

    llm = model

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"user_question": question, "answer": answer})


question = """

"""


answer = """

  """
