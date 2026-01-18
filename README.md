# 🚀 Wevolve - AI-Powered Career Acceleration Platform

![Wevolve Banner](https://img.shields.io/badge/AI-Career_Intelligence-blueviolet?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?style=flat-square&logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-15.1.0-000000?style=flat-square&logo=next.js)
![React](https://img.shields.io/badge/React-19.0.0-61DAFB?style=flat-square&logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat-square&logo=typescript)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python)

**Wevolve** is an intelligent career acceleration ecosystem that helps job seekers analyze their resumes, identify skill gaps, and discover perfectly matched job opportunities using AI-powered insights.

Built with ❤️ by **Kasukabe Defence Group**

---

## ✨ Features

### 🎯 Core Features
- **Smart Resume Parsing** - AI-powered extraction with confidence scoring for accurate data capture from PDF and DOCX files
- **Skills Gap Analysis** - Compare your skills against target roles with personalized learning paths and skill recommendations
- **Dynamic Job Discovery** - Find perfectly matched opportunities with smart filtering and match scoring
- **Profile Verification** - Review and edit parsed resume data with an intuitive interface
- **Learning Roadmaps** - Get personalized learning paths to bridge skill gaps
- **Job Bookmarking** - Save and manage interesting job opportunities

### 🎨 UI/UX Features
- **Dark Mode Only** - Sleek, modern dark theme for reduced eye strain
- **3D Interactive Background** - Spline-powered immersive experience
- **Smooth Animations** - Framer Motion for buttery transitions
- **Responsive Design** - Mobile-first approach with Tailwind CSS
- **Glassmorphism UI** - Modern, premium design aesthetic

---

## 🏗️ Tech Stack

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Next.js** | 15.1.0 | React framework with App Router |
| **React** | 19.0.0 | UI library |
| **TypeScript** | 5.x | Type safety |
| **Tailwind CSS** | 4.x | Utility-first styling |
| **Framer Motion** | 12.26.2 | Animations |
| **TanStack Query** | 5.90.18 | Server state management |
| **Axios** | 1.13.2 | HTTP client |
| **Zod** | 4.3.5 | Schema validation |
| **React Hook Form** | 7.71.1 | Form management |
| **Radix UI** | Various | Accessible component primitives |
| **Lucide React** | 0.562.0 | Icon library |
| **Spline** | 4.1.0 | 3D graphics |

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | 0.109.0 | Modern Python web framework |
| **Uvicorn** | 0.27.0 | ASGI server |
| **SQLAlchemy** | 2.0.36+ | ORM for database |
| **Pydantic** | 2.6.0+ | Data validation |
| **PDFPlumber** | 0.10.3 | PDF text extraction |
| **python-docx** | 1.1.0 | DOCX parsing |
| **TheFuzz** | - | Fuzzy string matching |
| **Passlib + Bcrypt** | 1.7.4 / 4.0.1 | Password hashing |
| **python-jose** | 3.3.0 | JWT tokens |
| **SQLite** | - | Database (production: PostgreSQL recommended) |

---

## 📁 Project Structure

```
wevolve-ps-1-2-3-5--kasukabe-defence-group/
│
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── config/                   # Configuration files
│   │   │   └── settings.py           # App settings & environment variables
│   │   ├── db/                       # Database layer
│   │   │   ├── __init__.py
│   │   │   ├── database.py           # Database connection & session
│   │   │   └── models.py             # SQLAlchemy models
│   │   ├── routers/                  # API endpoints
│   │   │   ├── auth.py               # Authentication (register/login)
│   │   │   ├── resume.py             # Resume upload & parsing
│   │   │   ├── matching.py           # Skills & gap analysis
│   │   │   ├── job_matching.py       # Job search & matching
│   │   │   └── roadmap.py            # Learning roadmap generation
│   │   ├── schemas/                  # Pydantic schemas
│   │   │   ├── user.py               # User schemas
│   │   │   ├── resume.py             # Resume schemas
│   │   │   ├── matching.py           # Match schemas
│   │   │   └── roadmap.py            # Roadmap schemas
│   │   ├── services/                 # Business logic
│   │   │   ├── resume_parser.py      # Resume parsing logic
│   │   │   ├── job_matcher.py        # Job matching algorithms
│   │   │   └── roadmap_generator.py  # Roadmap generation
│   │   ├── main.py                   # FastAPI app entry point
│   │   └── __init__.py
│   ├── data/                         # Static data files
│   ├── tests/                        # Unit tests
│   ├── venv/                         # Virtual environment
│   ├── requirements.txt              # Python dependencies
│   └── wevolve.db                    # SQLite database
│
├── frontend/                         # Next.js Frontend
│   ├── src/
│   │   ├── app/                      # Next.js App Router pages
│   │   │   ├── auth/
│   │   │   │   ├── login/            # Login page
│   │   │   │   └── register/         # Registration page
│   │   │   ├── upload/               # Resume upload page
│   │   │   ├── verify/               # Data verification page
│   │   │   ├── gap-analysis/         # Skills gap analysis page
│   │   │   ├── jobs/                 # Job listings page
│   │   │   ├── 3d/                   # 3D components
│   │   │   ├── layout.tsx            # Root layout
│   │   │   ├── page.tsx              # Home page
│   │   │   ├── providers.tsx         # Context providers
│   │   │   └── globals.css           # Global styles
│   │   ├── components/               # React components
│   │   │   ├── layout/               # Layout components (Header, Layout)
│   │   │   ├── jobs/                 # Job-related components
│   │   │   ├── resume/               # Resume-related components
│   │   │   ├── gap-analysis/         # Gap analysis components
│   │   │   ├── ui/                   # Reusable UI components (Radix)
│   │   │   └── 3d/                   # 3D Spline components
│   │   ├── contexts/                 # React contexts
│   │   │   ├── AuthContext.tsx       # Authentication state
│   │   │   ├── ResumeContext.tsx     # Resume data state
│   │   │   ├── SavedJobsContext.tsx  # Saved jobs state
│   │   │   └── ThemeContext.tsx      # Theme (dark mode)
│   │   ├── hooks/                    # Custom React hooks
│   │   ├── lib/                      # Utility functions
│   │   │   └── utils.ts              # Helper functions (cn, etc)
│   │   ├── services/                 # API service layer
│   │   │   ├── api.ts                # Axios instance
│   │   │   └── auth.ts               # Auth API calls
│   │   └── types/                    # TypeScript types
│   │       └── index.ts              # Shared type definitions
│   ├── public/                       # Static assets
│   ├── package.json                  # Node dependencies
│   ├── tsconfig.json                 # TypeScript config
│   ├── tailwind.config.ts            # Tailwind CSS config
│   └── next.config.mjs               # Next.js config
│
├── .gitignore                        # Git ignore rules
├── package.json                      # Root package.json
└── README.md                         # This file
```

---

## 🚀 Getting Started

### Prerequisites
- **Python** 3.9 or higher
- **Node.js** 18.x or higher
- **npm** or **yarn**
- **Git**

### Installation

#### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-org/wevolve-ps-1-2-3-5--kasukabe-defence-group.git
cd wevolve-ps-1-2-3-5--kasukabe-defence-group
```

#### 2️⃣ Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (Windows)
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (optional)
# Create a .env file in backend/ directory with:
# DATABASE_URL=sqlite:///./wevolve.db
# SECRET_KEY=your-secret-key-here
# ALGORITHM=HS256
# ACCESS_TOKEN_EXPIRE_MINUTES=30

# Run database migrations (if needed)
# The database will be created automatically on first run

# Start the backend server
uvicorn app.main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`
- **API Documentation (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative Docs (ReDoc)**: `http://localhost:8000/redoc`

#### 3️⃣ Frontend Setup

```bash
# Open a new terminal
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend app will be available at `http://localhost:3000`

---

## 🎮 Usage Guide

### 1. **Registration & Authentication**
   - Navigate to `/auth/register` to create a new account
   - Or login at `/auth/login` if you already have an account
   - JWT-based authentication ensures secure sessions

### 2. **Upload Your Resume**
   - Go to `/upload` page
   - Drag & drop or click to upload your resume (PDF or DOCX)
   - The AI will parse your resume automatically

### 3. **Verify Extracted Data**
   - Review the parsed information at `/verify`
   - Edit any incorrect or missing fields
   - Confirm when ready to proceed

### 4. **Analyze Skill Gaps**
   - Navigate to `/gap-analysis`
   - Enter a target job role or description
   - View your matched skills, missing skills, and confidence scores
   - Get personalized learning roadmaps to bridge gaps

### 5. **Discover Jobs**
   - Browse job listings at `/jobs`
   - Use advanced filters (location, skills, job type, salary range)
   - View match scores for each job based on your profile
   - Save interesting jobs for later

---

## 🔌 API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and receive JWT token
- `GET /auth/me` - Get current user profile (requires auth)

### Resume Management
- `POST /resume/upload` - Upload and parse resume (PDF/DOCX)
- `GET /resume/{user_id}` - Get parsed resume data
- `PUT /resume/{user_id}` - Update resume data

### Skill Matching
- `POST /matching/analyze` - Analyze skills gap against target role
- `GET /matching/skills` - Get list of all available skills

### Job Matching
- `POST /job-matching/search` - Search and match jobs
- `POST /job-matching/filter` - Filter jobs with advanced criteria

### Learning Roadmap
- `POST /roadmap/generate` - Generate personalized learning roadmap

---

## 🎨 Design System

### Colors (Dark Theme)
- **Primary**: Vibrant purple/blue gradient
- **Background**: Deep dark (`#0a0a0a`)
- **Surface**: Elevated dark (`#1a1a1a`)
- **Accent**: Neon highlights
- **Text**: High contrast white/gray

### Typography
- **Font Family**: Inter, system fonts
- **Headings**: Bold, large sizes (4xl - 7xl)
- **Body**: Clean, readable (base - lg)

### Components
- **Glassmorphism**: Backdrop blur with semi-transparent backgrounds
- **Shadows**: Soft, elevated shadows for depth
- **Borders**: Subtle borders with low opacity
- **Animations**: Smooth fade-ins, slide-ins, and micro-interactions

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

---

## 🚢 Deployment

### Backend Deployment
1. Update `requirements.txt` if needed
2. Set environment variables for production
3. Use a production-ready database (PostgreSQL recommended)
4. Deploy to platforms like:
   - **Railway**
   - **Render**
   - **Heroku**
   - **AWS EC2**
   - **Google Cloud Run**

### Frontend Deployment
1. Build the production bundle:
   ```bash
   npm run build
   ```
2. Deploy to platforms like:
   - **Vercel** (recommended for Next.js)
   - **Netlify**
   - **AWS Amplify**
   - **Google Cloud Platform**

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- **Frontend**: Follow TypeScript and React best practices
- **Backend**: Follow PEP 8 Python style guide
- Use ESLint for frontend and flake8/black for backend

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team - Kasukabe Defence Group

- **Frontend Lead**: Crafting beautiful, interactive UIs
- **Backend Lead**: Building robust, scalable APIs
- **AI/ML Engineer**: Implementing intelligent matching algorithms
- **DevOps**: Ensuring smooth deployment & CI/CD

---

## 📞 Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/your-org/wevolve-ps-1-2-3-5--kasukabe-defence-group/issues)
- **Email**: support@wevolve.ai
- **Discord**: [Join our community](#)

---

## 🙏 Acknowledgments

- **Radix UI** for accessible component primitives
- **Spline** for 3D graphics
- **FastAPI** for the amazing Python framework
- **Next.js** for the powerful React framework
- **Vercel** for deployment infrastructure

---

## 🗺️ Roadmap

### ✅ Completed
- [x] Resume parsing (PDF/DOCX)
- [x] User authentication
- [x] Skills gap analysis
- [x] Job matching algorithm
- [x] Learning roadmap generation
- [x] Dark mode UI
- [x] 3D interactive backgrounds

### 🚧 In Progress
- [ ] AI-powered resume suggestions
- [ ] Interview preparation module
- [ ] Real-time job alerts
- [ ] Company insights

### 🔮 Future Plans
- [ ] Mobile app (React Native)
- [ ] Chrome extension for job scraping
- [ ] Integration with LinkedIn
- [ ] Video interview practice with AI
- [ ] Salary negotiation assistant
- [ ] Multi-language support
- [ ] Advanced analytics dashboard

---

<div align="center">

**⭐ Star this repository if you find it helpful! ⭐**

Made with ❤️ by [Kasukabe Defence Group](https://github.com/kasukabe-defence-group)

</div>
