from PyPDF2 import PdfReader

pdf_file_path = "../../resumes/2.pdf"


import pdfplumber

if pdf_file_path:
    with pdfplumber.open(pdf_file_path) as pdf:
        print(
            f"ResumeProcessing() got pdf={pdf}, pdf_file_path={pdf_file_path}, pages={len(pdf.pages)}"
        )
        txt_resume = ""
        for page in pdf.pages:
            txt_resume += page.extract_text() or ""


pdf_reader = PdfReader(pdf_file_path)
print(
    f"ResumeProcessing() got pdf_reader={pdf_reader}, pdf_file_path={pdf_file_path}, pages={len(pdf_reader.pages)}"
)
txt_resume = ""
for page in pdf_reader.pages:
    txt_resume += page.extract_text() or ""
