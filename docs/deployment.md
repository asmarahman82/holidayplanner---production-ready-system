# 🚀 Deployment Guide

HolidayPlanner can run locally via Docker or be deployed to Railway for cloud hosting.

##  1. Local Development

### Prerequisites
Python 3.10+
Docker installed
.env file with API keys:
   OPENWEATHER_KEY=your_key
   YELP_API_KEY=your_key
   GROQ_API_KEY=your_key

Run Locally (without Docker)
uvicorn api.main_api:app --reload
streamlit run ui/app.py

## 2. Dockerized Setup
Build the Image
docker build -t holidayplanner .
Run the Container
docker run -p 8000:8000 -p 8501:8501 holidayplanner
Then open:
Streamlit UI → http://localhost:8501
FastAPI Docs → http://localhost:8000/docs

## 3. Railway Deployment
Steps
1.Push your code to GitHub.
2.Create a new Railway project → “Deploy from GitHub”.
3.Add environment variables under Settings → Variables:

  OPENWEATHER_KEY=
  YELP_API_KEY=
  GROQ_API_KEY=

4.Railway automatically detects your Dockerfile.
5.Set the Start Command to:
docker run -p 8000:8000 -p 8501:8501 holidayplanner
Deploy!
Once live, visit:

   API → <your-railway-url>/docs
   UI → <your-railway-url>:8501