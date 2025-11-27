import json
from django.template import Template, Context
from django.conf import settings
import os
from django import setup # Import the setup function

# --- 1. Setup Django Settings (Minimal Requirement for Template Engine) ---
if not settings.configured:
    # Set the minimal configuration required. 
    # Importantly, we need to tell Django about TEMPLATES, even if we won't use 
    # INSTALLED_APPS, the template system checks the app registry first.
    settings.configure(
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.dirname(__file__)], # Look for templates in the current directory
        }],
        # Required to prevent the AppRegistryNotReady error when using the template system
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
        ]
    )
    # Initialize the Django environment and load the application registry
    setup() 
    # We must call setup() AFTER settings.configure()

# --- File Paths ---
CONFIG_FILE = 'config_data.json'
TEMPLATE_FILE = 'template.html'
OUTPUT_FILE = 'rendered_site.html'

def render_django_template():
    """
    Simulates the Django process of loading configuration data and rendering a template.
    """
    print(f"--- Starting Site Generation Process ---")

    # --- 2. Load the Configuration Data (Context) ---
    try:
        with open(CONFIG_FILE, 'r') as f:
            # The JSON data becomes the context dictionary for the template
            context_data = json.load(f)
        print(f"Loaded configuration data from {CONFIG_FILE} for business: {context_data['business']['name']}")
    except FileNotFoundError:
        print(f"ERROR: Configuration file '{CONFIG_FILE}' not found.")
        return
    except json.JSONDecodeError:
        print(f"ERROR: Could not parse JSON data in '{CONFIG_FILE}'. Check for syntax errors.")
        return

    # --- 3. Load the Template ---
    try:
        with open(TEMPLATE_FILE, 'r') as f:
            template_content = f.read()
    except FileNotFoundError:
        print(f"ERROR: Template file '{TEMPLATE_FILE}' not found.")
        return

    # Create the Django Template object
    # This is the line that required the Django setup() call above
    template = Template(template_content)

    # Create the Context object to pass data to the template
    # Context is what lets you access data like {{ business.name }}
    context = Context(context_data)
    
    # --- 4. Render the Final HTML ---
    final_html = template.render(context)

    # --- 5. Save the Output ---
    try:
        with open(OUTPUT_FILE, 'w') as f:
            f.write(final_html)
        print(f"SUCCESS: Site rendered and saved to {OUTPUT_FILE}")
        print("You can now view this static HTML file in a browser.")
    except IOError:
        print(f"ERROR: Could not write output file '{OUTPUT_FILE}'.")


if __name__ == "__main__":
    # In a real Django application, this logic happens inside a View function.
    # We are running it as a standalone script for demonstration.
    
    # NOTE: You need to install Django to run this script: pip install django
    # Ensure 'config_data.json' and 'template.html' are in the same directory.
    render_django_template()
