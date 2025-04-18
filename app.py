import streamlit as st
from main import search_web, summarize_with_openrouter

# Streamlit UI
def main():
    st.title("AI Search and Summarization")

    query = st.text_input("Ask me something:", "")

    if st.button("Search") and query:
        st.write("Searching...")
        search_results, error = search_web(query)

        if error:
            st.error(error)
        elif not search_results:
            st.write("No results found.")
        else:
            st.write("Summarizing...")
            summary, error = summarize_with_openrouter(query, search_results)
            
            if error:
                st.error(error)
            else:
                st.write("### Summary")
                st.write(summary)

if __name__ == "__main__":
    main()
