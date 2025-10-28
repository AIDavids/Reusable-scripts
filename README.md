\# Groq Form Data Extractor



This Python script batch-processes a folder of images (PNG, JPG, JPEG) containing filled forms. It uses the Groq API with the Llama 4 Scout vision model to perform OCR and extract the form data into simple, structured text files.



For each image (e.g., `form\_001.jpg`), a corresponding text file (e.g., `form\_001\_extracted.txt`) will be created.



\## Features



\* \*\*Batch Processing\*\*: Processes all images in a specified input directory.

\* \*\*AI-Powered OCR\*\*: Uses the Groq API for high-accuracy text and form extraction.

\* \*\*Structured Output\*\*: Saves extracted data as a simple `KEY: VALUE` list in uppercase.

\* \*\*Secure\*\*: Uses environment variables to protect your API key.



\## Setup



\### 1. Dependencies



You'll need Python 3 and a few packages. You can install the required packages using pip:



