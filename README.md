# DevOps Pipeline for Task Management Application

A multi-service application demonstrating DevOps best practices including containerization, orchestration, monitoring, security scanning, and incident management.

## Application Architecture 

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │────▶│   Backend   │────▶│  PostgreSQL │
│  (Port 3000)│     │  (Port 5000)│     │  (Port 5432)│
└─────────────┘     └─────────────┘     └─────────────┘
       │                    │                    │
       └────────────────────┴────────────────────┘
                            │
                   ┌────────▼────────┐
                   │   Prometheus    │
                   │  (Port 9090)    │
                   └────────┬────────┘
                            │
                   ┌────────▼────────┐
                   │    Grafana      │
                   │  (Port 3001)    │
                   └─────────────────┘
```

## Getting started

### Prerequisites
- Docker & Docker Compose
- Git
- [Trivy](https://trivy.dev/latest/getting-started/installation/) (for security scanning)
- Postgres

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/pepportat/Devops_Final.git
   cd DevOps_Final
   ```
   You may want to test the app parts separately, in that case, you must install all the packages listed in the 
   requirements.txt file.


2. **Configure environment variables**
- The database needs environment variables, all listed in the docker_compose.yml file.
- Add the necessary variables in a .env file in the root directory.
```
POSTGRES_USER = your_user
POSTGRES_PASSWORD = your_password
POSTGRES_DB = database_name
```

3. **Start the application stack**
   ```bash
   docker-compose up --build
   ```

4. **Access the services**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3001 (admin/admin)
   - Adminer: http://localhost:8080

5. **Scanning with Trivy**

- To use Trivy, you can install it or follow the instructions linked above
- Then run the following command (I had problems with encoding, so I had to use this command)
```bash
 trivy image [image name]  --format table --no-progress --quiet --output .\reports\trivy\[destination_file].txt
```

Trivy will scan the selected image for vulnerabilities.

## Monitoring Implementation

### Prometheus Configuration
- Scrapes metrics from:
  - Backend Flask application (custom metrics)
  - Node Exporter (system metrics)
  - Prometheus itself

### Grafana Dashboards
1. **Flask Application Metrics**
   - Request rate by endpoint
   - Response time percentiles
   - Error rates
   - Status code distribution
   - CPU and Memory Usage
   - Application uptime

2. **System Metrics** (via Node Exporter)
   - CPU usage
   - Memory utilization
   - Disk I/O
   - Flask App statistics


## Security Implementation

### Secrets Management
- Database credentials stored in `.env` file
- `.env` file is git-ignored
- Environment variables injected at runtime
- No hardcoded secrets in source code

### Security Best Practices Applied
-  Non-root user in containers
-  Official base images from Docker Hub
-  Regular security scanning
-  Network isolation between services
-  Minimal container images (Alpine-based)

## Incident Response

### Simulated Incidents
1. **Database Failure**
   ```bash
   docker kill devops_db
   ```
You can cause a simulated incident with killing one of the core containers 
(db, backend, frontend), 
which will cause the application to fail, depending on what your standards 
are for a running application

Post-Mortem included in pdf document along with all required screenshots
```
DevOps_Final/
├── backend/
│   ├── app.py              
│   ├── db_connection.py    
│   ├── Dockerfile         
│   └── requirements.txt    
├── frontend/
│   ├── index.html          
│   └── Dockerfile         
├── monitoring/
│   ├── prometheus/
│   │   └── prometheus.yml  # Prometheus configuration
│   └── grafana/
│       └── dashboards/     # Grafana dashboard JSONs
├── reports/       # Trivy scan results
├── docker-compose.yml      # Service orchestration
├── .env                    # Environment variables
├── .gitignore
└── README.md              

```

## Tools Used

- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Backend**: Python Flask with Prometheus metrics
- **Frontend**: Static HTML/JS
- **Database**: PostgreSQL 17
- **Monitoring**: Prometheus + Grafana
- **Security**: Trivy vulnerability scanner
- **Metrics Collection**: Node Exporter, prometheus-flask-exporter


##  Fixes to potential problems

### Common Issues I had

1. **Prometheus can't scrape backend**
   ```bash
   # Check network connectivity
   docker exec devops_prometheus wget -qO- http://backend:5000/metrics
   ```

2. **Database connection errors**
   ```bash
   # Check database logs
   docker logs devops_db
   # Verify environment variables
   docker exec devops_backend env | grep DB_
   ```

3. **Grafana dashboards empty**
   - Import a dashboard or create on from scratch
     - if you wish to add the one i used, the necessary json file is included 
     in the dashboards directory.
   - Verify Prometheus is running
   - Check datasource configuration
   - Ensure metrics are being scraped


