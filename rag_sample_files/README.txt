RAG SAMPLE DOCUMENTS — FICTIONAL TRAINING DATA

Files:
- hiring_process.txt
- hr_docs.txt
- leave_policy.txt
- medical_policy.txt
- rca_docs.txt
- tech_docs.txt
- travel_expense.txt

Suggested practice questions:
1. How many annual leave days are provided in the sample policy?
2. What documents are commonly required during onboarding?
3. What are the required sections of an RCA?
4. What should I include in an IT access request?
5. What is the sample hotel spending limit?
6. What should happen if a medical emergency occurs?
7. What are the stages in the hiring process?

RAG exercise:
1. Load each TXT file.
2. Split text into chunks (for example, 300–500 characters with 50–80 characters overlap).
3. Create embeddings for each chunk.
4. Store embeddings and metadata (filename, chunk index) in a vector store.
5. Retrieve top-k relevant chunks for a question.
6. Ask an LLM to answer only from the retrieved context.
7. Test questions whose answers are absent and ensure the model says the documents do not specify.

Important:
All company names, policies, benefits, limits, and figures are fictional examples created for learning. Do not use these files as real HR, legal, medical, or finance guidance.
