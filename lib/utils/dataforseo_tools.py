import requests
from bs4 import BeautifulSoup
import streamlit as st
from loguru import logger

from lib.ai_seo_tools.dataforseo_analyzer import (
    DataForSEOAnalyzer,
    display_on_page_analysis,
    display_keyword_ideas,
)
from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen


def _fetch_page_text(url: str) -> str:
    """Return the raw text from a webpage."""
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        return soup.get_text("\n")
    except Exception as err:
        logger.error(f"Failed to fetch page text: {err}")
        return ""


def run_dataforseo_audit() -> None:
    """Streamlit UI to run a DataForSEO powered SEO audit on a URL."""
    st.subheader("DataForSEO SEO Audit")
    url = st.text_input("Enter page URL to analyze:")
    seed_keywords = st.text_input(
        "Seed keywords for additional ideas (comma separated):", ""
    )

    if st.button("Run SEO Audit"):
        if not url:
            st.error("Please provide a valid URL")
            return

        analyzer = DataForSEOAnalyzer()
        display_on_page_analysis(analyzer, url)

        seeds = [k.strip() for k in seed_keywords.split(",") if k.strip()]
        if seeds:
            display_keyword_ideas(analyzer, seeds)

        page_text = _fetch_page_text(url)
        if page_text:
            with st.spinner("Generating AI suggestions..."):
                prompt = (
                    "Analyze the following web page content and suggest SEO "
                    "keywords, blog topic ideas, and improvements to increase "
                    "organic visibility.\n\n" + page_text[:4000]
                )
                suggestions = llm_text_gen(prompt)
            st.markdown("## AI Suggestions")
            st.markdown(suggestions)
        else:
            st.warning("Unable to fetch page text for AI suggestions.")

