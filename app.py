from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64

genai.configure(api_key=os.getenv("API_KEY"))

def getResponse(input, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    res = model.generate_content([input, pdf_content[0], prompt])
    return res.text

def pdfSetup(ufile):
    if ufile is not None:
        images = pdf2image.convert_from_bytes(ufile.read())
        firstPage = images[0]

        imgByteArr = io.BytesIO()
        firstPage.save(imgByteArr, format="JPEG")
        imgByteArr = imgByteArr.getvalue()
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(imgByteArr).decode()

            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
 
st.set_page_config(page_title="ATS Resume Score Check")
st.header("Track your resume's ATS score")
inputText=st.text_area("Job Description: ",key="input")
ufile=st.file_uploader("Upload your resume(PDF): ",type=["pdf"])


if ufile is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume")

# submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("Percentage match")

input_prompt1 = """
Analyze the provided Resume for its overall quality and alignment with ATS best practices. 
Evaluate the clarity, structure, and formatting of the resume, ensuring it uses proper section headings 
(e.g., Work Experience, Skills, Education) and is easily parsed by ATS systems. Assess the inclusion of relevant keywords, 
both technical and soft skills, that align with common industry standards for the candidate's role. Identify any gaps in skills, 
experience, or education that could be flagged by an ATS as a mismatch for typical job requirements. 
Provide a detailed analysis of the resume, including strengths, areas for improvement, 
and recommendations for optimizing the document to improve its ATS compatibility. 
These recommendations could include improving keyword usage, enhancing the job descriptions with more measurable achievements, 
or adjusting the layout for better readability by ATS.
"""

input_prompt3 = """
 Analyze the provided Job Description and Resume to generate an ATS score from 0 to 100, 
 reflecting how well the resume matches the job requirements. Extract the core responsibilities, 
 mandatory and preferred skills, and experience requirements from the job description, and compare them to the skills, 
 qualifications, and experience in the resume. Look for keyword matching, experience relevance, and ATS-friendly formatting. 
 Provide a detailed explanation of the score, highlighting key strengths, gaps, and missing keywords, 
 and suggest actionable improvements to increase the resume's ATS compatibility, 
 such as adding relevant skills or rephrasing sections for better alignment. The output should include the ATS score, 
 a breakdown of the match, keyword alignment, and specific recommendations for optimizing the resume for ATS systems.
"""

if submit1:
    if ufile is not None:
        pdf_content=pdfSetup(ufile)
        response=getResponse(input_prompt1,pdf_content,inputText)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if ufile is not None:
        pdf_content=pdfSetup(ufile)
        response=getResponse(input_prompt3,pdf_content,inputText)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please upload the resume")