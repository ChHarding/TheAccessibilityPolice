import streamlit as st
import accessibility_checker

st.markdown("""
<style>
[data-testid="column"] {
    text-align: center;
    }
[data-testid="stMetric"] {
    text-align: center;
    }

[data-testid="stAlert"] {
    text-align: center;
    }

[data-testid="stMetricValue"] {
    margin-top: -10px;
    }

[data-testid="stMetricLabel"] {
    margin-bottom: -10px;
    }
</style>
""", unsafe_allow_html=True
)


st.title("The Accessibility Police")
st.write("An Automated Website Accessibility Checker")

url = st.text_input("Enter a website URL: ")

if st.button("Analyze Website"):
    html = accessibility_checker.get_webpage(url)
    soup = accessibility_checker.parse_html(html)
    results = accessibility_checker.analyze_page(soup)

    if results:
        st.subheader("ISSUES SUMMARY")

        summary = accessibility_checker.summarize_results(results)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.error("High Severity")
            st.metric("",summary['high'])
        with col2:
            st.warning("Medium Severity")
            st.metric("",summary['medium'])
        with col3:
            st.success("Low Severity")
            st.metric("", summary['low'])
        with col4:
            st.info("Total Issues")
            st.metric("", summary['total'])

        st.subheader("ISSUES BY CATEGORY")
        st.write("Missing Page Title:", summary['missing_page_title'])
        st.write("Missing Alt Text:", summary['missing_alt_text'])
        st.write("Missing Form Label:", summary['missing_form_labels'])
        st.write("Empty Link:", summary['empty_links'])
        st.write("Improper Heading Structure:", summary['heading_structure_issues'])
        st.write("Missing Language Attribute:", summary['missing_language_attribute'])

        st.subheader("DETAILED ISSUES")

        for issue in results:
            st.write("[" + issue['severity'].upper() + "] " + issue['type'])
            st.write("WCAG: " + issue['wcag'])
            st.write("Description: " + issue['description'])
            st.write("Element: " + issue['element'])
            st.write("User Impact: " + issue['user_impact'])
            st.divider()

        
    else:
        st.write("No accessibility issues found.")

