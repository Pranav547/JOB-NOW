from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.schema import Document
from uuid import uuid4
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class JobRAGAgent:
    def __init__(self):
        # Load OpenAI embeddings and chat model
        self.embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        self.db = Chroma(
            embedding_function=self.embeddings,
            persist_directory="chroma_db"  # Set to None if no persistence needed
        )
        self.retriever = self.db.as_retriever(search_kwargs={"k": 10})  # More results, smarter LLM filtering
        self.qa = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY),
            retriever=self.retriever,
            chain_type="stuff"
        )

    def ingest_jobs(self, jobs: list):
        """Embed and store job documents with location emphasis."""
        docs = []
        for job in jobs:
            title = job.get('job_title', 'No Title')
            company = job.get('employer_name', 'Unknown Company')
            city = job.get('job_city', '')
            state = job.get('job_state', '')
            country = job.get('job_country', '')
            description = job.get('job_description', '')

            # Strong location inclusion in embedding text
            text = (
                f"Job Title: {title}\n"
                f"Company: {company}\n"
                f"Location: {city}, {state}, {country}\n"
                f"Description: {description}"
            )

            doc = Document(page_content=text, metadata=job, id=str(uuid4()))
            docs.append(doc)

        self.db.add_documents(docs)

    def match(self, skills_query: str, location: str):
        """Use LLM to match jobs based on skills and location."""
        prompt = (
            f"A candidate is looking for jobs in '{location}' and has the following skills: '{skills_query}'.\n"
            f"From the job listings below, recommend top 5 jobs located in or near '{location}' that best match their skills.\n"
            f"For each job, return:\n"
            f"- Job Title\n"
            f"- Company\n"
            f"- Location\n"
            f"- Why it's a good match"
        )
        return self.qa.run(prompt)

    def clear_jobs(self):
        """Clear all stored job documents (reset DB)."""
        self.db.delete_collection()
