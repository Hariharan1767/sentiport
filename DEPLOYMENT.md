# Sentiport Deployment Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment](#production-deployment)
5. [Configuration](#configuration)
6. [Troubleshooting](#troubleshooting)
7. [API Documentation](#api-documentation)

---

## Prerequisites

### System Requirements
- **Python 3.8+**
- **Node.js 16+** and npm
- **Docker 20.10+** and Docker Compose 1.29+ (for containerized deployment)
- **4GB RAM minimum** (8GB+ recommended)
- **2GB disk space** for dependencies and data

### Optional Requirements
- **NVIDIA GPU** (for faster sentiment analysis and ML models)
- **Redis** (for caching in production)
- **PostgreSQL** (for persistent data storage in production)

---

## Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/sentiport.git
cd sentiport
```

### 2. Create Python Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Node.js Dependencies
```bash
npm install
```

### 5. Download NLTK Data (One-time)
```bash
python -c "
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('vader_lexicon')
"
```

Or use the automated script:
```bash
python run_local.py
```

### 6. Configure Environment Variables
Create a `.env` file in the project root:
```bash
# Flask Configuration
FLASK_APP=api_server.py
FLASK_ENV=development
PORT=5000

# Frontend Configuration
VITE_API_URL=http://localhost:5000

# Optional: API Keys for news data
NEWS_API_KEY=your_api_key_here
FINNHUB_API_KEY=your_api_key_here
```

### 7. Start Development Servers

**Terminal 1 - Backend API:**
```bash
python run_local.py
```
Or manually:
```bash
python api_server.py
```

**Terminal 2 - Frontend (in separate terminal):**
```bash
npm run dev
```

Access the application at:
- Frontend: http://localhost:5173
- API: http://localhost:5000
- API Health: http://localhost:5000/api/health

---

## Docker Deployment

### Build and Run with Docker Compose

#### 1. Ensure Docker and Docker Compose are Installed
```bash
docker --version
docker-compose --version
```

#### 2. Build the Docker Image
```bash
docker-compose build
```

#### 3. Start Services
```bash
docker-compose up -d
```

#### 4. Verify Services
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f api

# Test API health
curl http://localhost:5000/api/health
```

#### 5. Stop Services
```bash
docker-compose down
```

### Docker Deployment Scripts

**Windows:**
```bash
deploy.bat
```

**macOS/Linux:**
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## Production Deployment

### Option 1: Docker on Cloud Platforms

#### AWS ECS/Fargate
```bash
# Build and push image to AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag sentiport-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/sentiport-api:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/sentiport-api:latest
```

#### Google Cloud Run
```bash
gcloud run deploy sentiport --source . --platform managed --region us-central1
```

#### Azure Container Instances
```bash
az acr build --registry <registry-name> --image sentiport:latest .
```

### Option 2: Kubernetes Deployment

Create `k8s-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sentiport-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sentiport-api
  template:
    metadata:
      labels:
        app: sentiport-api
    spec:
      containers:
      - name: api
        image: sentiport-api:latest
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: production
        - name: PORT
          value: "5000"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: sentiport-api-service
spec:
  selector:
    app: sentiport-api
  type: LoadBalancer
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
```

Deploy with:
```bash
kubectl apply -f k8s-deployment.yaml
```

### Option 3: Traditional Server Deployment

#### 1. Install Dependencies
```bash
sudo apt-get update
sudo apt-get install -y python3.11 python3-pip nodejs npm nginx
```

#### 2. Clone and Setup
```bash
git clone https://github.com/yourusername/sentiport.git /opt/sentiport
cd /opt/sentiport
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
npm install
```

#### 3. Build Frontend
```bash
npm run build
```

#### 4. Create Systemd Service
Create `/etc/systemd/system/sentiport.service`:
```ini
[Unit]
Description=Sentiport API Server
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/opt/sentiport
Environment="PATH=/opt/sentiport/venv/bin"
Environment="FLASK_ENV=production"
ExecStart=/opt/sentiport/venv/bin/python api_server.py
Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable sentiport
sudo systemctl start sentiport
```

#### 5. Configure Nginx
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location / {
        root /opt/sentiport/dist;
        try_files $uri $uri/ /index.html;
    }
}
```

Reload nginx:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

## Configuration

### Environment Variables

#### Required
- `FLASK_APP` - Entry point (default: api_server.py)
- `FLASK_ENV` - Environment mode: development/production
- `PORT` - Server port (default: 5000)

#### Optional
- `DEBUG` - Enable debug mode (0/1)
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `DATABASE_URL` - Database connection string (for persistent storage)
- `REDIS_URL` - Redis connection string (for caching)
- `NEWS_API_KEY` - API key for news data
- `FINNHUB_API_KEY` - API key for financial data

### Configuration File

Create `config/config.yaml`:
```yaml
app:
  name: Sentiport
  version: 1.0.0
  environment: production
  debug: false
  
api:
  host: 0.0.0.0
  port: 5000
  workers: 4
  timeout: 120
  
data:
  cache_dir: ./data
  models_dir: ./models
  
sentiment:
  model_type: logistic_regression
  min_confidence: 0.6
  
optimization:
  risk_free_rate: 0.02
  rebalance_frequency: monthly
  
logging:
  level: INFO
  file: logs/sentiport.log
```

---

## Troubleshooting

### 1. Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### 2. NLTK Data Not Found
```bash
python -c "import nltk; nltk.download('punkt')"
```

### 3. Module Import Errors
Ensure virtual environment is activated:
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 4. Docker Build Failures
Clear cache and rebuild:
```bash
docker-compose down
docker system prune -a
docker-compose build --no-cache
```

### 5. API Connection Issues
Check if API is running:
```bash
curl http://localhost:5000/api/health
```

Check logs:
```bash
docker-compose logs -f api
# or
tail -f logs/sentiport.log
```

### 6. Memory Issues
Increase container memory limit in `docker-compose.yml`:
```yaml
services:
  api:
    mem_limit: 4g
```

---

## API Documentation

### Base URL
- **Development**: `http://localhost:5000`
- **Production**: `https://your-domain.com`

### Endpoints

#### Health Check
```
GET /api/health
```
Response: `{"status": "healthy", "timestamp": "2024-01-15T10:30:00", "version": "1.0.0"}`

#### Stock Data
```
POST /api/stocks/data
Body: {"ticker": "AAPL", "period": "1y", "interval": "1d"}
```

#### News Sentiment
```
POST /api/stocks/news
Body: {"ticker": "AAPL", "days": 7}
```

#### Comprehensive Analysis
```
POST /api/analysis/comprehensive
Body: {"ticker": "AAPL"}
```

#### Portfolio Optimization
```
POST /api/portfolio/optimize
Body: {
  "tickers": ["AAPL", "MSFT"],
  "target_return": 0.10,
  "method": "sentiment"
}
```

#### Backtest
```
POST /api/portfolio/backtest
Body: {
  "tickers": ["AAPL", "MSFT"],
  "weights": [0.6, 0.4],
  "start_date": "2023-01-01",
  "end_date": "2024-01-01"
}
```

---

## Performance Optimization

### 1. Enable Caching
- Redis for API response caching
- Browser caching for static assets

### 2. Database Optimization
- Index frequently queried columns
- Implement connection pooling

### 3. API Rate Limiting
- Implement rate limiting with Flask-Limiter
- Use API key authentication

### 4. Frontend Optimization
- Code splitting with Vite
- Lazy loading for components
- Image optimization

### 5. Monitoring and Logging
- Use ELK stack for log aggregation
- Set up application monitoring with Prometheus/Grafana
- Use APM tools (New Relic, DataDog)

---

## Support and Maintenance

### Regular Maintenance Tasks
- Update dependencies: `pip list --outdated`
- Monitor API logs for errors
- Backup database regularly
- Review and optimize slow queries
- Update security patches

### Monitoring Checklist
- [ ] API health status
- [ ] Database disk usage
- [ ] Memory and CPU usage
- [ ] Response times
- [ ] Error rates
- [ ] Data freshness

---

## Additional Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [Docker Documentation](https://docs.docker.com/)
- [Vite Documentation](https://vitejs.dev/)

---

**Last Updated**: February 2024
**Version**: 1.0.0
