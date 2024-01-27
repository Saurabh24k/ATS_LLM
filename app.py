import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import PyPDF2 as pdf


load_dotenv() ## load all our environment variables

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content (input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text


input_prompt="""
"Envision yourself as an advanced and highly experienced Application Tracking System (ATS), specifically tailored for the technology sector, with a profound expertise in fields like software engineering, data science, data analytics, big data engineering, Artificial Intelligence, and Machine Learning. Your core functionality is to meticulously assess resumes against specific job descriptions in these tech domains.

Given the highly competitive job market, your programming includes a sophisticated algorithm to offer constructive feedback for resume enhancement. Your evaluation process involves assigning a matching percentage that reflects how closely a resume aligns with the job description (JD). This calculation should be based on key skills, experiences, and qualifications listed in the JD.

Furthermore, you are equipped to identify and highlight any missing keywords or critical skills not present in the resume but required in the JD. Accompany these identifications with succinct suggestions for improvement. Your output should prioritize accuracy and relevancy, ensuring candidates receive the most effective guidance to tailor their resumes for optimal alignment with the job requirements."

resume:{text}
description:{jd}
I want the response in one single string having the structure
{{"Job Descriptio (JD) Match": "%", "Missing Keywords: []", "Profile Summary":""}}

"""

# Streamlit App

st.title("Smart Application Tracking System (ATS)")
st.text("Improve your resume")
jd = st.text_area("Paste your Job Description here...")
uploaded_file = st.file_uploader("Upload Your Resume", type = "pdf", help = "Please upload your resume in PDF format")

submit = st.button("Submit!")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_repsonse (input_prompt)
        formatted_response = response.replace("{{", "").replace("}}", "")
        st.subheader("Response")
        st.markdown(formatted_response)
    else:
        st.warning("Please upload a resume and paste a job description.")