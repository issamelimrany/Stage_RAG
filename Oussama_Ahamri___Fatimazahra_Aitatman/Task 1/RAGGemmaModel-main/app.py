import pdfplumber
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOllama
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
import chainlit as cl
import asyncio

@cl.on_chat_start
async def on_chat_start():
    files = None

    while files is None:
        files = await cl.AskFileMessage(
            content="Please upload a PDF file to begin!",
            accept=["application/pdf"],
            max_size_mb=100,
            timeout=180,
        ).send()

    if not files:
        await cl.Message(content="No file uploaded. Please try again.").send()
        return

    file = files[0]
    print(file)

    elements = [cl.Image(name="image", display="inline", path="pic.jpg")]
    msg = cl.Message(content=f"Processing `{file.name}`...", elements=elements)
    await msg.send()

    # Read the PDF file asynchronously
    try:
        pdf_text = await read_pdf_async(file.path)
    except Exception as e:
        await cl.Message(content=f"Failed to read the PDF file: {str(e)}").send()
        return

    # Split the text into chunks
    texts, metadatas = split_text(pdf_text)

    # Create a Chroma vector store
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    docsearch = await cl.make_async(Chroma.from_texts)(texts, embeddings, metadatas=metadatas)

    # Initialize message history for conversation
    message_history = ChatMessageHistory()

    # Memory for conversational context
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        chat_memory=message_history,
        return_messages=True,
    )

    # Create a chain that uses the Chroma vector store
    chain = ConversationalRetrievalChain.from_llm(
        ChatOllama(model="llama3"),
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        memory=memory,
        return_source_documents=True,
    )

    msg.content = f"Processing `{file.name}` done. You can now ask questions!"
    await msg.update()
    cl.user_session.set("chain", chain)

async def read_pdf_async(file_path):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, read_pdf, file_path)

def read_pdf(file_path):
    pdf_text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pdf_text += text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        raise e
    return pdf_text

def split_text(pdf_text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=50)
    texts = text_splitter.split_text(pdf_text)
    metadatas = [{"source": f"{i}-pl"} for i in range(len(texts))]
    return texts, metadatas

@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain")
    cb = cl.AsyncLangchainCallbackHandler()

    res = await chain.ainvoke(message.content, callbacks=[cb])
    answer = res["answer"]
    source_documents = res["source_documents"]

    text_elements = []

    if source_documents:
        for source_idx, source_doc in enumerate(source_documents):
            source_name = f"source_{source_idx}"
            text_elements.append(cl.Text(content=source_doc.page_content, name=source_name))
        source_names = [text_el.name for text_el in text_elements]

        if source_names:
            answer += f"\nSources: {', '.join(source_names)}"
        else:
            answer += "\nNo sources found"

    await cl.Message(content=answer, elements=text_elements).send()
