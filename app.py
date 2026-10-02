from datetime import date

import streamlit as st

from analyzer import analyze_resume
from resume_parser import extract_text_from_pdf

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")


# ---------- Helpers ----------
def badges(items, color):
    """Show a list of skills as colored Streamlit badges."""
    if not items:
        st.caption("None found")
        return
    clean = [str(i).replace("[", "(").replace("]", ")") for i in items]
    st.markdown(" ".join(f":{color}-badge[{i}]" for i in clean))


def show_verdict(score):
    if score >= 80:
        st.success("Strong Match")
    elif score >= 60:
        st.info("Good Match")
    elif score >= 40:
        st.warning("Average Match")
    else:
        st.error("Weak Match")


def bullets(items):
    return "\n".join(f"- {i}" for i in items) if items else "_Nothing to show._"


def build_report(r):
    lines = [
        "AI RESUME ANALYSIS REPORT",
        f"Date: {date.today().isoformat()}",
        f"Target role: {r['job_role']}",
        f"Match score: {r['match_score']}%",
        "",
        "SUMMARY", r["summary"], "",
        "MATCHING SKILLS", ", ".join(r["matching_skills"]) or "-", "",
        "MISSING SKILLS", ", ".join(r["missing_skills"]) or "-", "",
        "PARTIAL SKILLS", ", ".join(r["partial_skills"]) or "-", "",
        "MISSING KEYWORDS", ", ".join(r["missing_keywords"]) or "-", "",
        "EXPERIENCE MATCH", r["experience_match"], "",
        "EDUCATION MATCH", r["education_match"], "",
        "STRENGTHS", *[f"- {s}" for s in r["strengths"]], "",
        "RECOMMENDATIONS", *[f"- {s}" for s in r["recommendations"]],
    ]
    return "\n".join(lines)


# ---------- Header ----------
st.title("📄 AI Resume Analyzer")
st.caption("Compare your resume with a job description. Get a match score, skill gaps and tips to improve.")
st.divider()

# ---------- Inputs ----------
col_left, col_right = st.columns(2, gap="large")

with col_left:
    with st.container(border=True):
        st.subheader("1. Upload Resume")
        uploaded_file = st.file_uploader(
            "PDF or DOCX", type=["pdf", "docx"], label_visibility="collapsed"
        )

with col_right:
    with st.container(border=True):
        st.subheader("2. Paste Job Description")
        job_description = st.text_area(
            "Job description",
            height=180,
            placeholder="Paste the complete job description here...",
            label_visibility="collapsed",
        )

analyze_clicked = st.button("🔍 Analyze Resume", type="primary", use_container_width=True)

# ---------- Run analysis ----------
if analyze_clicked:
    if uploaded_file is None:
        st.warning("Please upload your resume.")
    elif len(job_description.strip()) < 50:
        st.warning("Please paste a complete job description (at least a few lines).")
    else:
        try:
            with st.spinner("Reading your resume..."):
                resume_text = extract_text_from_pdf(uploaded_file)

            if len(resume_text) < 100:
                st.error(
                    "Very little text was found. This may be a scanned/image-based resume. "
                    "Please upload a text-based PDF or a DOCX file."
                )
            else:
                with st.spinner("Analyzing against the job description..."):
                    st.session_state["result"] = analyze_resume(
                        resume_text[:15000], job_description.strip()[:8000]
                    )
        except ValueError as e:
            st.error(str(e))
        except Exception as e:
            st.error("Something went wrong while analyzing. Please try again.")
            with st.expander("Technical details"):
                st.code(str(e))

# ---------- Results ----------
result = st.session_state.get("result")

if result:
    st.divider()
    score = result["match_score"]

    with st.container(border=True):
        c1, c2 = st.columns([1, 2], gap="large")
        with c1:
            st.metric("Match Score", f"{score}%")
            st.progress(score / 100)
            show_verdict(score)
        with c2:
            st.subheader(result["job_role"])
            st.write(result["summary"])
            m1, m2, m3 = st.columns(3)
            m1.metric("Matching skills", len(result["matching_skills"]))
            m2.metric("Missing skills", len(result["missing_skills"]))
            m3.metric("Missing keywords", len(result["missing_keywords"]))

    tab1, tab2, tab3, tab4 = st.tabs(["🧠 Skills", "🔑 ATS Keywords", "🎯 Fit", "💡 Suggestions"])

    with tab1:
        st.markdown("**✅ Matching skills**")
        badges(result["matching_skills"], "green")
        st.markdown("**❌ Missing skills**")
        badges(result["missing_skills"], "red")
        st.markdown("**🟡 Partially matching skills**")
        badges(result["partial_skills"], "orange")

    with tab2:
        st.markdown("**Keywords found in your resume**")
        badges(result["matching_keywords"], "green")
        st.markdown("**Keywords to add**")
        badges(result["missing_keywords"], "red")

    with tab3:
        st.markdown("#### Experience / Projects")
        st.write(result["experience_match"] or "No details.")
        st.markdown("#### Education / Qualification")
        st.write(result["education_match"] or "No details.")

    with tab4:
        st.markdown("#### 💪 Strengths for this job")
        st.markdown(bullets(result["strengths"]))
        st.markdown("#### 🛠️ Recommendations")
        st.markdown(bullets(result["recommendations"]))

    st.download_button(
        "⬇️ Download Report",
        data=build_report(result),
        file_name="resume_analysis_report.txt",
        mime="text/plain",
    )

st.caption("Results are AI-generated. Review them before making decisions.")