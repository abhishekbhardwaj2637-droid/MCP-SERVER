import os
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

def generate_reports(insights_path: str, app_name: str = "com.nextbillion.groww"):
    """
    Reads the LLM insights JSON and generates Markdown and HTML reports.
    """
    if not os.path.exists(insights_path):
        print(f"Error: Insights file not found at {insights_path}")
        return False
        
    with open(insights_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if isinstance(data, list) and len(data) > 0:
        data = data[0]
        
    clusters = data.get("clusters", [])
    if not clusters:
        print("Warning: No clusters found in the insights file. Generating empty reports.")
        
    # Setup Jinja2 environment
    templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    env = Environment(loader=FileSystemLoader(templates_dir))
    
    # Common context variables
    date_str = datetime.now().strftime("%Y-%m-%d")
    context = {
        "app_name": app_name,
        "date": date_str,
        "clusters": clusters,
        "doc_url": "https://docs.google.com/document/d/PLACEHOLDER_DOC_ID/edit" # Will be updated in Phase 4
    }
    
    # Ensure reports directory exists
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # 1. Generate Plain Text Report (since Docs MCP doesn't support Markdown formatting)
    txt_template = env.get_template('plaintext_report.jinja2')
    txt_content = txt_template.render(**context)
    txt_path = os.path.join(reports_dir, f"{app_name}_report_{date_str}.txt")
    
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(txt_content)
    print(f"Generated Plain Text report: {txt_path}")
    
    # 2. Generate HTML Email Summary
    html_template = env.get_template('email_summary.jinja2')
    html_content = html_template.render(**context)
    html_path = os.path.join(reports_dir, f"{app_name}_email_{date_str}.html")
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated HTML email summary: {html_path}")
    
    return {
        "text_path": txt_path,
        "html_path": html_path
    }

if __name__ == "__main__":
    # If run directly, try to find the most recent insights file and generate reports
    processed_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'processed')
    if os.path.exists(processed_dir):
        files = [f for f in os.listdir(processed_dir) if f.endswith('.json')]
        if files:
            files.sort(reverse=True) # Get the most recent date
            recent_file = os.path.join(processed_dir, files[0])
            print(f"Found recent insights file: {recent_file}")
            generate_reports(recent_file)
        else:
            print(f"No JSON files found in {processed_dir}")
    else:
        print(f"Processed directory not found at {processed_dir}")
