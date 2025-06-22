# 🚀 Deployment Guide

This guide covers multiple deployment options for the URL Shortener application.

## 🐳 Docker Deployment (Recommended)

### Prerequisites
- Docker
- Docker Compose

### Steps

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

2. **Access the application:**
   - API: http://localhost
   - Direct FastAPI: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs

3. **View logs:**
   ```bash
   docker-compose logs -f
   ```

4. **Stop the application:**
   ```bash
   docker-compose down
   ```

## ☁️ Render Deployment

### Prerequisites
- GitHub repository
- Render account

### Steps

1. **Connect to Render:**
   - Go to [render.com](https://render.com)
   - Connect your GitHub repository

2. **Create Web Service:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables:**
   - Set `PYTHON_VERSION` to `3.10.18`

## 🔧 Manual Server Deployment

### Prerequisites
- Linux server with Python 3.8+
- systemd (for service management)

### Steps

1. **Clone and setup:**
   ```bash
   git clone https://github.com/parthrastogicoder/Url-Shortner.git
   cd Url-Shortner
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Create systemd service:**
   ```bash
   sudo nano /etc/systemd/system/url-shortener.service
   ```

   Service file content:
   ```ini
   [Unit]
   Description=URL Shortener FastAPI App
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/Url-Shortner
   Environment="PATH=/path/to/Url-Shortner/venv/bin"
   ExecStart=/path/to/Url-Shortner/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. **Start the service:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable url-shortener
   sudo systemctl start url-shortener
   ```

## 🌐 Heroku Deployment

### Prerequisites
- Heroku CLI
- Heroku account

### Steps

1. **Login to Heroku:**
   ```bash
   heroku login
   ```

2. **Create Heroku app:**
   ```bash
   heroku create your-url-shortener-app
   ```

3. **Deploy:**
   ```bash
   git push heroku main
   ```

4. **Open the app:**
   ```bash
   heroku open
   ```

## 🔧 Local Development

### Run locally:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Run tests:
```bash
pytest -v
```

## 📊 Production Considerations

### Database
- For production, consider using PostgreSQL instead of SQLite
- Set up database backups

### Security
- Add HTTPS/TLS certificates
- Implement rate limiting
- Add authentication for admin endpoints

### Monitoring
- Set up logging
- Add health check endpoints
- Monitor application metrics

### Performance
- Add Redis for caching
- Use a CDN for static assets
- Configure load balancing for high traffic

## 🔍 Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   sudo lsof -i :8000
   sudo kill -9 <PID>
   ```

2. **Permission denied:**
   ```bash
   sudo chown -R $USER:$USER /path/to/project
   ```

3. **Module not found:**
   ```bash
   pip install -r requirements.txt
   ```

### Logs
- Check application logs: `docker-compose logs -f url-shortener`
- Check system logs: `sudo journalctl -u url-shortener -f`

## 📈 Scaling

For high-traffic applications:
- Use a load balancer (nginx, HAProxy)
- Deploy multiple instances
- Use a distributed database
- Implement caching strategies
