import html
import re
from typing import Any

import streamlit as st


st.set_page_config(
    page_title="Research Studio",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --ink: #172b35;
        --muted: #6d8189;
        --teal: #087e78;
        --teal-dark: #06645f;
        --mint: #e8f5f1;
        --line: #e4eceb;
        --paper: #f6f9f8;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--ink);
    }
    .stApp { background: var(--paper); }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] {
        background: #102a32;
        border-right: 1px solid rgba(255,255,255,.08);
    }
    [data-testid="stSidebar"] * { color: #e6f1ef; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #a8c0bd;
    }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.12); }
    .block-container { max-width: 1200px; padding-top: 2.2rem; padding-bottom: 4rem; }

    .brand-lockup {
        display: flex; align-items: center; gap: 12px; margin: .2rem 0 2.3rem;
    }
    .brand-mark {
        width: 42px; height: 42px; display: grid; place-items: center;
        border-radius: 13px; background: #0b8179; font-size: 21px;
        box-shadow: 0 8px 20px rgba(0,0,0,.2);
    }
    .brand-name { font: 800 16px 'Manrope', sans-serif; letter-spacing: -.3px; }
    .brand-caption { color: #8faaa7 !important; font-size: 11px; margin-top: 2px; }

    .eyebrow {
        display: inline-flex; align-items: center; gap: 8px;
        color: var(--teal); font-size: 11px; font-weight: 700;
        letter-spacing: 1.3px; text-transform: uppercase;
    }
    .eyebrow:before {
        content: ''; width: 7px; height: 7px; border-radius: 50%;
        background: #12a394; box-shadow: 0 0 0 4px #d9efeb;
    }
    .hero-title {
        font: 800 clamp(2.1rem, 4vw, 3.35rem)/1.1 'Manrope', sans-serif;
        color: #17323a; letter-spacing: -2px; margin: 14px 0 10px;
    }
    .hero-copy {
        color: #70848a; font-size: 15px; line-height: 1.7;
        max-width: 670px; margin-bottom: 1.6rem;
    }
    .workflow {
        display: flex; align-items: center; flex-wrap: wrap; gap: 8px;
        margin: 0 0 1.4rem; color: #6d8189; font-size: 12px;
    }
    .workflow-step {
        padding: 7px 11px; border: 1px solid var(--line);
        border-radius: 999px; background: #fff;
    }
    .workflow-arrow { color: #a8b8b8; }

    div[data-testid="stForm"] {
        padding: 1.25rem 1.4rem 1.1rem; border: 1px solid var(--line);
        border-radius: 18px; background: #fff;
        box-shadow: 0 12px 35px rgba(29, 63, 67, .045);
    }
    .stTextArea label, .stTextInput label {
        color: #29444c !important; font-weight: 600 !important;
    }
    .stTextArea textarea {
        border-radius: 12px !important; border-color: #dce8e6 !important;
        background: #fbfdfc !important; line-height: 1.6 !important;
    }
    .stTextArea textarea:focus { border-color: #53aaa1 !important; }
    .stButton button, .stFormSubmitButton button {
        border-radius: 10px; font-weight: 700; transition: .15s ease;
    }
    .stFormSubmitButton button {
        color: #fff; background: var(--teal); border: 1px solid var(--teal);
        padding: .55rem 1.2rem;
    }
    .stFormSubmitButton button:hover {
        background: var(--teal-dark); border-color: var(--teal-dark);
    }
    .section-heading {
        font: 700 20px 'Manrope', sans-serif; color: #1b3940;
        letter-spacing: -.4px; margin: 1.65rem 0 .25rem;
    }
    .section-subtitle { color: #7b8d91; font-size: 13px; margin-bottom: 1rem; }
    .result-card {
        border: 1px solid var(--line); border-radius: 16px;
        padding: 1.1rem 1.3rem; background: #fff;
        box-shadow: 0 8px 24px rgba(29, 63, 67, .035);
    }
    .sidebar-note {
        padding: 13px; border-radius: 12px; background: rgba(255,255,255,.06);
        border: 1px solid rgba(255,255,255,.09); margin-top: 1rem;
    }
    .sidebar-note strong { color: #e8f5f1; font-size: 12px; }
    .sidebar-note p { font-size: 11px; line-height: 1.6; margin: 6px 0 0; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; border-bottom-color: var(--line); }
    .stTabs [data-baseweb="tab"] { padding: 10px 14px; }
    .stTabs [aria-selected="true"] { color: var(--teal) !important; }
    div[data-testid="stMetric"] {
        background: #fff; border: 1px solid var(--line);
        border-radius: 14px; padding: 14px 16px;
    }
    div[data-testid="stMetricLabel"] { color: #7b8d91; }
    [data-testid="stAlert"] { border-radius: 12px; }
    </style>
    """,
    unsafe_allow_html=True,
)


def _as_text(value: Any) -> str:
    """Convert pipeline output blocks into readable text."""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(
            str(block.get("text", ""))
            for block in value
            if isinstance(block, dict) and block.get("type") == "text"
        )
    return str(value) if value is not None else ""


def _extract_urls(*texts: str) -> list[str]:
    urls: list[str] = []
    for text in texts:
        for match in re.findall(r"https?://[^\s<>\"')\]]+", text):
            url = match.rstrip(".,;:!?")
            if url not in urls:
                urls.append(url)
    return urls


def _render_sidebar() -> None:
    with st.sidebar:
        st.markdown(
            """
            <div class="brand-lockup">
                <div class="brand-mark">⌕</div>
                <div>
                    <div class="brand-name">Research Studio</div>
                    <div class="brand-caption">MULTI-AGENT RESEARCH ASSISTANT</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("### Your research team")
        st.markdown(
            "- **Search agent** finds relevant sources\n"
            "- **Reader agent** extracts useful context\n"
            "- **Writer agent** drafts a structured report\n"
            "- **Critic agent** reviews quality and clarity"
        )
        st.markdown("---")
        st.markdown("#### How it works")
        st.markdown(
            "Enter a research question and the team will search the web, "
            "read a relevant page, write a report, then evaluate the result."
        )
        st.markdown(
            """
            <div class="sidebar-note">
                <strong>Designed for grounded research</strong>
                <p>Reports include source links and a separate critique.
                Always verify important claims against the original sources.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("")
        st.caption("Research Studio · Powered by your configured agents")


def _render_results(result: dict[str, Any], topic: str) -> None:
    report = _as_text(result.get("report"))
    feedback = _as_text(result.get("feedback"))
    search_results = _as_text(result.get("search_results"))
    scraped_content = _as_text(result.get("scraped_content"))
    sources = _extract_urls(report, search_results, scraped_content)

    st.markdown('<div class="section-heading">Research results</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-subtitle">A research brief for <strong>{html.escape(topic)}</strong></div>',
        unsafe_allow_html=True,
    )

    overview, source_count, review = st.columns(3)
    overview.metric("Pipeline", "Complete", help="Search, reading, writing, and review finished.")
    source_count.metric("Sources found", len(sources))
    review.metric("Quality review", "Included" if feedback else "Unavailable")

    report_col, action_col = st.columns([5, 1.35], vertical_alignment="center")
    with report_col:
        st.markdown("#### Research report")
    with action_col:
        st.download_button(
            "Download report",
            data=report,
            file_name=f"{re.sub(r'[^a-zA-Z0-9]+', '-', topic).strip('-').lower() or 'research'}-report.md",
            mime="text/markdown",
            use_container_width=True,
            disabled=not report,
        )

    report_tab, review_tab, sources_tab = st.tabs(
        ["Report", "Critic review", f"Sources & process ({len(sources)})"]
    )
    with report_tab:
        if report:
            st.markdown(report)
        else:
            st.info("The pipeline completed without returning a report.")

    with review_tab:
        if feedback:
            st.markdown(feedback)
        else:
            st.info("No critic feedback was returned for this run.")

    with sources_tab:
        if sources:
            st.markdown("##### Source links")
            for index, url in enumerate(sources, start=1):
                st.markdown(f"{index}. [{url}]({url})")
        else:
            st.info("No source URLs were found in the pipeline output.")
        with st.expander("Search results"):
            st.markdown(search_results or "_No search results returned._")
        with st.expander("Reader agent notes"):
            st.markdown(scraped_content or "_No scraped content returned._")


_render_sidebar()

st.markdown('<div class="eyebrow">Multi-agent research workspace</div>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">Turn questions into<br>well-sourced insight.</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-copy">Research a topic with a coordinated team of AI agents. '
    'Get a clear, structured report, source links, and an independent quality review.</p>',
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="workflow">
        <span class="workflow-step">01 &nbsp; Discover</span><span class="workflow-arrow">→</span>
        <span class="workflow-step">02 &nbsp; Read</span><span class="workflow-arrow">→</span>
        <span class="workflow-step">03 &nbsp; Write</span><span class="workflow-arrow">→</span>
        <span class="workflow-step">04 &nbsp; Review</span>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("research_form", clear_on_submit=False):
    topic = st.text_area(
        "What would you like to research?",
        key="research_topic",
        placeholder="For example: How are small businesses using generative AI in 2026?",
        height=105,
        help="Be specific for more focused search results and a more useful report.",
    )
    submitted = st.form_submit_button("✦  Start research", type="primary")

if submitted:
    cleaned_topic = topic.strip()
    if not cleaned_topic:
        st.warning("Enter a research question or topic to get started.")
    else:
        try:
            from pipeline import run_research_pipeline

            with st.status("Research team is getting to work...", expanded=True) as status:
                st.write("Searching for recent, relevant sources")
                st.write("Reading the most relevant source")
                st.write("Drafting and reviewing your research report")
                result = run_research_pipeline(cleaned_topic)
                status.update(
                    label="Research complete",
                    state="complete",
                    expanded=False,
                )
            st.session_state["research_result"] = result
            st.session_state["research_result_topic"] = cleaned_topic
        except Exception as error:
            st.error("The research run did not complete. Check your model and search API configuration, then try again.")
            with st.expander("Technical details"):
                st.exception(error)

if st.session_state.get("research_result"):
    st.divider()
    _render_results(
        st.session_state["research_result"],
        st.session_state.get("research_result_topic", "your topic"),
    )
else:
    st.markdown(
        """
        <div class="result-card" style="margin-top: 1.4rem;">
            <div class="eyebrow">Ready when you are</div>
            <div style="font:700 19px 'Manrope',sans-serif; margin:10px 0 5px;">
                Your next research brief starts with a question.
            </div>
            <div style="color:#7b8d91; font-size:13px; line-height:1.6;">
                Enter a topic above to bring your research team together. Your report,
                citations, and reviewer feedback will appear here.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )