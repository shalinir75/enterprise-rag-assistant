import streamlit as st

# Page configuration
st.set_page_config(
    page_title="BGI DocuQuery",
    page_icon="🤖",
    layout="wide"
)

# Initialize Session States
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processed_docs" not in st.session_state:
    st.session_state.processed_docs = False

# Sidebar: Document Upload & Settings
with st.sidebar:
    st.title("📄 BGI DocuQuery")
    st.markdown("---")
    
    st.subheader("1. Document Management")
    uploaded_files = st.file_uploader(
        "Upload PDF/Text Documents", 
        accept_multiple_files=True,
        type=["pdf", "txt", "docx"]
    )
    
    if st.button("Process Documents", type="primary", use_container_width=True):
        if uploaded_files:
            with st.spinner("Extracting & Indexing..."):
                # TODO: Call Member 1 / Member 2 pipeline here
                st.session_state.processed_docs = True
            st.success("Documents processed successfully!")
        else:
            st.warning("Please upload at least one document.")
            
    st.markdown("---")
    st.subheader("2. Debug & Inspection")
    show_chunks = st.checkbox("Show Retrieved Chunks", value=True)

# Main Header
st.title("🤖 BGI DocuQuery Assistant")
st.caption("Ask questions about your uploaded enterprise documents.")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display Retrieved Chunks & Citations if available
        if "chunks" in message and show_chunks:
            with st.expander("🔍 View Retrieved Context Chunks"):
                for idx, chunk in enumerate(message["chunks"], 1):
                    st.markdown(f"**Chunk {idx}** *(Source: {chunk.get('source', 'Unknown')})*")
                    st.info(chunk.get("text", ""))

# User Query Handling
if prompt := st.chat_input("Ask a question about BGI documents..."):
    # Display User Input
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Assistant Response Simulation
    with st.chat_message("assistant"):
        with st.spinner("Searching documents & generating response..."):
            # Mock retrieved chunks (This will be replaced when connecting Member 2/3 backend)
            dummy_chunks = [
                {"source": "bgi_policy.pdf", "text": "BGI guidelines specify standard operating procedures for document processing and AI assistant usage."},
                {"source": "report_2026.txt", "text": "The enterprise search system utilizes vector embeddings for contextual retrieval."}
            ]
            
            # Response text
            dummy_response = "Based on the uploaded BGI documents, the system uses vector embeddings to answer enterprise queries accurately."
            
            st.markdown(dummy_response)
            
            if show_chunks:
                with st.expander("🔍 View Retrieved Context Chunks"):
                    for idx, chunk in enumerate(dummy_chunks, 1):
                        st.markdown(f"**Chunk {idx}** *(Source: {chunk['source']})*")
                        st.info(chunk["text"])

    # Save to Session State
    st.session_state.messages.append({
        "role": "assistant", 
        "content": dummy_response,
        "chunks": dummy_chunks
    })