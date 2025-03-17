import streamlit as st

st.subheader("Suggested actions for cross-selling.")

# Dữ liệu giả định
customers = [
    {"name": "SCSK", "priority": "High"},
    {"name": "Sumitomo", "priority": "Medium"},
    {"name": "NTTD", "priority": "Low"},
    {"name": "SCSK1", "priority": "High"},
    {"name": "Sumitomo1", "priority": "Medium"},
    {"name": "NTTD1", "priority": "Low"}
]

# Tạo cột cho tên khách hàng, độ ưu tiên và nút "Xem chi tiết"
for customer in customers:
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.write(customer["name"])

    with col2:
        st.write(customer["priority"])

    with col3:
        st.button(f"Chi tiết actions", key=customer["name"])
