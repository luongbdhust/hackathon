import streamlit as st

st.subheader("Search customer portfolio and match case studies")

col1, col2 = st.columns([4, 1])

with col1:
    customerInfo = st.text_input(
        "Thông tin khách hàng (Tên, mã...)", "SCSK", label_visibility="collapsed")

with col2:
    st.button("🔍 Tra cứu")

company_info = {
    "Company Name": "Tech Solutions Ltd.",
    "Capital": "10 million USD",
    "Number of Staff": 250,
    "Scope of Business": "Software Development, AI Solutions, IT Consulting",
    "Branches Location": ["Tokyo, Japan", "Hanoi, Vietnam", "San Francisco, USA"]
}

with st.expander("Company portfolio", expanded=True):
    st.write(f"**Company Name:** {company_info['Company Name']}")
    st.write(f"**Capital:** {company_info['Capital']}")
    st.write(f"**Number of Staff:** {company_info['Number of Staff']}")
    st.write(f"**Scope of Business:** {company_info['Scope of Business']}")
    st.write("**Branches Location:**")
    for location in company_info["Branches Location"]:
        st.write(f"- {location}")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    centered = st.button("🎯 Matching with rikkei skill, casestudy", type="primary")

cards = [
    {"title": "case study 1", "description": "Mô tả case study 1"},
    {"title": "case study 2", "description": "Mô tả case study 2"},
    {"title": "case study 3", "description": "Mô tả case study 3"},
    {"title": "case study 4", "description": "Mô tả case study 4"},
]

col1, col2, col3, col4 = st.columns(4)
for i, card in enumerate(cards):
    col = [col1, col2, col3, col4][i % 4]  # Đảm bảo chỉ có 4 cột
    with col:
        st.write(f'**{card["title"]}**')
        st.write(card["description"])
        st.button("Chi tiết", key=f"btn_{i}")