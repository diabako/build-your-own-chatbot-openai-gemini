import functions_framework
import openai
from flask import jsonify

@functions_framework.http
def webhook(request):

    openai.api_key = <OPENAI API KEY>
    openai.organization = <ORGANIZATION ID>
    assistant_id = <ASSISTANT ID>

    request_json = request.get_json(silent=True)

    print("Request JSON:", request_json)

    text = request_json.get('text', '')  # Get the user message from 'text'

    # Creating a thread
    thread = openai.beta.threads.create()
    
    # Sending a message to the thread
    openai.beta.threads.messages.create(
        thread_id=thread.id, 
        role="user", 
        content=text
    )

    # Running the assistant
    run = openai.beta.threads.runs.create(
        thread_id=thread.id, 
        assistant_id=assistant_id,
    )

    # Wait for the run to complete
    while run.status in ["queued", "in_progress"]:
        run = openai.beta.threads.runs.retrieve(
            thread_id=thread.id, 
            run_id=run.id,
        )

    # Getting the response
    response = openai.beta.threads.messages.list(
        thread_id=thread.id, 
        order="asc"
    )
    response_content = {
    "fulfillment_response": {
        "messages": [{
            "text": {
                "text": [response.data[-1].content[0].text.value]
            }
        }]
    }
    }
    response_text = jsonify(response_content)
    return response_text  # Sends the response back to Dialogflow
