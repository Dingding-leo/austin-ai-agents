#!/usr/bin/env python3
"""LeadFlow - Simple lead capture and notification system"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta

DATA_FILE = Path("leads.json")

def load_leads():
    """Load leads from JSON file"""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_leads(leads):
    """Save leads to JSON file"""
    with open(DATA_FILE, "w") as f:
        json.dump(leads, f, indent=2)

# Configuration
config = {
    "notifications": {
        "enabled": True,
        "channels": ["telegram"],
    },
    "follow_ups": {
        "enabled": True,
        "delay_hours": 24,
        "message": "Hi {name}, just following up on your inquiry about {service}. Would you like to chat?"
    }
}

def add_lead(name: str, email: str, phone: str, service: str = "general"):
    """Add a new lead"""
    leads = load_leads()
    lead = {
        "id": len(leads) + 1,
        "name": name,
        "email": email,
        "phone": phone,
        "service": service,
        "created_at": datetime.now().isoformat(),
        "status": "new",
        "follow_up_sent": False
    }
    leads.append(lead)
    save_leads(leads)
    return lead

def get_leads(status: str = None):
    """Get all leads"""
    leads = load_leads()
    if status:
        return [l for l in leads if l["status"] == status]
    return leads

def send_follow_ups():
    """Send follow-up messages"""
    leads = load_leads()
    sent = []
    for lead in leads:
        if lead["status"] == "new":
            created = datetime.fromisoformat(lead["created_at"])
            if datetime.now() - created > timedelta(hours=config["follow_ups"]["delay_hours"]):
                message = config["follow_ups"]["message"].format(
                    name=lead["name"],
                    service=lead["service"]
                )
                print(f"Would send to {lead['phone']}: {message}")
                lead["follow_up_sent"] = True
                lead["status"] = "contacted"
                sent.append(lead)
    if sent:
        save_leads(leads)
    return sent

def generate_html_form():
    """Generate embeddable lead capture form"""
    
    html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Us</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               max-width: 400px; margin: 50px auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: 600; }
        input, select { width: 100%; padding: 10px; border: 1px solid #ddd; 
                        border-radius: 5px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #2563eb; color: white; 
                 border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background: #1d4ed8; }
        .success { display: none; padding: 15px; background: #dcfce7; 
                   color: #166534; border-radius: 5px; margin-top: 10px; }
    </style>
</head>
<body>
    <h2>Get in Touch</h2>
    <form id="leadForm">
        <div class="form-group">
            <label for="name">Name *</label>
            <input type="text" id="name" name="name" required>
        </div>
        <div class="form-group">
            <label for="email">Email *</label>
            <input type="email" id="email" name="email" required>
        </div>
        <div class="form-group">
            <label for="phone">Phone</label>
            <input type="tel" id="phone" name="phone">
        </div>
        <div class="form-group">
            <label for="service">Service Interest</label>
            <select id="service" name="service">
                <option value="general">General Inquiry</option>
                <option value="consulting">Consulting</option>
                <option value="development">Development</option>
                <option value="support">Support</option>
            </select>
        </div>
        <button type="submit">Submit</button>
    </form>
    <div class="success" id="success">Thanks! We'll be in touch soon.</div>
    
    <script>
        document.getElementById('leadForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            console.log('Lead submitted:', data);
            document.getElementById('leadForm').style.display = 'none';
            document.getElementById('success').style.display = 'block';
        });
    </script>
</body>
</html>'''
    return html

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="LeadFlow - SMB Lead Automation")
    parser.add_argument("--add", nargs=4, metavar=("NAME", "EMAIL", "PHONE", "SERVICE"),
                        help="Add a new lead")
    parser.add_argument("--list", action="store_true", help="List all leads")
    parser.add_argument("--form", action="store_true", help="Generate HTML form")
    parser.add_argument("--followup", action="store_true", help="Send follow-ups")
    
    args = parser.parse_args()
    
    if args.add:
        lead = add_lead(*args.add)
        print(f"Lead added: {lead['name']} ({lead['email']})")
    elif args.list:
        for lead in get_leads():
            print(f"[{lead['status']}] {lead['name']} - {lead['email']} - {lead['service']}")
    elif args.form:
        print(generate_html_form())
    elif args.followup:
        sent = send_follow_ups()
        print(f"Sent {len(sent)} follow-up messages")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
