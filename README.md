# Alix Estate Document Agent‐Based System

A lightweight Flask API that classifies and validates estate‐related documents (Death Certificates, Wills/Trusts, Property Deeds, Financial Statements, Tax Documents, Miscellaneous) using a local Ollama 3.2 LLM.

---

## Features

- **Master Router**: Receives an uploaded document, delegates to Classification → Compliance agents.  
- **Classification Agent**: Maps text to one of six estate categories.  
- **Compliance Agent**: Enforces category-specific validation rules.  
- **Client Script**: Reads sample `.txt` files and POSTs them to the API.  


---

## Prerequisites

- **Python 3.8+**  
- **Ollama CLI** (for local LLM inference)  
- (Optional) `virtualenv` or `venv` for isolation  

---

## Installing Ollama & Model

1. **Download Ollama CLI**  
   [https://ollama.com/download](https://ollama.com/download)  
2. **Verify installation**  
   ```bash
   ollama version
   ollama pull llama3.2
   ollama run llama3.2

Leave this running while you use the API.


3. Clone the repo
  ```bash
  git clone <your-repo-url>
  cd Alix
  ```


4. Create & activate a venv
  ```bash
python3 -m venv .venv
source .venv/bin/activate    # macOS/Linux
> .venv\Scripts\activate     # Windows
````

5. Install Python dependencies
  ```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
````

6. ensure your venv is active and Ollama is running
  ```bash
cd Alix/api
export FLASK_APP=app.py
python -m flask run
```

The API listens on http://127.0.0.1:5000

7. Run the client
  ```bash
cd Alix
python client.py
```

## Sends the following files located in the project document folder:

- death_cert.txt
- will_doc.txt
- financial_statement.txt
- false_death_cert.txt
- tax_document.txt
- property_deed.txt
- misc_doc.txt

and prints their JSON responses.

## Valid Death Certificate
curl -X POST http://127.0.0.1:5000/process_document \
  -H "Content-Type: application/json" \
  -d '{"documentId":"doc1","text":"STATE OF NEW YORK\nCERTIFICATE OF DEATH\nDate of death: January 1, 2023\nSigned by Registrar Helen T. Vaughn"}'


curl -X POST http://127.0.0.1:5000/process_document \
  -H "Content-Type: application/json" \
  -d '{"documentId":"doc2","text":"STATE OF NEW YORK\nCERTIFICATE OF DEATH\nThis is not a death certificate."}'



## Postman
New POST → http://127.0.0.1:5000/process_document

Headers → Content-Type: application/json

Body → raw → JSON:

{
  "documentId": "doc-will",
  "text": "Last Will and Testament of Jane Doe...\nSigned: Jane Doe\nDate: April 1, 2023"
}

Click Send, inspect the JSON response.



![alt text](image-1.png)


