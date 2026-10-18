import streamlit as st
from pipeline import run_research_pipeline


st.set_page_config(
    page_title="ResearchPilot | AI Research Agent",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Lightweight styling using Streamlit's supported HTML/CSS rendering.
st.markdown(
    """
    <style>
      .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1250px; }
      .hero {
        padding: 1.7rem 1.8rem;
        border-radius: 18px;
        background: linear-gradient(120deg, rgba(36, 99, 235, .16), rgba(14, 165, 233, .08));
        border: 1px solid rgba(120, 140, 170, .25);
        margin-bottom: 1.2rem;
      }
      .hero h1 { margin: 0 0 .35rem 0; font-size: 2.2rem; }
      .hero p { margin: 0; opacity: .82; font-size: 1.02rem; }
      div[data-testid="stMetric"] {
        padding: 1rem;
        border: 1px solid rgba(120, 140, 170, .25);
        border-radius: 14px;
      }
      .small-note { opacity: .72; font-size: .9rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


def to_display_text(value):
    """Convert common LangChain message/content shapes to readable text."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts = []
        for item in value:
            if isinstance(item, dict):
                parts.append(item.get("text", str(item)))
            else:
                parts.append(str(item))
        return "\n".join(part for part in parts if part)
    return str(value)


def render_result_section(title, content, empty_message):
    st.subheader(title)
    text = to_display_text(content)
    if text.strip():
        st.markdown(text)
    else:
        st.info(empty_message)


with st.sidebar:
    st.markdown("## 🔎 ResearchPilot")
    st.caption("Multi-step AI research workflow")
    st.divider()
    st.markdown("### How it works")
    st.markdown(
        """
        1. **Search** — finds relevant web results.
        2. **Read** — selects a source and scrapes its page.
        3. **Write** — drafts a structured research report.
        4. **Critique** — evaluates the report and suggests improvements.
        """
    )
    st.divider()
    st.markdown("**Powered by your existing pipeline**")
    st.caption("LangChain · Tavily · BeautifulSoup · Gemini")
    st.markdown(
        '<p class="small-note">Tip: specific topics usually produce more useful reports.</p>',
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <div class="hero">
      <h1>Research, from search to report.</h1>
      <p>Enter a topic and let your AI research pipeline gather sources, read a webpage,
      write a report, and critique its quality.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("research_form", clear_on_submit=False):
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Impact of war on stock markets",
        help="Enter a focused topic for the research agents.",
    )
    submitted = st.form_submit_button(
        "🚀 Run research",
        type="primary",
        use_container_width=True,
    )

if submitted:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        try:
            with st.spinner(
                "Research is in progress: searching the web, scraping a source, "
                "writing the report, and reviewing it..."
            ):
                result = run_research_pipeline(topic.strip())

            if not isinstance(result, dict):
                st.error(
                    "The pipeline did not return a dictionary. "
                    "Check that run_research_pipeline() returns its state."
                )
            else:
                st.session_state["research_result"] = result
                st.session_state["research_topic"] = topic.strip()
                st.success("Research pipeline completed.")
        except Exception as exc:
            st.error("The research pipeline failed.")
            st.exception(exc)

result = st.session_state.get("research_result")
saved_topic = st.session_state.get("research_topic", "")

if result:
    st.divider()
    st.markdown(f"## Results for: {saved_topic}")

    search_text = to_display_text(result.get("search_results", ""))
    scraped_text = to_display_text(result.get("scraped_content", ""))
    report_text = to_display_text(result.get("report", ""))
    feedback_text = to_display_text(result.get("feedback", ""))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Workflow", "Completed")
    col2.metric("Search output", "Available" if search_text.strip() else "Missing")
    col3.metric("Scraped content", "Available" if scraped_text.strip() else "Missing")
    col4.metric("Report", "Available" if report_text.strip() else "Missing")

    tab_report, tab_sources, tab_scraped, tab_critic = st.tabs(
        ["📝 Research report", "🌐 Search results", "📄 Scraped content", "🧪 Critic review"]
    )

    with tab_report:
        if report_text.strip():
            st.markdown(report_text)
            st.download_button(
                label="⬇️ Download report (.md)",
                data=f"# Research Report: {saved_topic}\n\n{report_text}",
                file_name="research_report.md",
                mime="text/markdown",
            )
        else:
            st.warning("The pipeline did not return a report.")

    with tab_sources:
        render_result_section(
            "Search results",
            search_text,
            "No search results were returned. Check the Tavily tool output in your pipeline.",
        )

    with tab_scraped:
        render_result_section(
            "Scraped webpage content",
            scraped_text,
            "No scraped content was returned. Check whether the reader agent received a valid URL.",
        )

    with tab_critic:
        render_result_section(
            "Critic feedback",
            feedback_text,
            "No critic feedback was returned.",
        )

    with st.expander("View raw pipeline result"):
        st.json(result)

else:
    st.info("Your results will appear here after you run a research task.")
    st.markdown("### Example topics")
    examples = [
        "Impact of war on stock markets",
        "How AI agents are being used in healthcare",
        "Renewable energy investment trends",
    ]
    cols = st.columns(len(examples))
    for col, example in zip(cols, examples):
        with col:
            st.button(
                example,
                key=f"example_{example}",
                use_container_width=True,
                on_click=lambda value=example: st.session_state.update(
                    {"example_topic": value}
                ),
            )
    if st.session_state.get("example_topic"):
        st.caption(
            f"Selected example: **{st.session_state['example_topic']}** — "
            "copy it into the Research topic field above and run the pipeline."
        )
