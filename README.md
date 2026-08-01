# OpenStream

**An open-source, transparent alternative to YouTube**

## Mission

To build a video platform that serves creators and viewers—not advertisers. OpenStream is designed to deliver content fairly, with transparent algorithms, community-driven moderation, and full user control.

## Key Features

- **Transparent Recommendations**: User-controlled ranking (Latest, Popular, Community-Rated)
- **Creator-First**: Channel management, analytics, and monetization alternatives
- **Community-Governed**: Open moderation and feature decisions
- **Privacy-First**: No behavioral tracking without explicit consent
- **Open Architecture**: Fully auditable code and ranking logic

## Tech Stack

- **Backend**: FastAPI (Python), PostgreSQL
- **Frontend**: React (web) + React Native (mobile)
- **Storage**: MinIO (S3-compatible)
- **Cache**: Redis
- **Video Processing**: FFmpeg, OpenCV
- **Recommendations**: PyTorch

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Node.js 18+
- Streamlit (optional, for the Streamlit frontend)

### Setup

```bash
# Clone repository
git clone https://github.com/erikaseascope/OpenStream.git
cd OpenStream

# Copy environment file
cp .env.example .env

# Start infrastructure
docker-compose up -d

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Run database migrations
alembic -c alembic.ini upgrade head

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# In a new terminal, start web frontend
cd ../frontend/web
npm install
npm start

# Optional: start Streamlit frontend
cd ../streamlit
pip install -r requirements.txt
streamlit run app.py --server.port 8501

# Access the application
# Web: http://localhost:3000
# Streamlit: http://localhost:8501
# API Docs: http://localhost:8000/docs
