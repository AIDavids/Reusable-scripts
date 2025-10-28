import os
import base64
import json
from PIL import Image
from groq import Groq
from dotenv import load_dotenv  # --- CHANGED ---: Added dotenv to load environment variables

# --- CHANGED ---: Load variables from a .env file (explained in README)
load_dotenv()

# --- Client Setup ---
# --- CHANGED ---: Replaced the hard-coded key with an environment variable
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY environment variable not set. Please create a .env file and add it.")

client = Groq(api_key=api_key)

def encode_image(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_form_data(base64_image):
    # --- PROMPT MODIFIED ---
    # This prompt now asks for a simple text format, not JSON.
    system_prompt = """
    You are an OCR and information extraction tool. Your task is to extract data from images of physical forms.
    
    Instructions:
    1. Extract all readable fields and their corresponding values from the form.
    2. Format the output as a simple, flat text list.
    3. Each field and its value should be on a new line in the format: FIELD_NAME: VALUE
    4. Make sure all extracted text (both the field name and the value) is in UPPERCASE.
    5. If a field is empty, not readable, or not filled in, use NULL (e.g., "EMAIL ADDRESS: NULL").
    6. Do NOT output JSON. Do NOT make up or hallucinate data. Only extract what is visibly present.
    """

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        # --- RESPONSE_FORMAT REMOVED ---
        # We removed the line: response_format={"type": "json_object"}
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Please extract the data from this filled form and output as a simple key: value text list."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}", "detail": "high"}}
                ]
            }
        ],
        temperature=0.0,
    )

    return response.choices[0].message.content

def process_images(read_path, write_path):
    os.makedirs(write_path, exist_ok=True)

    for filename in os.listdir(read_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Processing {filename}...")
            file_path = os.path.join(read_path, filename)
            base64_img = encode_image(file_path)
            try:
                # --- FILE HANDLING MODIFIED ---
                
                # 1. This variable now contains plain text, not a JSON string.
                extracted_text = extract_form_data(base64_img)
                
                # 2. We no longer need json.loads()
                
                # 3. The output file extension is changed to .txt
                output_file = os.path.join(write_path, filename.rsplit('.', 1)[0] + '_extracted.txt')
                
                # 4. We use a simple f.write() instead of json.dump()
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(extracted_text)
                    
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# ==== CONFIG ====
# --- CHANGED ---: Swapped hard-coded paths for relative paths.
# This tells the script to look for an 'images' folder and 'output_text' folder
# in the same directory where the script is run.
read_path = "images"
write_path = "output_text"

print(f"Starting processing...")
print(f"Reading from: {os.path.abspath(read_path)}")
print(f"Writing to: {os.path.abspath(write_path)}")

process_images(read_path, write_path)

print("Processing complete.")