"""
AI Notes Summarizer - Main Application
A Streamlit web application for summarizing PDF files and text content using AI.
"""

import streamlit as st
import os
from pathlib import Path

# Import custom modules
from modules.pdf_processor import PDFProcessor
from modules.text_summarizer import TextSummarizer
from modules.utils import (
    setup_logging,
    validate_input,
    display_summary_stats,
    format_file_size,
)


# Initialize components
@st.cache_resource
def initialize_components():
    """Initialize PDF processor and text summarizer"""
    pdf_processor = PDFProcessor()
    text_summarizer = TextSummarizer()
    return pdf_processor, text_summarizer


def main():
    """Main application function"""
    st.set_page_config(
        page_title="AI Notes Summarizer",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Initialize components
    pdf_processor, text_summarizer = initialize_components()

    # App header
    st.title("📝 AI Notes Summarizer")
    st.markdown(
        "Transform your lengthy documents and notes into concise, bullet-point summaries using AI."
    )

    # Sidebar for options
    st.sidebar.header("⚙️ Settings")

    # Model selection
    model_options = {
        "BART (Recommended)": "facebook/bart-large-cnn",
        "T5 Small": "t5-small",
        "DistilBART": "sshleifer/distilbart-cnn-12-6",
    }

    selected_model = st.sidebar.selectbox(
        "Choose AI Model:",
        options=list(model_options.keys()),
        index=0,
        help="BART is recommended for best quality summaries",
    )

    # Update text summarizer model if changed
    if text_summarizer.model_name != model_options[selected_model]:
        text_summarizer.model_name = model_options[selected_model]
        text_summarizer.summarizer = None  # Reset to reload model

    # Summary length options
    summary_length = st.sidebar.select_slider(
        "Summary Length:",
        options=["Short", "Medium", "Long"],
        value="Medium",
        help="Choose the desired length of the summary",
    )

    # Update summary length settings
    length_settings = {"Short": (30, 150), "Medium": (50, 300), "Long": (100, 500)}
    text_summarizer.min_summary_length, text_summarizer.max_summary_length = (
        length_settings[summary_length]
    )

    # Main content area
    tab1, tab2 = st.tabs(["📄 PDF Upload", "📝 Text Input"])

    with tab1:
        st.header("Upload PDF File")
        st.markdown("Upload a PDF file to extract and summarize its content.")

        uploaded_file = st.file_uploader(
            "Choose a PDF file", type=["pdf"], help="Upload a PDF file (max 10MB)"
        )

        if uploaded_file is not None:
            # Display file info
            file_size = format_file_size(uploaded_file.size)
            st.info(f"📄 **File:** {uploaded_file.name} ({file_size})")

            # Process PDF button
            if st.button("📖 Extract & Summarize PDF", type="primary"):
                with st.spinner("Processing PDF file..."):
                    # Extract text from PDF
                    extracted_text = pdf_processor.process_pdf(uploaded_file)

                    if extracted_text:
                        st.success("✅ Text extracted successfully!")

                        # Show extracted text preview
                        with st.expander("📝 View Extracted Text (Preview)"):
                            st.text_area(
                                "Extracted Content:",
                                value=(
                                    extracted_text[:1000] + "..."
                                    if len(extracted_text) > 1000
                                    else extracted_text
                                ),
                                height=200,
                                disabled=True,
                            )

                        # Generate summary
                        summary = text_summarizer.summarize_text(extracted_text)

                        if summary:
                            st.success("✅ Summary generated successfully!")

                            # Display summary
                            st.subheader("📋 Summary")
                            st.markdown(summary)

                            # Display statistics
                            st.subheader("📊 Statistics")
                            display_summary_stats(extracted_text, summary)

                            # Download option
                            st.download_button(
                                label="💾 Download Summary",
                                data=summary,
                                file_name=f"{uploaded_file.name}_summary.txt",
                                mime="text/plain",
                            )

    with tab2:
        st.header("Direct Text Input")
        st.markdown("Paste your text content directly for summarization.")

        text_input = st.text_area(
            "Enter your text here:",
            height=300,
            placeholder="Paste your text content here...",
            help="Minimum 100 characters required for effective summarization",
        )

        # Character count
        char_count = len(text_input)
        st.caption(f"Characters: {char_count:,}")

        if st.button("🚀 Summarize Text", type="primary"):
            if validate_input(text_input, min_length=100):
                # Generate summary
                summary = text_summarizer.summarize_text(text_input)

                if summary:
                    st.success("✅ Summary generated successfully!")

                    # Display summary
                    st.subheader("📋 Summary")
                    st.markdown(summary)

                    # Display statistics
                    st.subheader("📊 Statistics")
                    display_summary_stats(text_input, summary)

                    # Download option
                    st.download_button(
                        label="💾 Download Summary",
                        data=summary,
                        file_name="text_summary.txt",
                        mime="text/plain",
                    )

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>AI Notes Summarizer | Powered by Hugging Face Transformers</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
