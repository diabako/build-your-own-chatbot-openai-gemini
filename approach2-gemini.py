import functions_framework
import google.generativeai as genai
from flask import jsonify
from google.cloud import aiplatform
from google.cloud import storage
from google.oauth2 import service_account
import json
from google.cloud import secretmanager
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from vertexai.preview.language_models import TextEmbeddingModel


@functions_framework.http
def webhook(request):
    
    #1. Extract the user message from Dialogflow request
    request_json = request.get_json(silent=True)
    user_message = request_json.get('text', '')  
    
    # 2. Load data from our knowledge file
    faq_data = []
    bucket_name = <BUCKET-NAME> # bucket name where the knowledge document is stored
    file_name = <FILE-NAME> # knowledge file 
    service_account_details = <SERVICE-ACCOUNT-DETAILS> # service account details that have access to the file. 

    # Access credentials from Secret Manager client. I stored the service account details in secret manager
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=resource_name)

    # Load credentials from Secret Manager payload
    credentials_json = response.payload.data.decode('UTF-8')
    credentials_info = json.loads(credentials_json)
    credentials = service_account.Credentials.from_service_account_info(credentials_info)

    # Create a storage client with credentials
    client = storage.Client(credentials=credentials)

    # Get the bucket object
    bucket = client.bucket(bucket_name)

    # Access the data using the bucket and filename
    blob = bucket.blob(file_name)

    # Process data from file
    data = blob.download_as_string().decode('utf-8')
    for line in data.splitlines():
        if line.strip() and ',' in line:
            question, answer = line.split(',', 1)
            faq_data.append({'question': question.strip('\t\n\r '), 'answer': answer.strip()})
        
    faq_questions = [item['question'] for item in faq_data]  # List of questions
    faq_answers = [item['answer'] for item in faq_data]  # List of answers

    #3. Leverage Embeddings for text and cosine algorithm to get the closest answer from the user requests
    aiplatform.init(project=<PROJECT-ID>, location=<REGION>)
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko")

    # Encode the data into embeddings 
    faq_embeddings = []
    valid_indices = []
    for i, question in enumerate(faq_questions):
        if question:
            embedding = model.get_embeddings([question])[0].values
            faq_embeddings.append(list(embedding))
            valid_indices.append(i)

    user_embeddings = model.get_embeddings([user_message])[0].values

    # Perform cosine similarity and find the closest answer index
    cos_sim_array = cosine_similarity([user_embeddings], faq_embeddings)
    closest_embedding_index = np.argmax(cos_sim_array)
    closest_answer_index = valid_indices[closest_embedding_index]
    closest_answer = faq_answers[closest_answer_index]  

    # 4. Pass the user request and closest answer to Gemini model for better formatted answer
    context = f"Provide a better answer to User Question: {user_message} \n using this FAQ Answer: {closest_answer}"
    GOOGLE_API_KEY=GEMINI-API-KEY
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro') #initialize which model we want to use, here it's Gemini Pro
    response = model.generate_content(context) # sending the context to Gemini Pro
    generated_text = response.text # Extract the generated text from the response

    # 5. send the response back to dialogflow
    response_content = {
    "fulfillment_response": {
        "messages": [{
            "text": {
                "text": [generated_text]
            }
        }]
    }
    }
    response_text = jsonify(response_content)
    return response_text  # Sends the response back to Dialogflow
    
