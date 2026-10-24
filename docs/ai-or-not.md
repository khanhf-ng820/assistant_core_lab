# AI vs Non-AI Question Classification

## 10 Questions That NEED AI
| No. | Question | Reason for AI |
|---|---|---|
| 1 | Summarize the course syllabus for General Physics II. | Requires natural language summarization from unstructured text. |
| 2 | Draft an email asking a professor for an assignment extension due to illness. | Involves creative writing and personalized text generation. |
| 3 | Explain the concept of recursion using an analogy. | Demands adaptive explanation tailored to pedagogical context. |
| 4 | Rephrase this formal notice into a friendly student announcement. | Involves tone transformation and stylistic rewriting. |
| 5 | Translate this lecture excerpt into English with domain-specific terms. | Requires context-aware language translation. |
| 6 | How do I synthesize ideas from three different research papers on RAG? | Involves multi-document reasoning and synthesis. |
| 7 | Suggest a study strategy for a student struggling with Linear Algebra. | Needs personalized, contextualized advice generation. |
| 8 | Convert my raw bullet points into a structured seminar abstract. | Demands intent understanding and structural formatting. |
| 9 | Why does my C code give a segmentation fault in this pointer logic? | Requires complex code reasoning and debugging explanation. |
| 10 | Compare the Iterator pattern with the Observer pattern for my presentation. | Involves comparative synthesis of high-level abstract concepts. |

## 10 Questions That DO NOT Need AI (Rule / DB Based)
| No. | Question | Reason for Non-AI |
|---|---|---|
| 1 | Where is the Training Office located? | Exact factual lookup from database (`data/offices.csv`). |
| 2 | What are the operating hours of the Library on Saturdays? | Structured query against deterministic schedule data. |
| 3 | What is the formula for calculating priority score from credits and days left? | Deterministic mathematical evaluation (`priority = importance / days`). |
| 4 | List all courses scheduled for Monday in my timetable. | Direct relational filtering on structured calendar data. |
| 5 | What is the minimum GPA required to register for a thesis? | Strict static rule verification (`credits >= 120` and `gpa >= 2.0`). |
| 6 | Convert 50 credit points to tuition fee in VND. | Exact arithmetic multiplication by fixed rate unit. |
| 7 | Is room I.101 available at 10:00 AM today? | Precise boolean query on room booking database. |
| 8 | What is the deadline for submitting Lab 2? | Direct metadata fetch from course schedule table. |
| 9 | Who is the assigned reviewer for Member 1 in Week A? | Static rotation table lookup. |
| 10 | Show my current accumulated total credits. | Simple summation query over course history records. |