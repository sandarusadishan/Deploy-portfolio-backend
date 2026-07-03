import os
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# .env ෆයිල් එක ලෝඩ් කරනවා
load_dotenv()

app = FastAPI()

# Frontend (Vercel Portfolio) එකේ ඉඳන් API එක call කරන්න දෙන CORS සෙටප් එක
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 💡 ආරක්ෂිත ක්‍රමය: කෝඩ් එක ඇතුළේ Key එක ලියන්නේ නැහැ.
# ලැන්ග්චේන් එක ඔටෝමැටිකවම os.environ වෙතින් GEMINI_API_KEY එක කියවා ගන්නවා.
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3
)


class ChatRequest(BaseModel):
    message: str


# 💡 ඔයාගේ අලුත්ම CV එකෙන් Update කරපු සර්ව සම්පූර්ණ Knowledge Base එක
MY_PORTFOLIO_DATA = """
About Sandaru Sadishan:
- Name: Lanka Geeganage Sandaru Sadishan
- Current Role: Associate Software Engineer at Soft Vision IT Group (Pvt) Ltd (Promoted from Software Engineering Intern)
- Contact: +94 75 423 3902 | sandarusadishan0404@gmail.com
- Location: Kiribathgoda, Gampaha, Sri Lanka (Open to Remote & Worldwide Opportunities / Relocation)
- Managing Director of Softvision IT Group: Bawan Sivanandarajah

Professional Summary:
Associate Software Engineer with hands-on full-stack experience in MERN/Next.js, React, Node.js, TypeScript, and cross-platform Flutter mobile development. Experienced in delivering scalable applications, clean code, API integrations (RESTful, WhatsApp), n8n automation, and agile delivery.

Experience:
1. Associate Software Engineer - Soft Vision IT Group (Pvt) Ltd (Dec 2025 - Present)
   - Leading modules, architectural decisions, and full-stack initiatives.
   - Specializing in scalable solutions, cloud security, and n8n workflows.
2. Software Engineering Intern - Soft Vision IT Group (Pvt) Ltd (Jun 2025 - Dec 2025)
   - Built responsive web/mobile/cloud apps with React/Next.js, Node.js/Express, and databases.
   - Configured Microsoft SQL Server (MSSQL) and TSplus in Remote Desktop (RDP) environments.

Technical Skills:
- Frontend / UI: React, Next.js, TypeScript, JavaScript, HTML5, CSS3, TailwindCSS, Three.js
- Backend / APIs: Node.js, Express.js, Java Spring Boot, Python, RESTful APIs, WhatsApp API
- Mobile: Flutter, Dart
- Databases: MongoDB, MySQL, PostgreSQL, Supabase, MSSQL
- Tools / DevOps: Git/GitHub, Vercel, Docker, n8n Automation, Agile/Scrum
- Emerging: AWS (Amplify, Lambda, S3 in progress), Python (AI/ML basics), UI/UX Principles

Key Projects:
1. Lumos CRM System: Full-stack CRM with real-time notifications, role management, analytics, and automated workflows. (React, Node.js, Express, MySQL, TailwindCSS, WhatsApp API)
2. Busy Accounting WhatsApp Chatbot: Automated Python & Gemini AI agent that converts user queries into SQL to fetch accounting data.
3. Burger Shop Food Ordering System: Responsive food ordering website with menu, cart, login, and order features. (MERN Stack)
4. Amiga Technologies Electronics Importer: Premium showcase site with categories, pricing, warranties, and responsive design. (Next.js, Supabase, TailwindCSS)
5. Maxcity Plywood Business Site: SEO-optimized site with product gallery, certifications, and mobile layout. (React, TypeScript, Vite, Tailwind CSS)
6. Soft Vision Group Corporate Site: Interactive 3D corporate site showcasing enterprise services. (React, JavaScript, TailwindCSS, Three.js)
7. EduGuard Backend: Built using Node.js and MongoDB.
8. Vehicle Market Price Tracker: Data engineering project using Databricks and Medallion Architecture.

Education:
- BSc (Hons) Computer Science (Software Engineering) - Kingston University London (UK).
- Diploma in Software Engineering - International College of Excellence in Technology (iCET).
- English Diploma - ESOFT Uni (ESU).
- G.C.E. Advanced Level (Physical Science) - Henegama Central College.

Certifications:
- AWS Educate Introduction to Cloud 101 Badge
- AWS Educate Getting Started with Storage Badge
- Search Search Engine Optimization (SEO) with Squarespace Certificate (Coursera)
- Introduction to Artificial Intelligence (Simplilearn)

Languages: English (Fluent), Sinhala (Native)
References: 
- Lahiru Vithanage (Senior Software Engineer, Pagero Lanka)
- Tharushi Rubasinghe (Assistant Lecturer, SLIIT)
"""


@app.post("/api/portfolio-chat")
async def chat_with_sandaru_ai(request: ChatRequest):
    user_query = request.message

    prompt = f"""
    You are an intelligent, friendly, and professional AI Career Assistant representing Sandaru Sadishan.
    Your goal is to answer questions from recruiters, clients, or visitors using ONLY the verified facts provided in the context below.

    If someone asks about contact info, project details, or hiring availability, guide them enthusiastically using the context data.
    If the answer cannot be found in the context, politely say that you don't have that specific information but they can contact Sandaru directly at sandarusadishan0404@gmail.com. Do not hallucinate.

    Context about Sandaru:
    {MY_PORTFOLIO_DATA}

    User Question: {user_query}

    Answer:
    """

    response = llm.invoke(prompt)
    return {"reply": response.content}