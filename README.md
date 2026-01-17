# Wevolve 🚀

**The AI-Powered Career Acceleration Ecosystem**

---

## 🎯 Vision

Wevolve solves three critical problems in the recruitment lifecycle:

1. **Resume Intelligence (The "Fix")** - Intelligent parser with confidence scoring and ATS optimization
2. **Transparent Matching (The "Why")** - Multi-Factor Matching Engine with explainable scores
3. **Actionable Growth (The "How")** - Gap Analysis Engine with personalized learning roadmaps

---

## 🏗️ Architecture

```
wevolve-hackathon/
├── backend/          # FastAPI Application
│   ├── app/
│   │   ├── main.py       # API Entry Point
│   │   ├── models.py     # SQLAlchemy Schemas
│   │   ├── database.py   # DB Connection
│   │   └── routers/      # API Endpoints
│   ├── data/             # Mock JSON files
│   └── requirements.txt
├── frontend/         # React (Vite) Dashboard
│   ├── src/
│   └── package.json
└── README.md
```

---

## 🚀 Quick Start

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API available at: `http://localhost:8000`
Docs available at: `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Dashboard available at: `http://localhost:5173`

---

## 🔑 Key Algorithms

- **Weighted Compatibility Score**: Skills (40%), Location (20%), Salary (15%), Experience (15%), Role (10%)
- **Confidence Scoring**: Heuristic evaluation of parsed text quality
- **Skill Gap Topology**: Maps missing skills to learning phases based on dependencies

---

## 👥 Team: Kasukabe Defence Group

Built with ❤️ for the hackathon.
