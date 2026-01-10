# QueryInsight 🚀

**Database Query Performance Analyzer SaaS**

QueryInsight helps developers and DBAs optimize database performance, reduce infrastructure costs, and identify performance bottlenecks automatically.

## 🎯 Features

- **Multi-Database Support**: PostgreSQL, MySQL, MongoDB (more coming soon)
- **Automatic Query Analysis**: Capture and analyze slow queries in real-time
- **Smart Recommendations**: AI-powered index suggestions and query optimizations
- **Performance Metrics**: Track execution time trends, query patterns, and resource usage
- **Real-time Dashboard**: Beautiful, modern UI with interactive charts
- **Alerts & Notifications**: Get notified about performance degradation

## 🏗️ Architecture

QueryInsight follows **Clean Architecture** principles:

```
├── Domain Layer (Entities, Value Objects)
├── Application Layer (Use Cases, DTOs, Interfaces)
├── Infrastructure Layer (Database, Cache, External Services)
└── Presentation Layer (FastAPI REST API)
```

## 🛠️ Tech Stack

**Backend**:
- Python 3.11+ with FastAPI
- PostgreSQL + TimescaleDB for time-series data
- Redis (Upstash) for caching and message queue
- Celery for async task processing

**Frontend**:
- React + Vite
- shadcn/ui components
- Apache ECharts for visualizations
- Zustand for state management

**Infrastructure** (100% Free Tier):
- Hosting: Railway.app / Render.com
- Database: Neon.tech (PostgreSQL)
- Cache: Upstash Redis
- Frontend: Vercel
- CI/CD: GitHub Actions

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (for local development)
- Redis (for local development)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Configure environment variables
alembic upgrade head  # Run database migrations
uvicorn src.presentation.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Landing Page

```bash
cd landing-page
python -m http.server 8080
# Or use any static file server
```

## 📚 Documentation

- [Architecture Guide](docs/architecture.md)
- [API Documentation](docs/api.md)
- [Deployment Guide](docs/deployment.md)

## 🧪 Testing

**Backend**:
```bash
cd backend
pytest tests/ --cov=src --cov-report=html
```

**Frontend**:
```bash
cd frontend
npm run test
```

## 📈 Roadmap

- [x] Phase 0: Project Setup
- [ ] Phase 1: Core Engine (PostgreSQL collector, EXPLAIN analyzer)
- [ ] Phase 2: Dashboard (Real-time metrics, query details)
- [ ] Phase 3: Intelligence (Pattern detection, recommendations)
- [ ] Phase 4: Polish (Billing, notifications, documentation)
- [ ] Phase 5: Launch (ProductHunt, content marketing)

## 💼 Business Model

| Plan | Price | Databases | Retention | Features |
|------|-------|-----------|-----------|----------|
| Free | $0 | 1 | 7 days | Basic metrics |
| Starter | $49/mo | 3 | 30 days | Alerts |
| Pro | $149/mo | 10 | 90 days | Recommendations |
| Enterprise | $499/mo | Unlimited | 1 year | Custom integrations |

## 🤝 Contributing

We're in early development! Contributions welcome.

## 📄 License

MIT License - see LICENSE file

## 📧 Contact

- Website: [Coming Soon]
- Email: hello@queryinsight.com
- Twitter: @queryinsight

---

Built with ❤️ by developers, for developers.
