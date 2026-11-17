import streamlit as st
import accessibility_checker
import html as html_module

st.set_page_config(
    page_title="The Accessibility Police",
    page_icon="🔍",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #F1F5F9;
}
.jumbotron {
    background-color: #172554;
    padding: 2rem;
    border-radius: 0.5rem;
    margin-bottom: 2rem;
    }
.jumbotron-title {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 0;
    color: #ffffff;
    }
.subtitle {
    font-size: 1.5rem;
    font-weight: 400;
    color: #ffffff;
    }
.st-key-url-container,
.st-key-issue-container {
    background-color: #ffffff;
    padding: 1rem;
    border-radius: 0.5rem;
    }
.stButton > button {
    background-color: #2563EB;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    font-weight: 600;
}
.stButton > button:hover {
    background-color: #1D4ED8;
    color: #ffffff;
    border: none;
}
.filter-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #172554;
}
.issue-card {
    background-color: white;
    border: 1px solid #dce2ed;
    border-left: 3px solid #ff4b4b;
    border-radius: 13px;
    padding: 20px;
    margin-bottom: 12px;
    color: #172b4d;
}
.issue-card.medium {
    border-left-color: #e6a23c;
}
.issue-card.low {
    border-left-color: #16a36a;
}
.issue-heading {
    color: #172554;
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 700;
    font-size: 1.3rem;
    margin-bottom: 10px;
}
.issue-icon {
    background-color: #f3f5fa;
    border-radius: 8px;
    padding: 8px;
    font-size: 17px;
}
.severity {
    font-size: .8rem;
    padding: 4px 8px;
    border-radius: 20px;
    background-color: #fff0f0;
    color: #d93636;
    font-weight: 700;
}
.severity.medium {
    background-color: #fff5e5;
    color: #b7791f;
}
.severity.low {
    background-color: #e8f7ef;
    color: #16834f;
}
.issue-description {
    color: #64748b;
    font-size: 1.1rem;
    margin-left: 50px;
    margin-bottom: 15px;
}
.issue-code {
    background-color: #f3f5f9;
    color: #344c78;
    border-radius: 8px;
    padding: 10px;
    margin-left: 50px;
    font-family: monospace;
    font-size: 0.8rem;
    overflow-wrap: anywhere;
}
[data-testid="stVerticalBlock"] {
    gap: 0.7rem;
}
[data-testid="column"] {
    text-align: center;
    }
[data-testid="stAlert"] {
    text-align: center;
    margin-bottom: -20px;
    }
</style>
""", unsafe_allow_html=True
)

st.markdown("""
<div class="jumbotron">
    <div class="jumbotron-title">The Accessibility Police</div>
    <div class="subtitle">AN AUTOMATED WEBSITE ACCESSIBILITY CHECKER</div>
</div>
""", unsafe_allow_html=True)

with st.container(border=True, key="url-container"):
    st.markdown("Enter a website URL:")
    url = st.text_input("Website URL", placeholder="https://example.com", label_visibility="collapsed", key="url_input")
    analyze = st.button(
        ":material/search: Analyze Website",
        use_container_width=True
)

if analyze:
    html = accessibility_checker.get_webpage(url)

    if html is None:
        st.error("Could not retrieve that website. It may use bot protection (e.g. Cloudflare) "
                    "that blocks automated requests, have a certificate problem, or the URL may be incorrect.")
        st.stop()

    soup = accessibility_checker.parse_html(html)
    results = accessibility_checker.analyze_page(soup)

    categories = [
        "Missing page title",
        "Missing alt text",
        "Form input without label",
        "Empty link",
        "Incorrect heading structure",
        "Missing language attribute",
        "Empty heading",
        "Empty button"
    ]   

    issue_icons = {
        "Missing page title": "📃",
        "Missing alt text": "🖼️",
        "Form input without label": "🏷️",
        "Empty link": "🔗",
        "Incorrect heading structure": "📑",
        "Missing language attribute": "🌐",
        "Empty heading": "📝",
        "Empty button": "🔘"
    }

    counts = {}
    for category in categories:
        count = 0
        for issue in results:
            if issue["type"] == category:
                count += 1
        counts[category] = count

    sidebar, main = st.columns([1, 4])

    with sidebar:
        with st.container(border=True, key="issue-container"):
            st.markdown(
                '<div class="filter-title">ISSUES BY TYPE</div>',
                unsafe_allow_html=True
            )
            for category in categories:
                count = counts[category]
                st.markdown(f"""
                    <div style="
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        padding: 10px;
                        font-size: 0.8rem;
                        gap: 8px;
                    ">
                        <span>{category}</span>
                        <span style="
                            background-color: #f1f5f9;
                            border-radius: 20px;
                            padding: 5px;
                            font-weight: 600;
                        ">{count}</span>
                    </div>
                """, unsafe_allow_html=True)
    with main:
        if results:
            for issue in results:
                severity = issue["severity"].lower()

                issue_type = issue["type"]
                description = issue["description"]
                element = html_module.escape(issue["element"])
                wcag = issue["wcag"]
                user_impact = issue["user_impact"]
                issue_icon = issue_icons[issue_type]

                issue_card = f"""
                <div class="issue-card {severity}">
                <div class="issue-heading">
                    <span class="issue-icon">{issue_icon}</span>
                    <span>{issue_type}</span>
                    <span class="severity {severity}">{severity.upper()}</span>
                </div>
                <div class="issue-description">
                    {description}
                </div>
                <div class="issue-code">
                    {element}
                </div>
                <div class="issue-description" style="margin-top: 15px;">
                    <strong>WCAG:</strong> {wcag}
                </div>
                <div class="issue-description">
                    <strong>User Impact:</strong> {user_impact}
                </div>
                </div>
                """
                st.markdown(issue_card, unsafe_allow_html=True)

        else:
            st.info("No accessibility issues found.")

