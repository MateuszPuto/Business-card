import json
import os

CONFIG_FILE = 'config_data.json'

def prompt_simple_input(prompt, default=""):
    """Prompts for a single line of text with an optional default value."""
    return input(f"{prompt} (Default: '{default}'): ").strip() or default

def prompt_list_of_items(title, item_name, fields):
    """
    Prompts for a list of complex items (e.g., services, pricing).
    CRITICAL FIX: All generated keys are forced to lowercase snake_case 
    to match the template variables (e.g., 'Icon code' -> 'icon_code').
    """
    items = []
    print(f"\n--- Configure {title} ---")
    
    while True:
        print(f"\nAdding new {item_name} (leave blank to finish):")
        item = {}
        
        # Determine the dictionary key for the first field
        first_field_key = fields[0].lower().replace(' ', '_')
        first_field_prompt = fields[0].capitalize()
        
        # Prompt for the first field (used as the loop break)
        first_field_value = input(f"  {first_field_prompt}: ").strip()
        
        if not first_field_value:
            break
        
        item[first_field_key] = first_field_value
        
        # Prompt for remaining fields
        for field in fields[1:]:
            key = field.lower().replace(' ', '_')
            item[key] = input(f"  {field.capitalize()}: ").strip()
            
        items.append(item)
    return items

def prompt_hours_of_operation():
    """Prompts for daily operating hours."""
    print("\n--- Configure Operating Hours ---")
    hours = {}
    days = ["Mon - Fri", "Saturday", "Sunday"]
    
    for day in days:
        default_hours = "9:00 AM – 5:00 PM" if day != "Sunday" else "Closed"
        h = prompt_simple_input(f"  Hours for {day}", default_hours)
        hours[day] = h
    return hours

def generate_config_data():
    """Main function to run the questionnaire and save the JSON."""
    
    print("\n=======================================================")
    print("         Digital Business Card Configuration")
    print("=======================================================")
    
    # 1. Business Information
    business_name = prompt_simple_input("Enter Business Name", "Elite Hair Studio")
    tagline = prompt_simple_input("Enter Main Tagline", "The best cuts and color in Metropolis, booked instantly.")
    cta_primary = prompt_simple_input("Enter Primary Call-to-Action (e.g., Book Now)", "Book Your Appointment Now")
    cta_secondary = prompt_simple_input("Enter Secondary CTA (e.g., Call Us Now)", "Call to Check Availability")
    
    # 2. Section Headings (Optional, usually fixed by template, but configurable)
    headings = {
        "services": "Our Signature Services",
        "gallery": "Client Transformations",
        "pricing": "Current Price List",
        "contact": "Location & Booking"
    }
    
    # 3. Services List (Fields: name, icon_code)
    # The fields list determines the prompt text. The function converts them to lowercase snake_case.
    services = prompt_list_of_items("Services", "service", ["Name", "Icon code"])
    if not services:
        services = [{"name": "Placeholder Service", "icon_code": "default"}]
        
    # 4. Gallery Images (Fields: url, alt)
    gallery_images = prompt_list_of_items("Gallery Images", "image", ["URL", "Alt text"])
    if not gallery_images:
        gallery_images = [
            {"url": "https://placehold.co/400x300/fecaca/000?text=Style+A", "alt": "Style A", "alt_fallback": "Style A"},
            {"url": "https://placehold.co/400x300/fbcfe8/000?text=Style+B", "alt": "Style B", "alt_fallback": "Style B"}
        ]

    # 5. Pricing List (Fields: service_name, price)
    prices = prompt_list_of_items("Pricing", "price item", ["Service name", "Price"])
    if not prices:
        prices = [{"service_name": "Standard Rate", "price": "$100"}]
        
    pricing_note = prompt_simple_input("Enter Pricing Footnote", "*Prices may vary. Contact us for a quote.")

    # 6. Contact & Location
    print("\n--- Configure Contact Details ---")
    phone_formatted = prompt_simple_input("Enter Phone Number (Formatted)", "(555) 123-4567")
    phone_raw = phone_formatted.replace(" ", "").replace("(", "").replace(")", "").replace("-", "")
    email = prompt_simple_input("Enter Email Address", "book@elitehair.com")
    address_line_1 = prompt_simple_input("Enter Street Address / Suite", "456 Commerce Drive, Suite 101")
    address_line_2 = prompt_simple_input("Enter City, State, Zip", "Metropolis, CA 90210")
    map_url = prompt_simple_input("Enter Google Maps Directions Link", "https://maps.google.com/?q=456+Commerce+Drive,+Metropolis,+CA")
    map_embed_url = prompt_simple_input("Enter Google Maps Embed URL (iframe source)", "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1500!2d-118.25!3d34.05!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x80c2c62c3f8f121d%3A0x8e83b4f6e4a2e5d!2sLos%20Angeles%2C%20CA%2C%20USA!5e0!3m2!1sen!2sus!4v1634592000000!5m2!1sen!2sus")
    
    hours_of_operation = prompt_hours_of_operation()

    # 7. Assemble Final Configuration Dictionary
    config_dict = {
        "business": {
            "name": business_name,
            "tagline": tagline,
            "tagline_short": business_name, 
            "cta_primary": cta_primary,
            "cta_secondary": cta_secondary,
            "startup_name": "DigitalCard Co."
        },
        "section_headings": headings,
        "services": services,
        "gallery_images": gallery_images,
        "prices": prices,
        "pricing_note": pricing_note,
        "hours_of_operation": hours_of_operation,
        "contact": {
            "phone_raw": phone_raw,
            "phone_formatted": phone_formatted,
            "email": email,
            "address_line_1": address_line_1,
            "address_line_2": address_line_2,
            "map_url": map_url,
            "map_embed_url": map_embed_url
        }
    }
    
    # 8. Save to JSON File
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_dict, f, indent=2)
        print(f"\n=======================================================")
        print(f"✅ Configuration saved successfully to {CONFIG_FILE}!")
        print(f"Next step: Run 'python render_site.py' to generate the website.")
        print("\nNOTE: Ensure Django is installed (pip install django) before running render_site.py.")
        print("=======================================================")
    except IOError as e:
        print(f"ERROR: Could not write output file '{CONFIG_FILE}'. Details: {e}")
        
if __name__ == "__main__":
    generate_config_data()
