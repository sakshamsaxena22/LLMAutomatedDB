import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="LLM Real-Time DB",
    layout="wide"
)

st.title("🔍 LLM for Real-Time Database Queries")

query = st.text_input(
    "Enter a natural language query",
    placeholder="e.g. show failed transactions"
)

if st.button("Run Query"):
    if not query.strip():
        st.warning("Please enter a query")
        st.stop()

    with st.spinner("Querying database..."):
        try:
            response = requests.post(
                f"{API_BASE_URL}/query",
                json={"query": query},
                timeout=30
            )

            data = response.json()

            # ❌ Backend-level error (validator / LLM / Mongo)
            if response.status_code != 200:
                st.error("Query rejected by backend")
                st.code(data.get("detail", "Unknown error"))
                st.stop()

            # ❌ Logical error returned as JSON
            if "detail" in data:
                st.error(data["detail"])
                st.stop()

            # ✅ Success
            st.subheader("Generated MongoDB Query")
            st.json(data.get("generated_query", {}))

            st.subheader(f"Results ({data.get('count', 0)})")

            results = data.get("results", [])

            if not results:
                st.info("No records found.")
            else:
                st.dataframe(results, use_container_width=True)

        except requests.exceptions.ConnectionError:
            st.error("Backend is not running on http://127.0.0.1:8000")
        except requests.exceptions.Timeout:
            st.error("Backend request timed out")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
