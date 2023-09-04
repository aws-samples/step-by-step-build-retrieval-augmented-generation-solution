from query_embedding import query
from langchain.chains import LLMChain
from langchain import OpenAI
import json
from langchain import PromptTemplate

def build_chain():

    llm = OpenAI(openai_api_key=API_KEY, batch_size=5, temperature=0.2, max_tokens=30000)

    prompt_template = """

Please help me to find the answer, based on the retrieved information and the user input question.

user input question:
{question}

retrieved information
{retrieved_information}

Please ensure the answer are relevant to retrieved information, if you could not find the answer, please wrote #IDONTKNOW exact words without any extrat word.

"""

    prompt = PromptTemplate(
        template=prompt_template, input_variables=["retrieved_information", "question"]
    )

    llmchain = LLMChain(llm=llm, prompt=prompt)
    return llmchain

def run_chain(chain, question: str, history=[]):
    result = query(question)
    sources = list(map(lambda x: "page " + x[0], result))
    #source_documents = list(map(lambda x: x[1], result))
    source_documents = result
    answer = chain.run({
        'question': question,
        'retrieved_information': source_documents
    })
    
    result = {
        'answer': answer,
        'source_documents': source_documents,
        'sources': sources
    }
    return result

if __name__ == "__main__":
    llmchain = build_chain()
    Question = "What are the names of executive directors and senior management?"
    result = run_chain(llmchain, Question)
    print(result)
