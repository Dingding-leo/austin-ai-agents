#!/usr/bin/env python3
"""Deploy portfolio project to free hosting platforms"""

import os
import sys
import subprocess
from pathlib import Path

DEPLOY_GUIDES = {
    "render": {
        "name": "Render (Free)",
        "url": "https://render.com",
        "steps": [
            "1. Push code to GitHub",
            "2. Go to render.com and connect GitHub",
            "3. Select your repository",
            "4. Configure: Build Command: 'pip install -r requirements.txt', Start Command: 'python main.py'",
            "5. Click Deploy"
        ]
    },
    "railway": {
        "name": "Railway",
        "url": "https://railway.app",
        "steps": [
            "1. Install Railway CLI: npm i -g @railway/cli",
            "2. Login: railway login",
            "3. Init: railway init",
            "4. Deploy: railway up"
        ]
    },
    "fly": {
        "name": "Fly.io",
        "url": "https://fly.io",
        "steps": [
            "1. Install Fly CLI",
            "2. Login: fly auth login",
            "3. Launch: fly launch",
            "4. Deploy: fly deploy"
        ]
    }
}

def show_deploy_guide(platform: str):
    """Show deployment guide for platform"""
    if platform not in DEPLOY_GUIDES:
        print(f"Unknown platform: {platform}")
        print(f"Available: {', '.join(DEPLOY_GUIDES.keys())}")
        return
    
    guide = DEPLOY_GUIDES[platform]
    print(f"\n{'='*50}")
    print(f"Deploy to {guide['name']}")
    print(f"{'='*50}")
    print(f"URL: {guide['url']}\n")
    
    for step in guide['steps']:
        print(step)
    print()

def create_github_readme(project_name: str, template: str) -> str:
    """Generate professional README for portfolio"""
    
    template_descriptions = {
        "api": "REST API with authentication, CRUD operations, and production-ready structure",
        "fullstack": "Full-stack application with modern frontend and robust backend",
        "data": "Data pipeline with ETL workflow and visualization capabilities"
    }
    
    readme = f"""# {project_name}

{template_descriptions.get(template, "")}

## 🚀 Live Demo

[Deployed URL]

## 📁 Project Structure

```
project/
├── src/              # Source code
├── tests/            # Unit tests
├── docs/             # Documentation
└── README.md
```

## 🛠 Tech Stack

- Language: Python
- Framework: Flask
- Testing: pytest

## 📋 Features

- Production-ready structure
- Unit tests included
- Deployment ready

## 🔧 Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/{project_name}.git
cd {project_name}

# Install dependencies
pip install -r requirements.txt

# Run locally
python main.py
```

## 🧪 Testing

```bash
pytest tests/
```

## 📝 API Documentation

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/health | Health check |
| GET | /api/items | List items |
| POST | /api/items | Create item |

## 🚢 Deployment

This project is ready for deployment to:
- [Render](https://render.com)
- [Railway](https://railway.app)
- [Fly.io](https://fly.io)

## 📄 License

MIT

## 👤 Author

[Your Name]

## 🌟 Show your support

Give a ⭐️ if this project helped you!
"""
    return readme

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="DevPortfolio Deploy Helper")
    parser.add_argument("--guide", choices=list(DEPLOY_GUIDES.keys()), 
                        help="Show deployment guide")
    parser.add_argument("--readme", help="Generate README for project")
    parser.add_argument("--template", default="api", help="Template type")
    
    args = parser.parse_args()
    
    if args.guide:
        show_deploy_guide(args.guide)
    elif args.readme:
        print(create_github_readme(args.readme, args.template))
    else:
        print("DevPortfolio Deploy Helper")
        print("\nUsage:")
        print("  --guide render    Show Render deployment guide")
        print("  --readmy NAME    Generate README for project")

if __name__ == "__main__":
    main()
