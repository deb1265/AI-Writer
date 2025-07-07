import os
import PyPDF2
import docx
from loguru import logger
from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen


def load_document_text(filepath):
    """Load text content from supported file formats."""
    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext in {".txt", ".md"}:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        if ext == ".pdf":
            text = ""
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        if ext == ".docx":
            document = docx.Document(filepath)
            return "\n".join(p.text for p in document.paragraphs)
    except Exception as err:
        logger.error(f"Failed to load {filepath}: {err}")
    return ""


def summarize_text(text, filename):
    """Return a short summary of the text using LLM."""
    if not text:
        return ""
    prompt = (
        f"Provide a brief summary for the following document '{filename}':\n"
        f"{text}\n\nSummary:" 
    )
    try:
        return llm_text_gen(prompt)
    except Exception as err:
        logger.error(f"Summary generation failed: {err}")
    return ""


def process_folder(folder_path):
    """Summarize supported documents in the given folder."""
    summaries = []
    for root, _dirs, files in os.walk(folder_path):
        for name in files:
            path = os.path.join(root, name)
            text = load_document_text(path)
            if text:
                summary = summarize_text(text[:4000], name)
                if summary:
                    summaries.append(f"### {name}\n{summary}")
    return "\n\n".join(summaries)
