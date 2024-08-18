import os
os.environ['USER_AGENT'] = 'myagent'
os.environ["GROQ_API_KEY"] = "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"
# os.environ["OPENAI_API_KEY"] = "sk-proj-wk5OHzAj2Gq7gwfX04myT3BlbkFJNnAhFeKgjMoiHAzRBHqq"
# os.environ['HUGGINGFACEHUB_API_TOKEN'] = "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"

from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from pinecone import Pinecone
from pinecone_text.sparse import BM25Encoder

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.retrievers import PineconeHybridSearchRetriever

from langchain_groq import ChatGroq

import os
from django.conf import settings

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage
import asyncio



class LLMChatPipeline:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialize_pipeline()
        return cls._instance

    def initialize_pipeline(self):
        # Load your LLM chat pipeline here
        pc = Pinecone(api_key="ca8e6a33-7355-453f-ad4b-80c8a1c6a9c7")
        index_name = "traveler-demo-website-vectorstore"

        # connect to index
        pinecone_index = pc.Index(index_name)

        bm25 = BM25Encoder().load(settings.BASE_DIR / 'bm25_traveler_website.json')

        embed_model = HuggingFaceEmbeddings(model_name="Alibaba-NLP/gte-large-en-v1.5", model_kwargs={"trust_remote_code":True} )

        retriever = PineconeHybridSearchRetriever(
            embeddings=embed_model,
            sparse_encoder=bm25, 
            index=pinecone_index, 
            top_k=20, 
            alpha=0.5, 
        )

        llm = ChatGroq(
            model="llama-3.1-70b-versatile", 
            temperature=0, 
            max_tokens=1024, 
            max_retries=2,
            streaming=True
        )

        ### Contextualize question ###
        contextualize_q_system_prompt = """Given a chat history and the latest user question \
        which might reference context in the chat history, formulate a standalone question \
        which can be understood without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is.
        """
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}")
            ]
        )

        history_aware_retriever = create_history_aware_retriever(
            llm, retriever, contextualize_q_prompt
        )


        qa_system_prompt = """You are a highly skilled information retrieval assistant. Use the following pieces of retrieved context to answer the question. \
        If you don't know the answer, just say that you don't know. \
        Provide links to sources provided in the answer. \
        When responding to queries, your responses should be comprehensive and well-organized. For each response: \

            1. Provide Clear Answers \

            2. Include Detailed References: \
                - Include links to sources and any links or sites where there is a mentioned in the answer.
                - Links to Sources: Provide URLs to credible sources where users can verify the information or explore further. \
                - Downloadable Materials: Include links to any relevant downloadable resources if applicable. \
                - Reference Sites: Mention specific websites or platforms that offer additional information. \

            3. Formatting for Readability: \
                - Format the answer with proper paragraphs, links and headings.
                - Bullet Points or Lists: Where applicable, use bullet points or numbered lists to present information clearly. \
                - Emphasize Important Information: Use bold or italics to highlight key details. \

            4. Organize Content Logically \

        Do not include headings for defining sections. \

        {context}
        """

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}")
            ]
        )
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


        ### Statefully manage chat history ###
        store = {}

        def get_session_history(session_id: str) -> BaseChatMessageHistory:
            if session_id not in store:
                store[session_id] = ChatMessageHistory()
            return store[session_id]


        # conversational_rag_chain = RunnableWithMessageHistory(
        #     rag_chain,
        #     get_session_history,
        #     input_messages_key="input",
        #     history_messages_key="chat_history",
        #     output_messages_key="answer",
        # )


        # def get_response(message):
        #     answer = conversational_rag_chain.invoke(
        #         {"input": message},
        #         config={
        #             "configurable": {"session_id": "abc123"}
        #         },  # constructs a key "abc123" in `store`.
        #     )["answer"]

            # return answer
        
        self.pipeline = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

    async def get_streaming_answer(self, question):
        response_stream = []
        
        async def collect_stream(chunk):
            response_stream.append(chunk)
            yield chunk

        async def generate():
            response = await self.pipeline.ainvoke(
                {"input": question},
                config={
                    "configurable": {"session_id": "abc123"},
                    "callbacks": [StreamingStdOutCallbackHandler(collect_stream)]
                }
            )
            
            for chunk in response_stream:
                yield chunk

        return generate()

    def get_answer(self, question):
        # Use the pipeline to get the answer
        response = self.pipeline.invoke(
                {"input": question},
                config={
                    "configurable": {"session_id": "abc123"}
                },  # constructs a key "abc123" in `store`.
            )

        return response["answer"]
        
