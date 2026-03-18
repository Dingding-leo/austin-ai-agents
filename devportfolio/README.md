# DevPortfolio Builder

**Generate portfolio-ready projects in minutes. Get hired faster.**

## Problem

- 60K+ tech layoffs in March 2026 (Meta: 16,000)
- Hiring managers NOT reading resumes - want projects, skills context
- Laid off devs need quick portfolio to stand out

## Solution

Automated portfolio builder that generates:
1. GitHub repository with star-worthy projects
2. Deployment guides (Render, Railway, Fly.io)
3. Technical README with design decisions

## Quick Start

```bash
# Generate a project
python generate.py api my-portfolio-project
python generate.py fullstack my-fullstack-app
python generate.py data my-data-pipeline

# Get deployment help
python deploy.py --guide render

# Generate README
python deploy.py --readme my-project --template api
```

## Templates

| Template | Description |
|----------|-------------|
| `api` | REST API with Flask, auth, CRUD |
| `fullstack` | React + Python backend |
| `data` | ETL pipeline with pandas |

## Features

- ✅ Production-ready code structure
- ✅ Unit tests included
- ✅ Deployment guides
- ✅ Professional README generator
- ✅ Free hosting support

## Deployment

Deploy to free platforms:
- [Render](https://render.com) - Free tier
- [Railway](https://railway.app) - Free tier
- [Fly.io](https://fly.io) - Free tier

## Target Users

- Laid-off developers needing quick portfolio
- Junior devs building first portfolio
- Career switchers to tech

## Status

**MVP Ready** - Core generation scripts complete
