import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="LLM Real-Time DB", layout="wide")
st.title("🔍 LLM for Real-Time Database Queries")

query = st.text_input(
    "Enter a natural language query",
    placeholder="e.g. show FAILED transactions",
)

if st.button("Run Query"):
    if not query.strip():
        st.warning("Please enter a query")
        st.stop()

    with st.spinner("Querying database..."):
        try:
            res = requests.post(
                f"{API_BASE_URL}/query",
                json={"query": query},
                timeout=30,
            ).json()

            if "detail" in res:
                st.error(res["detail"])
                st.stop()

            st.subheader("Generated MongoDB Query")
            st.json(res["generated_query"])

            st.subheader(f"Results ({res['count']})")
            st.dataframe(res["results"])

        except Exception as e:
            st.error(str(e))
