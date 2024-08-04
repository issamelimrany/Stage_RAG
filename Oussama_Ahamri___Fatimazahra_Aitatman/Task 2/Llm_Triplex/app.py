from langchain_community.document_loaders import PDFPlumberLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
from pypdf import PdfReader
import ollama
import gradio as gr
import os
import json
import ollama

# Assurez-vous que vous avez installé et configuré correctement ollama
ollama.pull("sciphi/triplex")

def triplextract(text, entity_types, predicates):
    input_format = """
        **Entity Types:**
        {entity_types}

        **Predicates:**
        {predicates}

        **Text:**
        {text}
        """

    message = input_format.format(
                entity_types = json.dumps({"entity_types": entity_types}),
                predicates = json.dumps({"predicates": predicates}),
                text = text)

    # Pass the message as a single string
    prompt = message
    output = ollama.generate(model='sciphi/triplex', prompt=prompt)
    return output

if __name__ == "__main__":
    entity_types = ["PERSON", "LOCATION"]
    predicates = ["PROFESSION", "BASED_IN"]

    reader = PdfReader("data/bibliographie.pdf")
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    prediction = triplextract(text, entity_types, predicates)

    response_string = prediction['response'].strip('```json\n').strip()
    response_string = response_string.lstrip('\n')
    response_string = response_string.strip('```')
    response_string = response_string.replace('```', '')
    response_string = response_string.replace("json", "")
    response_json = json.loads(response_string)
    entities_and_triples = response_json['entities_and_triples']
    print(entities_and_triples)

    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(text)

    loader = TextLoader("./output.txt")
    docs = loader.load()

    # Split into chunks
    text_splitter = SemanticChunker(HuggingFaceEmbeddings())
    documents = text_splitter.split_documents(docs)

    # Instantiate the embedding model
    embedder = HuggingFaceEmbeddings()

    # Create the vector store and fill it with embeddings
    vector = FAISS.from_documents(documents, embedder)
    retriever = vector.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    # Define llm
    llm = Ollama(model="sciphi/triplex")

    # Define the prompt
    prompt = """
    1. Use the following pieces of context to answer the question at the end.
    2. If you don't know the answer, just say that "I don't know" but don't make up an answer on your own.\n
    3. Keep the answer crisp and limited to 3,4 sentences.

    Context: {context}

    Question: {question}

    Helpful Answer:"""

    QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt) 

    llm_chain = LLMChain(
                    llm=llm, 
                    prompt=QA_CHAIN_PROMPT, 
                    callbacks=None, 
                    verbose=True)

    document_prompt = PromptTemplate(
        input_variables=["page_content", "source"],
        template="Context:\ncontent:{page_content}\nsource:{source}",
    )

    combine_documents_chain = StuffDocumentsChain(
                    llm_chain=llm_chain,
                    document_variable_name="context",
                    document_prompt=document_prompt,
                    callbacks=None)
                
    qa = RetrievalQA(
                    combine_documents_chain=combine_documents_chain,
                    verbose=True,
                    retriever=retriever,
                    return_source_documents=True)

    def respond(question, history):
        return qa(question)["result"]

    gr.ChatInterface(
        respond,
        chatbot=gr.Chatbot(height=500),
        textbox=gr.Textbox(placeholder="Ask me question related to Document ", container=False, scale=7),
        title="RAG Chatbot",
        examples=["When did Isaac Newton die?", "What were the key events and influences in Einstein's early education?"],
        cache_examples=True,
        retry_btn=None,
    ).launch(share=True)
