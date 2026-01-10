# Deployment Guide

## Local Development

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/query-insight.git
   cd query-insight
   ```

2. **Start services with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

   This will start:
   - PostgreSQL with TimescaleDB
   - Redis
   - Backend API (port 8000)
   - Frontend (port 5173)
   - Celery worker

3. **Access the application**:
   - Frontend: http://localhost:5173
   - API Docs: http://localhost:8000/docs
   - API: http://localhost:8000

### Manual Setup (without Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database credentials
alembic upgrade head
uvicorn src.presentation.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## Production Deployment

### Option 1: Railway.app (Recommended for MVP)

**Free tier**: $5 credit/month

1. **Create account** at https://railway.app

2. **Connect GitHub repository**

3. **Create PostgreSQL database**:
- Click "New" → "Database" → "PostgreSQL"
- Copy connection string

4. **Deploy backend**:
   ```bash
   # In Railway dashboard:
   - New → GitHub Repo → Select query-insight
   - Root Directory: /backend
   - Build Command: pip install -r requirements.txt
   - Start Command: uvicorn src.presentation.main:app --host 0.0.0.0 --port $PORT
   ```

5. **Set environment variables**:
   ```
   DATABASE_URL=<from Railway PostgreSQL>
   REDIS_URL=<from Upstash>
   SECRET_KEY=<generate secure key>
   JWT_SECRET_KEY=<generate secure key>
   ENV=production
   DEBUG=False
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```

6. **Deploy frontend** (see Vercel section below)

### Option 2: Render.com

**Free tier**: Free for web services, databases limited

1. **Create PostgreSQL database** on Render

2. **Create Web Service**:
   - Connect GitHub
   - Root Directory: `backend`
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn src.presentation.main:app --host 0.0.0.0 --port $PORT`

3. **Add environment variables** (same as Railway)

### Frontend Deployment: Vercel

**Free tier**: Unlimited bandwidth

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Deploy**:
   ```bash
   cd frontend
   vercel
   ```

3. **Set environment variables** in Vercel dashboard:
   ```
   VITE_API_URL=https://your-backend.railway.app
   ```

4. **Configure build settings**:
   - Framework: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`

### Database: Neon.tech

**Free tier**: 0.5GB storage

1. **Create account** at https://neon.tech

2. **Create database**:
   - Click "Create Project"
   - Choose region (closest to your users)
   - Copy connection string

3. **Enable TimescaleDB extension**:
   ```sql
   CREATE EXTENSION IF NOT EXISTS timescaledb;
   CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
   ```

4. **Run migrations**:
   ```bash
   # Set DATABASE_URL environment variable
   export DATABASE_URL="postgresql://..."
   alembic upgrade head
   ```

### Redis: Upstash

**Free tier**: 10K commands/day

1. **Create account** at https://upstash.com

2. **Create Redis database**:
   - Click "Create Database"
   - Choose region

3. **Copy connection URL** and set as `REDIS_URL`

### Email: Resend

**Free tier**: 100 emails/day

1. **Create account** at https://resend.com

2. **Get API key** from dashboard

3. **Verify domain** (or use testing domain)

4. **Set environment variable**:
   ```
   RESEND_API_KEY=re_...
   ```

### Monitoring: BetterStack

**Free tier**: 1GB logs/month

1. **Create account** at https://betterstack.com

2. **Create source** for logs

3. **Get source token** and set:
   ```
   BETTERSTACK_TOKEN=...
   ```

### Uptime Monitoring: UptimeRobot

**Free tier**: 50 monitors

1. **Create account** at https://uptimerobot.com

2. **Add monitors**:
   - API health: `https://your-backend.railway.app/health`
   - Frontend: `https://your-frontend.vercel.app`

3. **Set alert email** for notifications

---

## CI/CD with GitHub Actions

Already configured in `.github/workflows/`!

**On every push to `main`**:
1. Run tests
2. Check code quality (linting, type checking)
3. Build frontend
4. Deploy to Railway (backend) and Vercel (frontend) automatically

**Set GitHub Secrets**:
- `RAILWAY_TOKEN`: From Railway dashboard
- `VERCEL_TOKEN`: From Vercel settings

---

## SSL/HTTPS

- **Railway**: Automatic HTTPS
- **Render**: Automatic HTTPS
- **Vercel**: Automatic HTTPS

No configuration needed!

---

## Custom Domain

### Backend (Railway)

1. Go to Railway project settings
2. Click "Domains"
3. Add custom domain (e.g., `api.queryinsight.com`)
4. Add CNAME record in your DNS:
   ```
   api.queryinsight.com → <railway-domain>
   ```

### Frontend (Vercel)

1. Go to Vercel project settings
2. Click "Domains"
3. Add custom domain (e.g., `app.queryinsight.com`)
4. Add DNS records as instructed

### Free Domain

Use **Freenom** for free domains (.tk, .ml, .ga):
1. Go to https://www.freenom.com
2. Search for available domain
3. Register for free (1 year)

---

## Scaling Strategy

### When free tiers are not enough:

1. **Database** (when >0.5GB):
   - Upgrade Neon to $19/mo (3GB)
   - Or migrate to Supabase Pro ($25/mo)

2. **Backend** (when >$5 Railway credit):
   - Upgrade Railway to $20/mo
   - Or use Fly.io ($10-20/mo)

3. **Redis** (when >10K commands):
   - Upgrade Upstash to $10/mo (100K commands)

4. **Email** (when >100 emails/day):
   - Upgrade Resend to $20/mo (10K emails/mo)
   - Or use SendGrid ($15/mo)

**Total cost for 1000+ users**: ~$50-100/month

---

## Backup Strategy

### Database Backups

**Neon automatic backups**: 7 days retention

**Manual backup**:
```bash
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

**Store backups**:
- GitHub (encrypted)
- Google Drive
- AWS S3 free tier (5GB)

### Redis Backups

Redis data is cache only - no backups needed.

---

## Security Checklist

- [ ] HTTPS enabled everywhere
- [ ] Environment variables not committed
- [ ] API rate limiting enabled
- [ ] SQL injection prevention (parameterized queries)
- [ ] JWT tokens expire (24 hours)
- [ ] Passwords hashed with bcrypt
- [ ] CORS configured correctly
- [ ] Security headers (Helmet.js equivalent)
- [ ] Dependencies scanned (`pip-audit`, `npm audit`)
- [ ] Monitoring and alerting set up

---

## Troubleshooting

### Backend won't start

1. Check logs: `railway logs` or Render dashboard
2. Verify environment variables
3. Check database connection
4. Run migrations: `alembic upgrade head`

### Frontend API calls failing

1. Check CORS settings in backend
2. Verify `VITE_API_URL` is correct
3. Check network tab in browser DevTools

### Database connection issues

1. Verify connection string format
2. Check firewall/IP whitelist (Neon dashboard)
3. Test connection: `psql $DATABASE_URL`

### Out of Railway credits

1. Check resource usage in dashboard
2. Optimize queries/reduce API calls
3. Upgrade to paid plan ($20/mo)

---

## Performance Optimization

### Backend

- Enable Redis caching for frequently accessed data
- Use database connection pooling
- Add indexes on commonly queried fields
- Use async/await for I/O operations

### Frontend

- Code splitting with React lazy loading
- Image optimization
- Enable Vite compression
- Use CDN for static assets

### Database

- Regular VACUUM and ANALYZE
- Monitor query performance
- Add appropriate indexes
- Use TimescaleDB compression for old metrics

---

## Getting Help

- **Documentation**: See `/docs` folder
- **Issues**: GitHub Issues
- **Email**: support@queryinsight.com
- **Community**: Discord (link in README)
