"""
Text Summarization Module
Handles text summarization using Hugging Face Transformers.
"""

from transformers import pipeline, AutoTokenizer
import torch
from typing import List, Optional
import streamlit as st
import re


class TextSummarizer:
    """Class to handle text summarization using pre-trained models"""

    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        """
        Initialize the text summarizer

        Args:
            model_name: Name of the pre-trained model to use
        """
        self.model_name = model_name
        self.summarizer = None
        self.tokenizer = None
        self.max_chunk_length = 1024  # Maximum tokens per chunk
        self.min_summary_length = 50
        self.max_summary_length = 300

    @st.cache_resource
    def load_model(_self):
        """
        Load the summarization model and tokenizer
        """
        try:
            # Check if CUDA is available
            device = 0 if torch.cuda.is_available() else -1

            # Show device info
            if torch.cuda.is_available():
                st.info(f"🚀 Using GPU acceleration: {torch.cuda.get_device_name()}")
            else:
                st.info("💻 Using CPU for processing (this may be slower)")

            # Load the summarization pipeline
            _self.summarizer = pipeline(
                "summarization",
                model=_self.model_name,
                device=device,
                torch_dtype=(
                    torch.float16 if torch.cuda.is_available() else torch.float32
                ),
            )

            # Load tokenizer for text chunking
            _self.tokenizer = AutoTokenizer.from_pretrained(_self.model_name)

            st.success(f"✅ Model loaded successfully: {_self.model_name}")
            return True

        except OSError as e:
            if "Connection error" in str(e) or "timeout" in str(e).lower():
                st.error(
                    "❌ Network error: Could not download the model. Please check your internet connection."
                )
            else:
                st.error(f"❌ Model loading error: {str(e)}")
            return False
        except RuntimeError as e:
            if "CUDA" in str(e):
                st.error("❌ GPU memory error. Trying to use CPU instead...")
                try:
                    _self.summarizer = pipeline(
                        "summarization",
                        model=_self.model_name,
                        device=-1,  # Force CPU
                        torch_dtype=torch.float32,
                    )
                    _self.tokenizer = AutoTokenizer.from_pretrained(_self.model_name)
                    st.success("✅ Model loaded successfully on CPU")
                    return True
                except Exception as cpu_e:
                    st.error(f"❌ Failed to load model on CPU: {str(cpu_e)}")
                    return False
            else:
                st.error(f"❌ Runtime error loading model: {str(e)}")
                return False
        except Exception as e:
            st.error(f"❌ Unexpected error loading model: {str(e)}")
            return False

    def chunk_text(self, text: str) -> List[str]:
        """
        Split long text into smaller chunks for processing

        Args:
            text: Input text to chunk

        Returns:
            List[str]: List of text chunks
        """
        if not self.tokenizer:
            # Fallback chunking by sentences if tokenizer not available
            sentences = re.split(r"[.!?]+", text)
            chunks = []
            current_chunk = ""

            for sentence in sentences:
                if len(current_chunk) + len(sentence) < 2000:  # Rough character limit
                    current_chunk += sentence + ". "
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence + ". "

            if current_chunk:
                chunks.append(current_chunk.strip())

            return chunks

        # Use tokenizer for precise chunking
        tokens = self.tokenizer.encode(text)
        chunks = []

        for i in range(0, len(tokens), self.max_chunk_length):
            chunk_tokens = tokens[i : i + self.max_chunk_length]
            chunk_text = self.tokenizer.decode(chunk_tokens, skip_special_tokens=True)
            chunks.append(chunk_text)

        return chunks

    def summarize_chunk(self, chunk: str) -> Optional[str]:
        """
        Summarize a single text chunk

        Args:
            chunk: Text chunk to summarize

        Returns:
            str: Summary of the chunk or None if summarization fails
        """
        try:
            # Adjust summary length based on chunk length
            chunk_length = len(chunk.split())
            max_length = min(
                self.max_summary_length, max(self.min_summary_length, chunk_length // 3)
            )
            min_length = min(self.min_summary_length, max_length // 2)

            summary = self.summarizer(
                chunk,
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
                truncation=True,
            )

            return summary[0]["summary_text"]

        except Exception as e:
            st.warning(f"Error summarizing chunk: {str(e)}")
            return None

    def format_as_bullets(self, summary_text: str) -> str:
        """
        Format summary text as bullet points

        Args:
            summary_text: Raw summary text

        Returns:
            str: Formatted bullet points
        """
        # Split by sentences and create bullet points
        sentences = re.split(r"[.!?]+", summary_text)
        bullets = []

        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 10:  # Filter out very short fragments
                bullets.append(f"• {sentence}")

        return "\n".join(bullets)

    def summarize_text(self, text: str) -> Optional[str]:
        """
        Complete text summarization pipeline

        Args:
            text: Input text to summarize

        Returns:
            str: Formatted summary or None if summarization fails
        """
        if not text or len(text.strip()) < 100:
            st.error(
                "❌ Text is too short to summarize effectively (minimum 100 characters required)"
            )
            return None

        # Check text length limits
        word_count = len(text.split())
        if word_count > 10000:
            st.warning(
                f"⚠️ Large text detected ({word_count:,} words). Processing may take several minutes."
            )

        try:
            # Load model if not already loaded
            if not self.summarizer:
                with st.spinner("🤖 Loading AI model..."):
                    if not self.load_model():
                        return None

            # Chunk the text
            chunks = self.chunk_text(text)

            if len(chunks) == 0:
                st.error("❌ Could not process the text into chunks")
                return None

            st.info(f"📄 Processing {len(chunks)} text chunk(s)...")

            # Summarize each chunk
            summaries = []
            progress_bar = st.progress(0)
            failed_chunks = 0

            for i, chunk in enumerate(chunks):
                try:
                    with st.spinner(f"🔄 Summarizing part {i+1} of {len(chunks)}..."):
                        chunk_summary = self.summarize_chunk(chunk)
                        if chunk_summary:
                            summaries.append(chunk_summary)
                        else:
                            failed_chunks += 1
                except Exception as e:
                    st.warning(f"⚠️ Failed to summarize chunk {i+1}: {str(e)}")
                    failed_chunks += 1
                    continue

                progress_bar.progress((i + 1) / len(chunks))

            # Check if we have any successful summaries
            if not summaries:
                st.error("❌ Could not generate any summaries from the text")
                return None

            if failed_chunks > 0:
                st.warning(
                    f"⚠️ {failed_chunks} out of {len(chunks)} chunks failed to process"
                )

            # Combine summaries
            combined_summary = " ".join(summaries)

            # If we have multiple chunks, summarize the combined summary
            if len(chunks) > 1 and len(combined_summary.split()) > 200:
                try:
                    with st.spinner("🔄 Creating final summary..."):
                        final_summary = self.summarize_chunk(combined_summary)
                        if final_summary:
                            combined_summary = final_summary
                except Exception as e:
                    st.warning(
                        f"⚠️ Could not create final summary, using combined chunks: {str(e)}"
                    )

            # Format as bullet points
            formatted_summary = self.format_as_bullets(combined_summary)

            if not formatted_summary.strip():
                st.error("❌ Generated summary is empty")
                return None

            return formatted_summary

        except MemoryError:
            st.error(
                "❌ Out of memory. Please try with a shorter text or restart the application."
            )
            return None
        except Exception as e:
            st.error(f"❌ Unexpected error during summarization: {str(e)}")
            return None
