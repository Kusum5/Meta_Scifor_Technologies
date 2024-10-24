import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores.chroma import Chroma
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import ChatOpenAI, OpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import (List, Tuple)

# from langchain import HuggingFaceHub
from langchain_community.embeddings import HuggingFaceEmbeddings

# from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

load_dotenv()


class CVAnalyzer():
    async def get_pdf_text(self, pdf_docs) -> str:
        text = ""
        pdf_reader = PdfReader(pdf_docs)

        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

    async def create_docs(self, cvs_list: list, unique_id):
        docs = []
        for file_obj in cvs_list:
            file_details = file_obj.get_file_details()
            chunks = await self.get_pdf_text(file_obj.cv)

            docs.append(Document(
                page_content=chunks,
                metadata={
                    "name": file_details.get('name'),
                    "id": file_details.get('id'),
                    "type": file_details.get('type'),
                    "size": file_details.get('size'),
                    "unique_id": unique_id
                }
            ))
        return docs

    async def create_embeddings_load_data(self) -> OpenAIEmbeddings:
        embeddings = OpenAIEmbeddings()
        # embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-V2")
        return embeddings

    async def get_vectorstore(self, documents, embeddings):
        vectorstore = Chroma.from_documents(documents=documents, embedding=embeddings)
        return vectorstore

    async def similar_docs(self, query, number_response_docs, vectorstore, unique_id) -> List[Tuple[Document, float]]:
        return vectorstore.similarity_search_with_score(query, int(number_response_docs), {"unique_id": unique_id})

    async def get_summary(self, current_doc):
        # llm = HuggingFaceHub(repo_id="bigscience/bloom", model_kwargs={"temperature":1e-10})
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
        # llm = OpenAI(temperature=0)
        chain = load_summarize_chain(llm, chain_type="map_reduce")
        summary = chain.run(current_doc)
        return summary

    async def get_summary_str(self, text):
        # llm = HuggingFaceHub(repo_id="bigscience/bloom", model_kwargs={"temperature":1e-10})
        # llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
        llm = OpenAI(temperature=0)
        chain = load_summarize_chain(llm, chain_type="map_reduce")
        summary = chain.run(Document(page_content=text))
        return summary


class ChatPDFLangchain():
    # ----------------------- Load Documents ------------------------------------
    async def get_pdf_text(self, pdf_docs) -> str:
        text = ""
        pdf_reader = PdfReader(pdf_docs)

        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

    async def create_docs(self, pdf_list: list, unique_id: str) -> list:
        docs = []

        for file_obj in pdf_list:
            file_details = file_obj.get_file_details()
            chunks = await self.get_pdf_text(file_obj.file)
            docs.append(Document(
                page_content=chunks,
                metadata={
                    "name": file_details.get('name'),
                    "id": file_details.get('id'),
                    "type": file_details.get('type'),
                    "size": file_details.get('size'),
                    "unique_id": unique_id}))
        return docs

    # ---------------Transform(Split) Documents -----------------------------
    async def split_docs(self, documents, chunk_size=2000, chunk_overlap=250):
        text_splitter = RecursiveCharacterTextSplitter(separators=["\n", "\n\n", "\n\n\n"], chunk_size=chunk_size,
                                                       chunk_overlap=chunk_overlap)  # Break large documents in few chunks
        docs = text_splitter.split_documents(documents=documents)
        # docs = text_splitter.split_text(document_in_text_formatat)
        # chunks = text_splitter.create_documents(docs)
        return docs

    async def get_embeddings(self):
        load_dotenv()
        # embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl") 
        # embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        return embeddings

    async def get_vectorstore(self, documents, embeddings):
        return Chroma.from_documents(documents=documents, embedding=embeddings)

    async def get_similar_docs(self, db, query, k=2):
        return db.similarity_search(query, k=k)

    async def get_chain(self):
        load_dotenv()
        # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
        # llm = HuggingFaceHub(repo_id="bigscience/bloom",model_kwargs={"temperature":1e-10})
        # llm = HuggingFaceHub(repo_id="google/flan-t5-large",model_kwargs={"temperature":0.9})

        template = """You are a virtual assistant. Your name is Pixie. Use the information provided in the context to answer the question at the end. Always respond in an assertive and formal manner. If you do not know or cannot find the answer to the question, simply say that you could not find the answer and ask the client to rephrase the question, do not attempt to make up an answer. After each answer, always ask if they would like to know anything else.
            {context}
            {chat_history}
            Question: {question}
            Helpful Response:
        """
        QA_CHAIN_PROMPT = PromptTemplate(
            input_variables=["context", "chat_history", "question"],
            template=template
        )
        return load_qa_chain(
            llm=OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-3.5-turbo-instruct"),
            chain_type="stuff",
            memory=ConversationBufferMemory(memory_key="chat_history", input_key="question"),
            prompt=QA_CHAIN_PROMPT
        )

    async def get_answer(self, chain, query, relevant_docs):
        response = chain.invoke({"input_documents": relevant_docs, "question": query}, return_only_outputs=True)[
            "output_text"]
        # print(chain.memory.buffer)
        return response
