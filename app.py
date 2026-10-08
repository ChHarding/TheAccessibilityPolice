import streamlit as st
import accessibility_checker

st.title("The Accessibility Police")
st.write("An Automated Website Accessibility Checker")

url = st.text_input("Enter a website URL: ")

if st.button("Analyze Website"):
    html = accessibility_checker.get_webpage(url)
    soup = accessibility_checker.parse_html(html)
    results = accessibility_checker.analyze_page(soup)

    if results:
        st.write(results)
    else:
        st.write("No accessibility issues found.")