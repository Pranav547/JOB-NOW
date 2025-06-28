import streamlit as st
import requests
from datetime import datetime

# Page settings
st.set_page_config(page_title="AI Job Finder", layout="wide")  # Use wide layout

# Custom CSS for background and styling
st.markdown("""
    <link href='https://fonts.googleapis.com/css?family=Poppins' rel='stylesheet'>
    <style>
        * {
            font-family: 'Poppins', sans-serif;
        }

        .stApp {
            background-image: url("https://images.unsplash.com/photo-1504384308090-c894fdcc538d");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            color: white !important;
        }

        .block-container {
            max-width: 95% !important;
            margin: 0 auto;
            background-color: rgba(0, 0, 0, 0.6);
            padding: 3rem;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.4);
        }

        .job-card {
            background-color: rgba(255, 255, 255, 0.15);
            padding: 1.2rem;
            border-radius: 10px;
            margin-bottom: 1.2rem;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            transition: transform 0.2s ease;
            color: white;
        }

        .job-card:hover {
            transform: scale(1.01);
            background-color: rgba(255, 255, 255, 0.2);
        }

        h1, h2, h3, h4, h5, h6, p, span, div {
            color: white !important;
        }

        .footer {
            text-align: center;
            margin-top: 2rem;
            color: #ffffffaa;
            font-size: 0.9rem;
        }
    </style>
""", unsafe_allow_html=True)

# Local logo
st.image("logo.png", width=100)

# Title
st.title("JOB @now")

# Inputs
skills = st.text_input("Enter your skills (comma-separated):")
location = st.text_input("Enter preferred job location:")
pages = st.slider("Number of pages to search:", min_value=1, max_value=5, value=1)

# Button
if st.button("Find Jobs"):
    if not skills:
        st.warning("Please enter at least one skill.")
    else:
        with st.spinner("Searching for jobs..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:5000/find-jobs/",
                    json={"skills": skills, "location": location, "pages": pages},
                    timeout=15
                )
                if response.status_code == 200:
                    jobs = response.json().get("jobs", [])
                    if jobs:
                        st.success(f"Found {len(jobs)} jobs:")
                        for job in jobs:
                            # Extract posted date (just the date part)
                            posted_at = job.get("job_posted_at_datetime_utc", "")
                            posted_date = ""
                            if posted_at:
                                try:
                                    posted_date = datetime.strptime(posted_at, "%Y-%m-%dT%H:%M:%S.%fZ").date()
                                except ValueError:
                                    posted_date = posted_at

                            st.markdown("<div class='job-card'>", unsafe_allow_html=True)
                            st.subheader(job.get("job_title", "No Title"))
                            st.write(f"**Company:** {job.get('employer_name', 'Unknown')}")
                            st.write(f"**Location:** {job.get('job_city', '')}, {job.get('job_country', '')}")
                            st.write(f"**Type:** {job.get('job_employment_type', '')}")
                            st.write(f"**Posted On:** {posted_date}")
                            
                            with st.expander("📄 Show Job Description"):
                                st.markdown(job.get("job_description", "No Description Available"))

                            st.markdown(f"[🌐 Apply Here]({job.get('job_apply_link', '#')})", unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.info("No jobs found matching your criteria.")
                else:
                    st.error(f"Server Error {response.status_code}: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")

# Footer
st.markdown("""
    <div class="footer">
        🚀 This is done by <strong>Pranav</strong>
    </div>
""", unsafe_allow_html=True)
