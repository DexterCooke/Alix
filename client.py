import requests
import os

API_URL = "http://127.0.0.1:5000/process_document"

def send_document(document_id, file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    headers = {"Content-Type": "application/json"}
    payload = {"documentId": document_id, "text": text}

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        if response.ok:
            print(f"Document {document_id} processed successfully:")
            print(response.json())
        else:
            print(f"Failed to process document {document_id}: {response.status_code} {response.reason}")
            print("Response content:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error processing document {document_id}: {e}")

if __name__ == "__main__":
    send_document("doc1", "./documents/death_cert.txt")
    send_document("doc2", "./documents/will.txt")
    send_document("doc3", "./documents/miscellaneous.txt")
    send_document("doc4", "./documents/false_death_cert.txt")
    send_document("doc5", "./documents/financial_statement.txt")
    send_document("doc6", "./documents/tax_doc.txt")
    send_document("doc7", "./documents/property_deed.txt")    
    
