# CLAUDE.md - Value Betting Platform

This file provides comprehensive guidance to Claude Code when working with the value betting platform codebase.

## Core Development Philosophy

### KISS (Keep It Simple, Stupid)
Start with the simplest solution that works. We're building a data pipeline, not a spaceship. Complexity should only be added when proven necessary through actual bottlenecks or failures.

### YAGNI (You Aren't Gonna Need It)
Don't build for hypothetical scenarios. We'll add multi-sport support when we actually need it, not because we might need it someday.

### Modular Monolith First
Start with a well-structured monolith. Microservices come later if needed. Each component should be modular enough to extract but integrated enough to work simply.

### Data First, UI Later
Focus on reliable data collection and processing. Dashboards and fancy UIs come after we have solid data pipelines.

## 🏗️ System Architecture

### Core Components

```
├── scrapers/           # Data collection layer (Scrapy)
├── airflow/           # Orchestration layer (Apache Airflow)
├── analytics/         # Strategy and analysis layer
├── storage/           # Data persistence layer (S3 + Database)
├── docker/            # Containerization
└── config/            # System configuration
```

### Technology Stack
- **Data Collection**: Scrapy 2.11.2
- **Orchestration**: Apache Airflow 2.10.5
- **Storage**: S3 (primary) + PostgreSQL/MongoDB (metadata)
- **Processing**: Apache Spark (future)
- **Containerization**: Docker & Docker Compose
- **Language**: Python 3.11+

## 📐 Design Principles

### 1. Separation of Concerns
Each component has a single, well-defined responsibility:
- Scrapers only scrape
- Airflow only orchestrates
- Analytics only analyzes
- Storage only stores

### 2. Fail Fast, Recover Gracefully
- Validate data early in the pipeline
- Log failures comprehensively
- Implement automatic retries with exponential backoff
- Never lose data - always persist raw data first

### 3. Immutable Data Pipeline
- Raw data is never modified, only transformed
- Each transformation creates a new dataset
- Maintain full audit trail from source to insight

### 4. Schema Evolution
- Design for change - betting markets evolve
- Use versioned schemas
- Backward compatibility for at least 2 versions

## 🗂️ Project Structure

```
value-betting-platform/
│
├── CLAUDE.md                    # This file - project overview
├── README.md                    # User-facing documentation
├── docker-compose.yml           # Multi-container orchestration
├── requirements.txt             # Python dependencies
├── .env.example                # Environment template
│
├── scrapers/
│   ├── CLAUDE.md               # Scraping architecture guide
│   └── odds_scraper/
│       ├── CLAUDE.md          # Spider implementation details
│       └── ...
│
├── airflow/
│   ├── CLAUDE.md              # DAG development guide
│   ├── dags/                  # Airflow DAGs
│   └── plugins/               # Custom operators
│
├── analytics/
│   ├── CLAUDE.md              # Strategy framework guide
│   ├── strategies/            # Betting strategies
│   └── backtesting/           # Historical analysis
│
├── storage/
│   ├── CLAUDE.md              # Storage patterns guide
│   ├── schemas/               # Data schemas
│   └── migrations/            # Schema migrations
│
├── config/
│   ├── CLAUDE.md              # Configuration guide
│   └── environments/          # Environment configs
│
└── docker/
    ├── CLAUDE.md              # Container guide
    └── Dockerfile             # Custom images
```

## 🚀 Development Workflow

### Local Development Setup

```bash
# 1. Clone repository
git clone <repository>
cd value-betting-platform

# 2. Create environment file
cp .env.example .env
# Edit .env with your configuration

# 3. Start infrastructure
docker-compose up -d

# 4. Verify services
docker-compose ps
# Should see: postgres, redis, airflow-*, healthy

# 5. Test a spider
docker-compose exec airflow-worker \
    scrapy crawl oddsportal_match_spider \
    -a match_url="<test_url>"
```

### Development Commands

```bash
# View logs
docker-compose logs -f [service_name]

# Execute commands in container
docker-compose exec airflow-worker bash

# Run specific spider
docker-compose exec airflow-worker \
    scrapy crawl [spider_name] -a [args]

# Trigger Airflow DAG
docker-compose exec airflow-webserver \
    airflow dags trigger [dag_id]

# Stop all services
docker-compose down
```

## 📊 Data Flow Principles

### 1. Raw → Processed → Analyzed
```
Scraped Data (raw) → Normalized Data (processed) → Insights (analyzed)
     ↓                      ↓                          ↓
   S3/raw/               S3/processed/            S3/insights/
```

### 2. Idempotent Operations
Every operation should produce the same result if run multiple times with the same input.

### 3. Time-Partitioned Storage
Data is partitioned by collection time for efficient querying:
```
s3://bucket/raw/odds/year=2025/month=01/day=15/hour=14/
```

## 🔧 Configuration Management

### Environment Variables
All configuration through environment variables. No hardcoded values.

```bash
# Data Sources
ODDSPORTAL_BASE_URL=https://www.oddsportal.com

# Storage
S3_BUCKET=value-betting-data
AWS_REGION=us-east-1

# Database (future)
DATABASE_URL=postgresql://user:pass@host:5432/db

# Orchestration
AIRFLOW_PARALLELISM=10
```

### Configuration Hierarchy
1. Environment variables (highest priority)
2. Configuration files
3. Default values (lowest priority)

## 🐛 Error Handling Philosophy

### 1. Explicit Over Implicit
```python
# ❌ Bad - Silent failure
try:
    process_odds(data)
except:
    pass

# ✅ Good - Explicit handling
try:
    process_odds(data)
except OddsProcessingError as e:
    logger.error(f"Failed to process odds: {e}", extra={"data": data})
    raise
```

### 2. Log Everything
- Every error with full context
- Every retry attempt
- Every data transformation
- Every external API call

### 3. Graceful Degradation
If one bookmaker fails, continue with others. If one match fails, continue with remaining matches.

## 📈 Performance Targets

### Current Scale (Phase 1)
- 100 concurrent matches
- <30 second value calculation
- 95% spider success rate
- <5 minute data staleness for live matches

### Future Scale (Phase 2+)
- 1000+ concurrent matches
- <10 second value calculation
- 99% spider success rate
- Real-time odds updates

## 🔒 Security Principles

### 1. Never Commit Secrets
All secrets in environment variables or secret management systems.

### 2. Principle of Least Privilege
Each component only has access to what it needs.

## 📝 Code Standards

### Python Version
Python 3.11+ for all components

### Style Guide
- Follow PEP 8
- Line length: 100 characters
- Use type hints
- Google-style docstrings

### File Size Limits
- No file over 500 lines
- No function over 50 lines
- No class over 200 lines

## 🧪 Testing Strategy

### Test Levels
1. **Unit Tests**: Individual functions/methods
2. **Integration Tests**: Component interactions
3. **End-to-End Tests**: Full pipeline validation

### Test Location
Tests live next to the code they test:
```
spider.py
test_spider.py
```

## 📚 Documentation Standards

### Documentation Hierarchy
1. **CLAUDE.md files**: Technical implementation guides for AI assistance
2. **README.md files**: User-facing documentation
3. **Inline comments**: Complex logic explanation
4. **Docstrings**: Function/class documentation

### What to Document
- **Why** over **what** - Code shows what, comments explain why
- Architecture decisions
- Non-obvious business logic
- External dependencies
- Configuration requirements

## ⚠️ Important Notes

### For Claude Code
- **NEVER modify production data directly**
- **Always test spiders with single URLs first**
- **Keep backward compatibility when updating schemas**
- **Log extensively but avoid logging sensitive data**
- **Each directory's CLAUDE.md has specific details - always check it**

### Current Development Status
- ✅ Basic scraping infrastructure
- ✅ Docker containerization
- 🔄 Airflow DAG development
- 📋 Storage layer implementation
- 📋 Analytics framework
- 📋 Strategy implementation

### Priority Order
1. Reliable data collection
2. Consistent data storage
3. Basic arbitrage detection
4. Advanced strategies
5. UI/Dashboard

## 🔍 Directory-Specific Guides

Each major directory has its own CLAUDE.md with specific details:

- **scrapers/CLAUDE.md**: Scraping patterns, spider development
- **airflow/CLAUDE.md**: DAG patterns, scheduling strategies
- **analytics/CLAUDE.md**: Strategy implementation, backtesting
- **storage/CLAUDE.md**: Data schemas, storage patterns
- **docker/CLAUDE.md**: Container configuration, optimization

Always consult the specific CLAUDE.md for the directory you're working in.

---

_This document provides high-level guidance. For implementation details, see directory-specific CLAUDE.md files._