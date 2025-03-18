from pymongo import MongoClient
import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_openai import ChatOpenAI

mongoClient = MongoClient(st.secrets["MONGO_URI"])
db = mongoClient["rikkei"]
logsCollection = db["logs"]

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key=st.secrets["OPENAI_API_KEY"]
)

docsearch = PineconeVectorStore.from_existing_index(
    index_name=st.secrets["PINECONE_INDEX_NAME"],
    embedding=embeddings,
    namespace=st.secrets["PINECONE_NAMESPACE"],
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={
    "k": 5,
})

llm = ChatOpenAI(
    base_url=st.secrets["DEEPSEEK_BASE_URL"],
    openai_api_key=st.secrets["DEEPSEEK_API_KEY"],
    model_name=st.secrets["DEEPSEEK_MODEL"],
    temperature=0.0,
    streaming=True
)

retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
combine_docs_chain = create_stuff_documents_chain(
    llm, retrieval_qa_chat_prompt)
retriverChain = create_retrieval_chain(retriever, combine_docs_chain)
    
st.subheader(
    "Q&A about the skills, case studies, and others available at Rikkeisoft")

if prompt := st.chat_input("Nhập câu truy vấn tại đây?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    rag_context = None
    rag_response = ""
    with st.chat_message("assistant"):
        placeholder = st.empty()
        st.caption(st.secrets["DEEPSEEK_MODEL"])
        for chunk in retriverChain.stream({"input": prompt}):
            if "answer" in chunk:
                rag_response += chunk["answer"]
                placeholder.write(rag_response)
            elif "context" in chunk:
                rag_context = chunk["context"]
        if isinstance(rag_context, list) and len(rag_context) > 0:
            with st.expander("Chi tiết dữ liệu tham khảo"):
                for doc in rag_context:
                    pageImageLink = doc.metadata['imagePath'].replace(
                        './output', 'https://pub-74060844f1a94706b326346e0c230aec.r2.dev')
                    st.image(pageImageLink)

                    fileLink = doc.metadata['originFilePath'].replace(
                        './casestudy', 'https://pub-0ed76f275ac543f195fb2c0884153262.r2.dev')
                    st.text("Link slide: ")
                    st.link_button(
                        f"Go to {doc.metadata['originFileName']}", fileLink)
    logsCollection.insert_one(
        {"prompt": prompt, "rag_response": rag_response})
