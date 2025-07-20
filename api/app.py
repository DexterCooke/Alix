from flask import Flask, request, jsonify
from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage
import json

app = Flask(__name__)

llm = Ollama(model="llama3.2")

TAXONOMY = {
    "Death Certificate": "01.0000-50",
    "Will or Trust": "02.0300-50",
    "Property Deed": "03.0090-00",
    "Financial Statement": "04.5000-00",
    "Tax Document": "05.5000-70",
    "Miscellaneous": "00.0000-00"
}

def query_ollama(messages):
    try:
        response = llm.chat(messages)
        return response.message.content.strip()
    except Exception as e:
        print(f"Error querying Ollama: {e}")
        return ""

def classify_document(document_id, document_text):
    system_msg = ChatMessage(
        role="system",
        content=(
            "You are an intelligent agent that classifies estate documents "
            "into exactly one of these categories (case sensitive): "
            "Death Certificate, Will or Trust, Property Deed, Financial Statement, Tax Document, Miscellaneous."
        )
    )
    user_msg = ChatMessage(
        role="user",
        content=f"Please classify this document:\n\n{document_text}\n\nReply with exactly one category name."
    )
    messages = [system_msg, user_msg]
    category_name = query_ollama(messages)

    if category_name not in TAXONOMY:
        category_name = "Miscellaneous"
    category_code = TAXONOMY[category_name]

    return {"documentId": document_id, "categoryCode": category_code, "categoryName": category_name}

def validate_document(document_id, category_code, document_text):
    category_name = next((k for k, v in TAXONOMY.items() if v == category_code), "Miscellaneous")

    if category_name == "Death Certificate":
        rules = (
            "- Must contain 'Certificate of Death'\n"
            "- Must contain 'Date of death'\n"
            "- Must contain 'Place of Death'\n"
            "- Must contain 'Full Name of Deceased'\n"
            "- Must contain 'Sex'\n"
            "- Must contain 'Age at Death'\n"
            "- Must contain 'Date of Birth'\n"
            "- Must contain 'Social Security Number'\n"
            "- Must contain 'Usual Residence'\n"
            "- Must contain 'Marital Status'\n"
            "- Must contain 'Name of Spouse'\n"
            "- Must contain 'Occupation'\n"
            "- Must contain 'Informant Name'\n"
            "- Must contain 'Relationship to Deceased'\n"
            "- Must contain 'Cause of Death'\n"
            "- Must contain 'Certifying Physician'\n"
            "- Must contain 'Date Signed'\n"
            "- Must contain 'Registrar'\n"
        )
    elif category_name == "Will or Trust":
        rules = (
            "- Must contain 'Last Will and Testament' or 'Trust Agreement'\n"
            "- Must contain the full name of the testator\n"
            "- Must include the date the document was signed\n"
            "- Must specify beneficiaries or trustees\n"
            "- Must be properly signed by the testator or trustee\n"
        )
    else:
        return {"documentId": document_id, "valid": True, "reason": "No validation required"}

    system_msg = ChatMessage(
        role="system",
        content=f"Validate this document for {category_name} compliance.\nRules:\n{rules}"
    )
    user_msg = ChatMessage(
        role="user",
        content=f"Document:\n{document_text}\n\nAnswer ONLY in JSON format: {{\"valid\": true/false, \"reason\": \"explanation if valid/invalid\"}}"
    )
    messages = [system_msg, user_msg]

    compliance_response = query_ollama(messages)

    try:
        compliance_result = json.loads(compliance_response)
    except Exception:
        compliance_result = {"valid": False, "reason": "Invalid JSON response from compliance agent"}

    # Ensure reason key exists and is a string
    if "reason" not in compliance_result:
        if compliance_result.get("valid") is True:
            compliance_result["reason"] = ""
        else:
            compliance_result["reason"] = "No reason provided."

    compliance_result["documentId"] = document_id

    return compliance_result

@app.route("/process_document", methods=["POST"])
def process_document():
    data = request.json
    document_id = data.get("documentId")
    document_text = data.get("text", "")

    classification = classify_document(document_id, document_text)
    compliance = validate_document(document_id, classification["categoryCode"], document_text)

    return jsonify({
        "documentId": document_id,
        "categoryCode": classification["categoryCode"],
        "categoryName": classification["categoryName"],
        "valid": compliance.get("valid"),
        "reason": compliance.get("reason")
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
