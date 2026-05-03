## Apex Agent

**An intelligent, localized business strategy and computer vision API powered by RAG (Retrieval-Augmented Generation) and Google Gemini.**

Apex Agent is built to democratize elite business intelligence. By leveraging a custom RAG pipeline loaded with Y-Combinator startup principles and a Google Gemini reasoning engine, it provides localized, highly actionable marketing strategies for small businesses. It also features a computer vision agent to mathematically critique marketing materials.

## ✨ Key Features

*   **🧠 RAG Strategy Engine:** Ingests and cross-references high-level market data (Y-Combinator transcripts) using **ChromaDB** and **HuggingFace** embeddings to generate highly specific, context-aware business strategies.
*   **👁️ Computer Vision Agent:** Uses **OpenCV** and NumPy to mathematically calculate visual contrast and clutter in marketing flyers, translating raw pixel data into actionable design feedback.
*   **⚡ High-Speed Inference:** Powered by Google's `gemini-1.5-flash` model for rapid, hackathon-ready API responses.
*   **🌍 Localized Context:** Capable of adapting Silicon Valley frameworks to local market constraints (e.g., Lagos retail markets).

## 🛠️ Tech Stack

*   **Backend Framework:** Django / Python
*   **AI & LLM Orchestration:** LangChain, Google Generative AI (Gemini)
*   **Vector Database:** ChromaDB
*   **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)
*   **Computer Vision:** OpenCV (`cv2`), NumPy
*   **Deployment:** Render (Backend), Vercel (Next.js Frontend)

---

## 💻 Local Setup & Installation

Follow these steps to run the Apex API on your local machine.

### 1. Clone the repository

git clone [https://github.com/UkohEmmanuel1/apel-agent.git](https://github.com/UkohEmmanuel1/apel-agent.git)
cd apel-agent

2. Create and activate a Virtual Environment
Bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Environment Variables
Create a .env file in the root directory (next to manage.py) and add your Google API Key:

Code snippet
GOOGLE_API_KEY=your_actual_api_key_here
5. Run the Server
Bash
python manage.py runserver
The API will be live at http://127.0.0.1:8000/.

📡 API Endpoints
1. Generate Business Strategy
Endpoint: /api/strategy/

Method: POST

Headers: Content-Type: application/json

Body:

JSON
{
  "query": "I run a local provision store in Yaba, Lagos. A massive supermarket just opened nearby. How do I compete?"
}
2. Analyze Marketing Image
Endpoint: /api/analyze-image/

Method: POST

Headers: Content-Type: multipart/form-data

Body: Form-data with key image and a .png or .jpg file attached.

☁️ Deployment
This backend is configured for deployment on Render.

Build Command: pip install -r requirements.txt

Start Command: gunicorn core_project.wsgi (Replace core_project with your main Django app name)

Note: Ensure GOOGLE_API_KEY is added to your Render Environment Variables, as .env is ignored by Git.
