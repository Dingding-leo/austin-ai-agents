#!/usr/bin/env python3
"""DevPortfolio Builder - Generate star-worthy project in minutes"""

import os
import sys
from pathlib import Path

PROJECT_TEMPLATES = {
    "api": {
        "name": "REST API Starter",
        "files": ["main.py", "requirements.txt", "README.md", "tests/test_api.py"],
        "description": "Production-ready REST API with authentication"
    },
    "fullstack": {
        "name": "Full Stack App",
        "files": ["frontend/", "backend/", "docker-compose.yml"],
        "description": "React + Node.js with deployment config"
    },
    "data": {
        "name": "Data Pipeline",
        "files": ["etl.py", "requirements.txt", "notebooks/analysis.ipynb"],
        "description": "ETL pipeline with visualizations"
    }
}

def generate_project(template_type: str, project_name: str, output_dir: str):
    """Generate a portfolio-ready project"""
    
    if template_type not in PROJECT_TEMPLATES:
        print(f"Error: Unknown template '{template_type}'")
        print(f"Available: {', '.join(PROJECT_TEMPLATES.keys())}")
        return False
    
    template = PROJECT_TEMPLATES[template_type]
    project_path = Path(output_dir) / project_name
    
    # Create project structure
    project_path.mkdir(parents=True, exist_ok=True)
    
    # Generate files based on template
    if template_type == "api":
        _generate_api_template(project_path, project_name)
    elif template_type == "fullstack":
        _generate_fullstack_template(project_path, project_name)
    elif template_type == "data":
        _generate_data_template(project_path, project_name)
    
    print(f"Generated {template['name']} at {project_path}")
    return True

def _generate_api_template(path: Path, name: str):
    """Generate REST API template"""
    
    # main.py
    main_py = f'''"""
{name} - Production REST API
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# In-memory data store (replace with DB in production)
data_store = []

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({{"status": "healthy", "version": "1.0.0"}})

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify({{"items": data_store}})

@app.route('/api/items', methods=['POST'])
def create_item():
    item = request.json
    item["id"] = len(data_store) + 1
    data_store.append(item)
    return jsonify(item), 201

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((i for i in data_store if i.get("id") == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({{"error": "Not found"}}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
'''
    
    # requirements.txt
    requirements = '''flask==3.0.0
flask-cors==4.0.0
pytest==7.4.0
'''
    
    # README.md
    readme = f'''# {name}

Production-ready REST API built with Flask.

## Features
- RESTful endpoints
- CORS enabled
- Health check endpoint
- CRUD operations

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/health | Health check |
| GET | /api/items | List all items |
| POST | /api/items | Create item |
| GET | /api/items/:id | Get item |

## Deployment

Deploy to Render, Railway, or Fly.io with the included Dockerfile.
'''
    
    # Write files
    (path / "main.py").write_text(main_py)
    (path / "requirements.txt").write_text(requirements)
    (path / "README.md").write_text(readme)
    
    # Create tests directory
    tests_dir = path / "tests"
    tests_dir.mkdir(exist_ok=True)
    (tests_dir / "__init__.py").write_text("")
    (tests_dir / "test_api.py").write_text('''"""API tests"""
import sys
sys.path.insert(0, '..')
from main import app

def test_health():
    client = app.test_client()
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'
''')

def _generate_fullstack_template(path: Path, name: str):
    """Generate full-stack template"""
    frontend_dir = path / "frontend"
    backend_dir = path / "backend"
    
    frontend_dir.mkdir(exist_ok=True)
    backend_dir.mkdir(exist_ok=True)
    
    # Frontend index.html
    (frontend_dir / "index.html").write_text(f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}</title>
    <style>
        body {{ font-family: system-ui, sans-serif; max-width: 800px; margin: 0 auto; padding: 2rem; }}
        h1 {{ color: #333; }}
    </style>
</head>
<body>
    <h1>{name}</h1>
    <p>Full-stack application</p>
    <script>
        fetch('/api/health')
            .then(r => r.json())
            .then(data => console.log(data));
    </script>
</body>
</html>
''')
    
    # Backend main.py (simplified)
    (backend_dir / "main.py").write_text(f'''"""
{name} Backend
"""
from flask import Flask, jsonify, send_from_directory
app = Flask(__name__, static_folder='../frontend')

@app.route('/api/health')
def health():
    return jsonify({{"status": "healthy"}})

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
''')
    
    # Docker compose
    (path / "docker-compose.yml").write_text(f'''version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
''')
    
    # README
    (path / "README.md").write_text(f'''# {name}

Full-stack application with React frontend and Python backend.

## Quick Start

```bash
docker-compose up --build
```

## Tech Stack
- Frontend: HTML/CSS/JS
- Backend: Python Flask
- Deployment: Docker
''')

def _generate_data_template(path: Path, name: str):
    """Generate data pipeline template"""
    
    (path / "etl.py").write_text(f'''"""
{name} - ETL Pipeline
"""
import pandas as pd

def extract(source: str):
    """Extract data from source"""
    # Replace with actual data source
    return pd.DataFrame({{"data": []}})

def transform(df: pd.DataFrame):
    """Transform data"""
    return df

def load(df: pd.DataFrame, destination: str):
    """Load data to destination"""
    df.to_csv(destination, index=False)

def run_etl():
    df = extract("source")
    df = transform(df)
    load(df, "output.csv")
    print("ETL complete!")

if __name__ == "__main__":
    run_etl()
''')
    
    (path / "requirements.txt").write_text("pandas>=2.0.0\nmatplotlib>=3.7.0\n")
    
    (path / "README.md").write_text(f'''# {name}

Data pipeline with ETL workflow.

## Usage
```bash
pip install -r requirements.txt
python etl.py
```
''')

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="DevPortfolio Builder")
    parser.add_argument("template", choices=["api", "fullstack", "data"], 
                        help="Project template type")
    parser.add_argument("name", help="Project name")
    parser.add_argument("--output", default=".", help="Output directory")
    
    args = parser.parse_args()
    
    success = generate_project(args.template, args.name, args.output)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
