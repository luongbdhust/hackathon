from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pymongo import MongoClient
from langchain.schema import HumanMessage, SystemMessage
import streamlit as st
from typing import Optional
from agents import Agent, Runner, WebSearchTool, set_default_openai_api, set_default_openai_client, set_tracing_disabled
from openai import AsyncOpenAI
from pydantic import BaseModel, Field
import asyncio
import nest_asyncio

nest_asyncio.apply()

mongoClient = MongoClient(st.secrets["MONGO_URI"])
db = mongoClient["rikkei"]
caseStudyCollection = db["casestudy"]

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key=st.secrets["OPENAI_API_KEY"]
)

docsearch = PineconeVectorStore.from_existing_index(
    index_name=st.secrets["PINECONE_INDEX_NAME"],
    embedding=embeddings,
    namespace=st.secrets["PINECONE_NAMESPACE"],
)

llm = ChatOpenAI(
    base_url=st.secrets["DEEPSEEK_BASE_URL"],
    openai_api_key=st.secrets["DEEPSEEK_API_KEY"],
    model_name=st.secrets["DEEPSEEK_MODEL"],
    temperature=1,
    streaming=True
)

custom_client = AsyncOpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
)

set_default_openai_client(custom_client)
# set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)


class CompanyInfo(BaseModel):
    """会社情報"""
    companyName: str = Field(description="会社名")
    capital: Optional[str] = Field(description="会社の時価総額")
    numberOfStaff: Optional[str] = Field(
        description="会社の従業員数")
    scopeOfBusiness: Optional[str] = Field(
        description="会社の事業活動範囲")
    branchesLocations: Optional[str] = Field(
        description="会社の本社や支店の所在地情報")
    revenue: Optional[str] = Field(description="会社の売上")
    recruitmentSituation: Optional[str] = Field(
        description="会社の採用状況")
    summary: Optional[str] = Field(
        description="会社の概要")


agent = Agent(
    name="Assistant",
    instructions="あなたはどの会社に関する情報を検索する専門家です。",
    model="gpt-4o-mini",
    tools=[WebSearchTool(
        user_location={"type": "approximate", "country": "JP", })],
    output_type=CompanyInfo,
)

st.set_page_config(page_title="Matching", layout="wide")
st.subheader("Search customer portfolio and match case studies")

col1, col2 = st.columns([4, 1])

with col1:
    customerInfo = st.text_input(
        "Thông tin khách hàng (Tên, mã...)", "SCSK", label_visibility="collapsed")

if 'company_info' not in st.session_state:
    st.session_state.company_info = None

if 'company_str' not in st.session_state:
    st.session_state.company_str = ''

with col2:
    if st.button("🔍 Tra cứu"):
        if customerInfo:
            print(customerInfo)

            agenResult = Runner.run_sync(
                agent, f'"{customerInfo}" はある会社に関連する情報です。この会社についての他の情報を検索し、私のアウトソーシングIT会社との協力の方向性を見つけてください。')

            st.session_state.company_info = agenResult.final_output
            print(st.session_state.company_info)

if st.session_state.company_info:
    st.session_state.company_str = f"""
    **会社名:** {st.session_state.company_info.companyName}\n
    **会社の時価総額:** {st.session_state.company_info.capital}\n
    **会社の従業員数:** {st.session_state.company_info.numberOfStaff}\n
    **会社の事業活動範囲:** {st.session_state.company_info.scopeOfBusiness}\n
    **会社の本社や支店の所在地情報:** {st.session_state.company_info.branchesLocations}\n
    **会社の売上:** {st.session_state.company_info.revenue}\n
    **会社の採用状況:** {st.session_state.company_info.recruitmentSituation}\n
    **会社の概要:** {st.session_state.company_info.summary}
    """
else:
    st.session_state.company_str = f"""
    **会社名:** SCSK株式会社\n
    **会社の時価総額:** 21,420百万円（2024年3月31日現在）\n
    **会社の従業員数:** 16,296名（2024年3月31日現在）\n
    **会社の事業活動範囲:**  アプリケーション、ネットワーク、パッケージソフトなどの提案、設計、開発、運用、保守およびプロジェクト管理。情報システムに関するコンサルテーション、製品開発、情報技術戦略の立案。システム・インテグレーション、パッケージ・インテグレーション、エンジニアリング・ソリューション、ネットワーク・ソリューションの提供。ハードウェアおよびソフトウェアの輸入・販売。テクニカルサポート、カスタマーサポート、ヘルプデスクサービス、国内外のBPOセンターによるバックオフィス業務の提供。\n
    **会社の本社や支店の所在地情報:** 東京本社（東京都江東区豊洲3-2-20 豊洲フロント）をはじめ、首都圏7カ所、関西圏3カ所、国内13のBPOセンター、海外拠点としてSCSK USA Inc.、SCSK Europe Ltd.、SCSK Asia Pacific Pte.Ltd.、PT SCSK Global Indonesia、SCSK Myanmar Ltd.などを展開。\n
    **会社の売上:**  4,803億円（2024年3月期 連結） \n
    **会社の採用状況:** SCSK株式会社は、キャリア開発、リーダーシップ開発、専門能力開発、ビジネス基礎能力開発の4カテゴリーで全200種類の社内研修を実施し、社員の継続的なキャリア開発に力を入れています。また、上司との面談を通じてキャリア計画を確認する「CDP制度」や、社内公募でキャリアアップの機会を提供する「ジョブチャレンジ制度」、社員が経験・スキルなどを公開し異動先を募る「キャリアチャレンジ制度」など、多彩なキャリア開発の機会を提供しています。 \n
    **会社の概要:** SCSK株式会社は、住友商事グループのグローバルITサービスカンパニーであり、1969年に設立されました。アプリケーション、ネットワーク、パッケージソフトなどの提案、設計、開発、運用、保守およびプロジェクト管理を中心に、情報システムに関するコンサルテーション、製品開発、情報技術戦略の立案、システム・インテグレーション、パッケージ・インテグレーション、エンジニアリング・ソリューション、ネットワーク・ソリューションの提供、ハードウェアおよびソフトウェアの輸入・販売、テクニカルサポート、カスタマーサポート、ヘルプデスクサービス、国内外のBPOセンターによるバックオフィス業務の提供など、多岐にわたるITサービスを展開しています。
    """

with st.expander("Company portfolio", expanded=True):
    st.write(st.session_state.company_str)

if st.button("🎯 Matching with rikkei skill, casestudy", type="primary"):

    promtSearch = f"""
        これはある会社の情報です： \n
        { st.session_state.company_str}
        \n
        この会社とrikkei（リッケイソフト, rikkeisoft）との協力情報を提供してください。
    """

    results = docsearch.similarity_search_with_score(query=promtSearch, k=4)
    for doc, score in results:
        st.progress(score, f"{score*100:.1f} matched")
        fileLink = doc.metadata['originFilePath'].replace(
            './casestudy', 'https://pub-0ed76f275ac543f195fb2c0884153262.r2.dev')
        st.link_button(
            f"Go to {doc.metadata['originFileName']}", fileLink)

        caseStudy = caseStudyCollection.find_one({
            "originFilePath": doc.metadata['originFilePath']
        })

        if caseStudy:
            st.write("Wait for thinking about idea ...")
            slidesStr = "\n".join(page['gpt4oSemanticText']
                                  for page in caseStudy['pages'])
            promptCasestudy = f"""
            これはある会社に関する内容です。 \n
            { st.session_state.company_str}\n
            これは、ITアウトソーシング会社（rikkei）のケーススタディに関する内容です。\n
            {slidesStr}\n
            rikkeiの営業担当者として、この会社にどのようにアプローチすればよいか教えてください。
            """
            # print(promptCasestudy)
            placeholder = st.empty()
            llm_response = ""
            for chunk in llm.stream([
                SystemMessage(
                    content="You are only allowed to answer in Vietnamese. Please do not use any other language."),
                HumanMessage(content=promptCasestudy)
            ]):
                llm_response += chunk.content
                placeholder.write(llm_response)

        break