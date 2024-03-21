# Building a Personalized Chatbot for My Website: GPT4 and Gemini Approaches

This repository contains the code and resources for building a personalized chatbot using different approaches, as described in the blog post "Building a Personalized Chatbot for My Website: Three Approaches". The code provided here focuses on Approach 1 and Approach 2.

## Approach 1: OpenAI Assistant + GCP Cloud Functions + Dialogflow

### Files

- approach1-gpt.py: The main Python code for the Cloud Function that integrates with the OpenAI assistant and handles requests from Dialogflow.
- approach1-requirements.txt: The requirements file specifies the necessary dependencies for the Cloud Function.

### Usage

1. Set up your OpenAI assistant using the OpenAI admin interface, as described in the blog post.
2. Create a new Google Cloud Function and configure it with the provided approach1-gpt.py code and approach1-requirements.txt dependencies.
3. Set up Dialogflow to call the Cloud Function and integrate the chatbot into your website, following the steps outlined in the blog post.

## Approach 2: GCP Gemini Pro + Cloud Functions + Cloud Storage

### Files

approach2-gemini.py: The main Python code for the Cloud Function that leverages GCP Gemini Pro, Cloud Functions, and Cloud Storage to build the chatbot.
approach2-requirements.txt: The requirements file specifying the necessary dependencies for the Cloud Function.

### Usage

1. Prepare your knowledge base by organizing your website's content into a structured CSV file and uploading it to Google Cloud Storage.
2. Create a new Google Cloud Function and configure it with the provided approach2-gemini.py code and approach2-requirements.txt dependencies.
3. Set up Dialogflow to call the Cloud Function and integrate the chatbot into your website, following the steps outlined in the blog post.

Please refer to the blog post for detailed explanations, tips, and troubleshooting guidance for each approach.
