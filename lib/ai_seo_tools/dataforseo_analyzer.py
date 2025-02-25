import os
import json
import base64
import time
import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# DataForSEO API credentials
DATAFORSEO_LOGIN = os.getenv('DATAFORSEO_LOGIN')
DATAFORSEO_PASSWORD = os.getenv('DATAFORSEO_PASSWORD')

class DataForSEOAnalyzer:
    """
    A class to interact with DataForSEO's API and perform various SEO analyses.
    """
    
    def __init__(self, login=None, password=None):
        """
        Initialize the DataForSEO analyzer with API credentials.
        
        Args:
            login (str): DataForSEO API login (optional if set in environment)
            password (str): DataForSEO API password (optional if set in environment)
        """
        self.login = login or DATAFORSEO_LOGIN
        self.password = password or DATAFORSEO_PASSWORD
        
        if not self.login or not self.password:
            st.error("DataForSEO API credentials not found. Please set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD environment variables.")
            return
            
        self.base_url = "https://api.dataforseo.com/v3"
        self.headers = {
            'Authorization': 'Basic ' + base64.b64encode(f"{self.login}:{self.password}".encode()).decode(),
            'Content-Type': 'application/json'
        }
    
    def make_request(self, endpoint, method="GET", data=None):
        """
        Make a request to the DataForSEO API.
        
        Args:
            endpoint (str): API endpoint to request
            method (str): HTTP method (GET, POST, etc.)
            data (dict): Data to send with the request
            
        Returns:
            dict: API response
        """
        url = f"{self.base_url}/{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=self.headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            else:
                st.error(f"Unsupported HTTP method: {method}")
                return None
                
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error making request to DataForSEO API: {e}")
            return None
    
    def analyze_keywords(self, keywords, location_code=2840, language_code="en"):
        """
        Analyze keywords using DataForSEO's Keyword Data API.
        
        Args:
            keywords (list): List of keywords to analyze
            location_code (int): Location code (default: 2840 for United States)
            language_code (str): Language code (default: "en" for English)
            
        Returns:
            dict: Keyword analysis data
        """
        endpoint = "keywords_data/google/search_volume/live"
        data = [{
            "location_code": location_code,
            "language_code": language_code,
            "keywords": keywords
        }]
        
        response = self.make_request(endpoint, method="POST", data=data)
        if not response or "tasks" not in response:
            return None
            
        return response
    
    def analyze_competitors(self, domain, location_code=2840, language_code="en"):
        """
        Analyze competitors using DataForSEO's Domain vs Domain API.
        
        Args:
            domain (str): Domain to analyze
            location_code (int): Location code (default: 2840 for United States)
            language_code (str): Language code (default: "en" for English)
            
        Returns:
            dict: Competitor analysis data
        """
        endpoint = "domain_analytics/competitors/live"
        data = [{
            "target": domain,
            "location_code": location_code,
            "language_code": language_code
        }]
        
        response = self.make_request(endpoint, method="POST", data=data)
        if not response or "tasks" not in response:
            return None
            
        return response
    
    def analyze_backlinks(self, domain, limit=100):
        """
        Analyze backlinks using DataForSEO's Backlinks API.
        
        Args:
            domain (str): Domain to analyze
            limit (int): Maximum number of backlinks to return
            
        Returns:
            dict: Backlinks analysis data
        """
        endpoint = "backlinks/backlinks/live"
        data = [{
            "target": domain,
            "limit": limit
        }]
        
        response = self.make_request(endpoint, method="POST", data=data)
        if not response or "tasks" not in response:
            return None
            
        return response
    
    def analyze_serp(self, keyword, location_code=2840, language_code="en"):
        """
        Analyze search engine results pages using DataForSEO's SERP API.
        
        Args:
            keyword (str): Keyword to analyze
            location_code (int): Location code (default: 2840 for United States)
            language_code (str): Language code (default: "en" for English)
            
        Returns:
            dict: SERP analysis data
        """
        endpoint = "serp/google/organic/live/regular"
        data = [{
            "keyword": keyword,
            "location_code": location_code,
            "language_code": language_code,
            "depth": 100
        }]
        
        response = self.make_request(endpoint, method="POST", data=data)
        if not response or "tasks" not in response:
            return None
            
        return response
    
    def analyze_keyword_ideas(self, seed_keywords, location_code=2840, language_code="en", limit=100):
        """
        Get keyword ideas using DataForSEO's Keyword Ideas API.
        
        Args:
            seed_keywords (list): List of seed keywords
            location_code (int): Location code (default: 2840 for United States)
            language_code (str): Language code (default: "en" for English)
            limit (int): Maximum number of keyword ideas to return
            
        Returns:
            dict: Keyword ideas data
        """
        endpoint = "keywords_data/google/keyword_ideas/live"
        data = [{
            "location_code": location_code,
            "language_code": language_code,
            "keywords": seed_keywords,
            "limit": limit
        }]
        
        response = self.make_request(endpoint, method="POST", data=data)
        if not response or "tasks" not in response:
            return None
            
        return response
    
    def analyze_content_gaps(self, domain, competitors, location_code=2840, language_code="en"):
        """
        Analyze content gaps between a domain and its competitors.
        
        Args:
            domain (str): Main domain to analyze
            competitors (list): List of competitor domains
            location_code (int): Location code (default: 2840 for United States)
            language_code (str): Language code (default: "en" for English)
            
        Returns:
            dict: Content gap analysis data
        """
        endpoint = "domain_analytics/keywords_intersections/live"
        data = [{
            "targets": [domain] + competitors,
            "location_code": location_code,
            "language_code": language_code,
            "filters": [
                {
                    "filter_type": "not_in",
                    "from": domain
                }
            ],
            "limit": 100
        }]
        
        response = self.make_request(endpoint, method="POST", data=data)
        if not response or "tasks" not in response:
            return None
            
        return response
    
    def analyze_on_page(self, url):
        """
        Analyze on-page factors using DataForSEO's On-Page API.
        
        Args:
            url (str): URL to analyze
            
        Returns:
            dict: On-page analysis data
        """
        # First, create a task
        task_endpoint = "on_page/task_post"
        task_data = [{
            "target": url,
            "max_crawl_pages": 10,
            "load_resources": True,
            "enable_javascript": True,
            "custom_js": "meta = {}; meta.title = document.title; meta;"
        }]
        
        task_response = self.make_request(task_endpoint, method="POST", data=task_data)
        if not task_response or "tasks" not in task_response:
            return None
            
        # Get the task ID
        task_id = task_response["tasks"][0]["id"]
        
        # Wait for the task to complete
        max_retries = 5
        retries = 0
        while retries < max_retries:
            time.sleep(10)  # Wait 10 seconds between checks
            
            # Check task status
            status_endpoint = f"on_page/tasks/{task_id}"
            status_response = self.make_request(status_endpoint)
            
            if not status_response or "tasks" not in status_response:
                retries += 1
                continue
                
            status = status_response["tasks"][0]["status"]
            if status == "ready":
                # Task is complete, get the results
                results_endpoint = f"on_page/pages/{task_id}"
                results = self.make_request(results_endpoint)
                return results
                
            retries += 1
            
        st.error("Timed out waiting for on-page analysis to complete.")
        return None


def display_keyword_analysis(analyzer, keywords):
    """
    Display keyword analysis results in Streamlit.
    
    Args:
        analyzer (DataForSEOAnalyzer): DataForSEO analyzer instance
        keywords (list): List of keywords to analyze
    """
    st.write("## Keyword Analysis")
    
    with st.spinner("Analyzing keywords..."):
        result = analyzer.analyze_keywords(keywords)
        
    if not result:
        st.error("Failed to analyze keywords.")
        return
        
    data = []
    for task in result.get("tasks", []):
        for item in task.get("result", []):
            for keyword_data in item.get("items", []):
                data.append({
                    "Keyword": keyword_data.get("keyword"),
                    "Search Volume": keyword_data.get("search_volume"),
                    "CPC": keyword_data.get("cpc"),
                    "Competition": keyword_data.get("competition")
                })
    
    if not data:
        st.warning("No keyword data found.")
        return
        
    df = pd.DataFrame(data)
    
    # Display the data
    st.write("### Keyword Metrics")
    st.dataframe(df)
    
    # Create visualizations
    st.write("### Search Volume Comparison")
    fig = px.bar(df, x="Keyword", y="Search Volume", title="Search Volume by Keyword")
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("### Cost Per Click (CPC)")
    fig = px.bar(df, x="Keyword", y="CPC", title="CPC by Keyword")
    st.plotly_chart(fig, use_container_width=True)


def display_competitor_analysis(analyzer, domain):
    """
    Display competitor analysis results in Streamlit.
    
    Args:
        analyzer (DataForSEOAnalyzer): DataForSEO analyzer instance
        domain (str): Domain to analyze
    """
    st.write("## Competitor Analysis")
    
    with st.spinner("Analyzing competitors..."):
        result = analyzer.analyze_competitors(domain)
        
    if not result:
        st.error("Failed to analyze competitors.")
        return
        
    data = []
    for task in result.get("tasks", []):
        for item in task.get("result", []):
            for competitor in item.get("items", []):
                data.append({
                    "Competitor": competitor.get("domain"),
                    "Common Keywords": competitor.get("common_keywords"),
                    "Relevance": competitor.get("relevance") * 100,  # Convert to percentage
                    "SE Traffic": competitor.get("se_traffic")
                })
    
    if not data:
        st.warning("No competitor data found.")
        return
        
    df = pd.DataFrame(data)
    
    # Display the data
    st.write("### Top Competitors")
    st.dataframe(df)
    
    # Create visualizations
    st.write("### Competitor Relevance")
    fig = px.bar(
        df.sort_values("Relevance", ascending=False).head(10), 
        x="Competitor", 
        y="Relevance", 
        title="Top 10 Competitors by Relevance (%)"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("### Common Keywords with Competitors")
    fig = px.bar(
        df.sort_values("Common Keywords", ascending=False).head(10), 
        x="Competitor", 
        y="Common Keywords", 
        title="Top 10 Competitors by Common Keywords"
    )
    st.plotly_chart(fig, use_container_width=True)


def display_backlink_analysis(analyzer, domain):
    """
    Display backlink analysis results in Streamlit.
    
    Args:
        analyzer (DataForSEOAnalyzer): DataForSEO analyzer instance
        domain (str): Domain to analyze
    """
    st.write("## Backlink Analysis")
    
    with st.spinner("Analyzing backlinks..."):
        result = analyzer.analyze_backlinks(domain)
        
    if not result:
        st.error("Failed to analyze backlinks.")
        return
        
    summary = {}
    backlinks = []
    
    for task in result.get("tasks", []):
        for item in task.get("result", []):
            summary = item.get("summary", {})
            for backlink in item.get("items", []):
                backlinks.append({
                    "Source URL": backlink.get("source_url"),
                    "Target URL": backlink.get("target_url"),
                    "Anchor Text": backlink.get("anchor"),
                    "Domain Authority": backlink.get("domain_rank"),
                    "Is DoFollow": backlink.get("dofollow"),
                    "First Seen": backlink.get("first_seen")
                })
    
    if not backlinks:
        st.warning("No backlink data found.")
        return
        
    df = pd.DataFrame(backlinks)
    
    # Display summary data
    st.write("### Backlink Summary")
    total_backlinks = summary.get("total_count", 0)
    referring_domains = summary.get("referring_domains", 0)
    dofollow_links = summary.get("dofollow", 0)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Backlinks", f"{total_backlinks:,}")
    with col2:
        st.metric("Referring Domains", f"{referring_domains:,}")
    with col3:
        st.metric("DoFollow Links", f"{dofollow_links:,}")
    
    # Display backlink data
    st.write("### Top Backlinks")
    st.dataframe(df.sort_values("Domain Authority", ascending=False).head(20))
    
    # Create visualizations
    if "first_seen" in df.columns and not df["first_seen"].isnull().all():
        df["first_seen"] = pd.to_datetime(df["first_seen"])
        df["month"] = df["first_seen"].dt.to_period("M")
        monthly_backlinks = df.groupby("month").size().reset_index(name="count")
        monthly_backlinks["month_str"] = monthly_backlinks["month"].astype(str)
        
        st.write("### Backlink Growth Over Time")
        fig = px.line(
            monthly_backlinks, 
            x="month_str", 
            y="count", 
            title="Backlinks Acquired Over Time"
        )
        st.plotly_chart(fig, use_container_width=True)


def display_serp_analysis(analyzer, keyword):
    """
    Display SERP analysis results in Streamlit.
    
    Args:
        analyzer (DataForSEOAnalyzer): DataForSEO analyzer instance
        keyword (str): Keyword to analyze
    """
    st.write("## SERP Analysis")
    
    with st.spinner(f"Analyzing SERP for '{keyword}'..."):
        result = analyzer.analyze_serp(keyword)
        
    if not result:
        st.error("Failed to analyze SERP.")
        return
        
    serp_items = []
    
    for task in result.get("tasks", []):
        for item in task.get("result", []):
            for serp_item in item.get("items", []):
                if serp_item.get("type") == "organic":
                    serp_items.append({
                        "Position": serp_item.get("rank_absolute"),
                        "URL": serp_item.get("url"),
                        "Title": serp_item.get("title"),
                        "Description": serp_item.get("description"),
                        "Domain": serp_item.get("domain"),
                        "SERP Features": ", ".join(serp_item.get("serp_features", {}).keys())
                    })
    
    if not serp_items:
        st.warning("No SERP data found.")
        return
        
    df = pd.DataFrame(serp_items)
    
    # Display the data
    st.write(f"### Top 10 Results for '{keyword}'")
    st.dataframe(df.head(10))
    
    # Domain distribution
    domain_counts = df["Domain"].value_counts().reset_index()
    domain_counts.columns = ["Domain", "Count"]
    
    st.write("### Domain Distribution in SERP")
    fig = px.pie(
        domain_counts.head(10), 
        values="Count", 
        names="Domain", 
        title="Top Domains in SERP Results"
    )
    st.plotly_chart(fig, use_container_width=True)


def display_keyword_ideas(analyzer, seed_keywords):
    """
    Display keyword ideas results in Streamlit.
    
    Args:
        analyzer (DataForSEOAnalyzer): DataForSEO analyzer instance
        seed_keywords (list): List of seed keywords
    """
    st.write("## Keyword Ideas")
    
    with st.spinner("Generating keyword ideas..."):
        result = analyzer.analyze_keyword_ideas(seed_keywords)
        
    if not result:
        st.error("Failed to generate keyword ideas.")
        return
        
    keyword_ideas = []
    
    for task in result.get("tasks", []):
        for item in task.get("result", []):
            for keyword_data in item.get("items", []):
                keyword_ideas.append({
                    "Keyword": keyword_data.get("keyword"),
                    "Search Volume": keyword_data.get("search_volume"),
                    "CPC": keyword_data.get("cpc"),
                    "Competition": keyword_data.get("competition"),
                    "Trend": keyword_data.get("trend")
                })
    
    if not keyword_ideas:
        st.warning("No keyword ideas found.")
        return
        
    df = pd.DataFrame(keyword_ideas)
    
    # Sort by search volume and display
    st.write("### Top Keyword Ideas by Search Volume")
    st.dataframe(df.sort_values("Search Volume", ascending=False).head(50))
    
    # Display by competition level
    st.write("### Keyword Ideas by Competition Level")
    
    # Create competition level categories
    df["Competition Level"] = pd.cut(
        df["Competition"],
        bins=[0, 0.33, 0.66, 1],
        labels=["Low", "Medium", "High"]
    )
    
    comp_counts = df["Competition Level"].value_counts().reset_index()
    comp_counts.columns = ["Competition Level", "Count"]
    
    fig = px.pie(
        comp_counts, 
        values="Count", 
        names="Competition Level", 
        title="Keyword Ideas by Competition Level",
        color="Competition Level",
        color_discrete_map={"Low": "green", "Medium": "gold", "High": "red"}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Show top 10 low competition keywords
    st.write("### Top 10 Low Competition Keywords")
    low_comp_df = df[df["Competition Level"] == "Low"].sort_values("Search Volume", ascending=False).head(10)
    st.dataframe(low_comp_df[["Keyword", "Search Volume", "CPC", "Competition"]])


def display_content_gap_analysis(analyzer, domain, competitors):
    """
    Display content gap analysis results in Streamlit.
    
    Args:
        analyzer (DataForSEOAnalyzer): DataForSEO analyzer instance
        domain (str): Main domain to analyze
        competitors (list): List of competitor domains
    """
    st.write("## Content Gap Analysis")
    
    with st.spinner("Analyzing content gaps..."):
        result = analyzer.analyze_content_gaps(domain, competitors)
        
    if not result:
        st.error("Failed to analyze content gaps.")
        return
        
    gap_keywords = []
    
    for task in result.get("tasks", []):
        for item in task.get("result", []):
            for keyword_data in item.get("items", []):
                competitors_ranking = []
                for domain_serp in keyword_data.get("keywords_data", []):
                    domain_name = domain_serp.get("se_domain")
                    position = domain_serp.get("position")
                    if domain_name and position:
                        competitors_ranking.append(f"{domain_name}: {position}")
                
                gap_keywords.append({
                    "Keyword": keyword_data.get("keyword"),
                    "Search Volume": keyword_data.get("search_volume"),
                    "Keyword Difficulty": keyword_data.get("keyword_difficulty"),
                    "CPC": keyword_data.get("cpc"),
                    "Competitor Rankings": ", ".join(competitors_ranking)
                })
    
    if not gap_keywords:
        st.warning("No content gap keywords found.")
        return
        
    df = pd.DataFrame(gap_keywords)
    
    # Sort by search volume and display
    st.write("### Content Gap Keywords")
    st.dataframe(df.sort_values("Search Volume", ascending=False))
    
    # Display visualization
    st.write("### Content Gap Opportunities by Search Volume")
    fig = px.scatter(
        df.head(20), 
        x="Keyword Difficulty", 
        y="Search Volume", 
        size="CPC", 
        hover_name="Keyword",
        labels={"Keyword Difficulty": "Keyword Difficulty (0-100)", "Search Volume": "Monthly Search Volume"},
        title="Top 20 Content Gap Opportunities"
    )
    st.plotly_chart(fig, use_container_width=True)


def display_on_page_analysis(analyzer, url):
    """
    Display on-page analysis results in Streamlit.
    
    Args:
        analyzer (DataForSEOAnalyzer): DataForSEO analyzer instance
        url (str): URL to analyze
    """
    st.write("## On-Page Analysis")
    
    with st.spinner(f"Analyzing on-page factors for '{url}'..."):
        result = analyzer.analyze_on_page(url)
        
    if not result:
        st.error("Failed to analyze on-page factors.")
        return
        
    on_page_data = {}
    page_metrics = {}
    
    for task in result.get("tasks", []):
        for item in task.get("result", []):
            if "items" in item and item["items"]:
                page_data = item["items"][0]
                on_page_data = {
                    "URL": page_data.get("url"),
                    "Status Code": page_data.get("status_code"),
                    "Page Title": page_data.get("meta", {}).get("title"),
                    "Meta Description": page_data.get("meta", {}).get("description"),
                    "H1": page_data.get("page_metrics", {}).get("h1", {}).get("count"),
                    "H2": page_data.get("page_metrics", {}).get("h2", {}).get("count"),
                    "Images": page_data.get("page_metrics", {}).get("images", {}).get("count"),
                    "Internal Links": page_data.get("page_metrics", {}).get("internal_links", {}).get("count"),
                    "External Links": page_data.get("page_metrics", {}).get("external_links", {}).get("count"),
                    "Load Time": page_data.get("page_timing", {}).get("time_to_interactive")
                }
                
                page_metrics = page_data.get("page_metrics", {})
    
    if not on_page_data:
        st.warning("No on-page data found.")
        return
        
    # Display basic on-page factors
    st.write("### On-Page Factors")
    for key, value in on_page_data.items():
        st.write(f"**{key}:** {value}")
    
    # Display content analysis
    if "content" in page_metrics:
        content_data = page_metrics["content"]
        st.write("### Content Analysis")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Word Count", content_data.get("word_count", 0))
        with col2:
            st.metric("Text/HTML Ratio", f"{content_data.get('text_ratio', 0):.2f}%")
        with col3:
            st.metric("Unique Words", content_data.get("unique_words", 0))
    
    # Display page issues
    if "checks" in page_metrics:
        checks = page_metrics["checks"]
        st.write("### Page Issues")
        
        issues = []
        for check_name, check_data in checks.items():
            if check_data.get("status") == "failed":
                issues.append({
                    "Issue": check_name.replace("_", " ").title(),
                    "Importance": check_data.get("importance", ""),
                    "Message": check_data.get("message", "")
                })
        
        if issues:
            df = pd.DataFrame(issues)
            st.dataframe(df)
        else:
            st.success("No critical issues found.")


def main_dataforseo_analyzer():
    """
    Main function for the DataForSEO Analyzer Streamlit app.
    """
    st.title("DataForSEO Comprehensive SEO Analyzer")
    st.write("""
    This tool leverages DataForSEO's API to provide comprehensive SEO analysis for your website,
    including keyword research, competitor analysis, backlink analysis, and more.
    """)
    
    # Check for API credentials
    if not DATAFORSEO_LOGIN or not DATAFORSEO_PASSWORD:
        st.warning("""
        DataForSEO API credentials not found. Please set the following environment variables:
        - DATAFORSEO_LOGIN
        - DATAFORSEO_PASSWORD
        
        You can get API credentials by signing up at [DataForSEO](https://app.dataforseo.com/register).
        """)
        
        # Allow manual entry of credentials
        login = st.text_input("DataForSEO Login:")
        password = st.text_input("DataForSEO Password:", type="password")
        
        if not login or not password:
            st.stop()
        
        analyzer = DataForSEOAnalyzer(login, password)
    else:
        analyzer = DataForSEOAnalyzer()
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Keyword Analysis", 
        "Competitor Analysis", 
        "Backlink Analysis", 
        "SERP Analysis",
        "Keyword Ideas",
        "Content Gap Analysis",
        "On-Page Analysis"
    ])
    
    with tab1:
        st.header("Keyword Analysis")
        st.write("Analyze the search volume, competition, and other metrics for your target keywords.")
        
        keywords_input = st.text_area("Enter keywords (one per line):")
        location = st.selectbox("Location", ["United States", "United Kingdom", "Canada", "Australia"], index=0)
        location_codes = {"United States": 2840, "United Kingdom": 2826, "Canada": 2124, "Australia": 2036}
        
        if st.button("Analyze Keywords"):
            if not keywords_input:
                st.error("Please enter at least one keyword.")
            else:
                keywords = [k.strip() for k in keywords_input.split("\n") if k.strip()]
                display_keyword_analysis(analyzer, keywords)
    
    with tab2:
        st.header("Competitor Analysis")
        st.write("Identify your top competitors and analyze their SEO performance.")
        
        domain = st.text_input("Enter your domain (e.g., example.com):")
        location = st.selectbox("Location ", ["United States", "United Kingdom", "Canada", "Australia"], index=0)
        
        if st.button("Analyze Competitors"):
            if not domain:
                st.error("Please enter a domain.")
            else:
                display_competitor_analysis(analyzer, domain)
    
    with tab3:
        st.header("Backlink Analysis")
        st.write("Analyze your backlink profile and discover link building opportunities.")
        
        domain_backlinks = st.text_input("Enter domain for backlink analysis:")
        limit = st.slider("Number of backlinks to analyze:", 10, 1000, 100)
        
        if st.button("Analyze Backlinks"):
            if not domain_backlinks:
                st.error("Please enter a domain.")
            else:
                display_backlink_analysis(analyzer, domain_backlinks)
    
    with tab4:
        st.header("SERP Analysis")
        st.write("Analyze the search engine results page for your target keywords.")
        
        keyword_serp = st.text_input("Enter keyword for SERP analysis:")
        location_serp = st.selectbox("Location  ", ["United States", "United Kingdom", "Canada", "Australia"], index=0)
        
        if st.button("Analyze SERP"):
            if not keyword_serp:
                st.error("Please enter a keyword.")
            else:
                display_serp_analysis(analyzer, keyword_serp)
    
    with tab5:
        st.header("Keyword Ideas")
        st.write("Discover new keyword opportunities based on your seed keywords.")
        
        seed_keywords_input = st.text_area("Enter seed keywords (one per line):")
        location_ideas = st.selectbox("Location   ", ["United States", "United Kingdom", "Canada", "Australia"], index=0)
        limit_ideas = st.slider("Number of keyword ideas to generate:", 10, 1000, 100)
        
        if st.button("Generate Keyword Ideas"):
            if not seed_keywords_input:
                st.error("Please enter at least one seed keyword.")
            else:
                seed_keywords = [k.strip() for k in seed_keywords_input.split("\n") if k.strip()]
                display_keyword_ideas(analyzer, seed_keywords)
    
    with tab6:
        st.header("Content Gap Analysis")
        st.write("Identify content gaps between your website and your competitors.")
        
        domain_gap = st.text_input("Enter your domain:")
        competitors_input = st.text_area("Enter competitor domains (one per line):")
        location_gap = st.selectbox("Location    ", ["United States", "United Kingdom", "Canada", "Australia"], index=0)
        
        if st.button("Analyze Content Gaps"):
            if not domain_gap or not competitors_input:
                st.error("Please enter your domain and at least one competitor domain.")
            else:
                competitors = [c.strip() for c in competitors_input.split("\n") if c.strip()]
                display_content_gap_analysis(analyzer, domain_gap, competitors)
    
    with tab7:
        st.header("On-Page Analysis")
        st.write("Analyze on-page factors for a specific URL.")
        
        url_on_page = st.text_input("Enter URL for on-page analysis:")
        
        if st.button("Analyze On-Page Factors"):
            if not url_on_page:
                st.error("Please enter a URL.")
            else:
                display_on_page_analysis(analyzer, url_on_page)


if __name__ == "__main__":
    main_dataforseo_analyzer()
