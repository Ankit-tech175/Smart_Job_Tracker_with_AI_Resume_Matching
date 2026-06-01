from nlp.parser import parse_resume


# Path to uploaded resume
resume_path = "uploads/Ankit_Chauhan_Resume_v3.pdf"


# Parse resume
result = parse_resume(resume_path)


print("\n===== PARSED RESUME =====\n")

print("Extracted Skills:\n")

print(result["skills"])

print("\n=========================\n")