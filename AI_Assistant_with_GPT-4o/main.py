#This is done on datalab workbook so, I won't be able to run and I won't be able to have all the papers.
#Run openAI package
!pip install openai == 1.33.0
import os
import openai
import pandas as pd

#Define OpenAI client

client = openai.OPENAI()

#Upload the papers

# Run this
papers = pd.DataFrame({
    "filename": [
        "2405.10313v1.pdf",
        "2401.03428v1.pdf",
        "2401.09395v2.pdf",
        "2401.13142v3.pdf",
        "2403.02164v2.pdf",
        "2403.12107v1.pdf",
        "2404.10731v1.pdf",
        "2312.11562v5.pdf",
        "2311.02462v2.pdf",
        "2310.15274v1.pdf"
    ],
    "title": [
        "How Far Are We From AGI?",
        "EXPLORING LARGE LANGUAGE MODEL BASED INTELLIGENT AGENTS: DEFINITIONS, METHODS, AND PROSPECTS",
        "CAUGHT IN THE QUICKSAND OF REASONING, FAR FROM AGI SUMMIT: Evaluating LLMs’ Mathematical and Coding Competency through Ontology-guided Interventions",
        "Unsocial Intelligence: an Investigation of the Assumptions of AGI Discourse",
        "Cognition is All You Need The Next Layer of AI Above Large Language Models",
        "Scenarios for the Transition to AGI",
        "What is Meant by AGI? On the Definition of Artificial General Intelligence",
        "A Survey of Reasoning with Foundation Models",
        "Levels of AGI: Operationalizing Progress on the Path to AGI",
        "Systematic AI Approach for AGI: Addressing Alignment, Energy, and AGI Grand Challenges"
    ]
})
papers["filename"] = "papers/" + papers["filename"]
papers

#Define the fuction to upload a file to a assistance

def upload_file_for_assistance(file_path):
    uploaded_file = client.files.create(
        file = open(filpath, "rb")
        purpose = "assistants"
    )
    return uploaded_file.id

# Now we apply the upload_file_for_assistance() function to each filename in the papers dataset to upload them
#In the papers, select the filename column
#then apply upload_file_for_assistance(),
#then convert the result to list.
#Assign to uploaded_file_ids.

uploaded_file_ids = papers["filename"]\
    .apply(upload_file_for_assistance)\
    .to_list()

#Create the vectors store, associating the uploaded file IDs and naming it.
#To access tje documents and get sensible results, they need to be split up inot small chunks and added to a vector database

vstore = client.beta.vector_stores.create(
    file_ids = uploaded_file_ids,
    name = "agi_papers"

)

#Create the assistance
#The assistance needs a prompts describing how it should behave. This consists of few paragraphs of text that give GPT information
#about what role it should be talking about, and how to pharse the responses










#Define the asistant and assign to aggie
aggie = client.beta.assistants.create(
    name = "Aggie",
    instructions = assistant_promot,
    model = "gpt-4o",
    tools = [{"type": "file_search"}],
    tool_resources = {"file_search": {"vector_store_ids": [vstore.id]}}
)

#We can now use Aggie in the OpenAi developer platform

#Create a Conversation Thread

conversation = client.beta.threads.create()

#Add a user message to the conversation 
msg_what_is_Agi = client.beta.threads.message.create(
    thread_id = coversation_id,
    role = "user",
    content = "Whar is the most common definition of AGI?"
)

#To run the assistant we need event handler to make it print in the datalab workbook



#Define the function
def run_aggie():
    with client.beta.threads.runs.stream(
        thread_id = conversation.id,
        assistant_id = aggie.id,
        event_handler = EventHandler(),

    ) as stream:
        steam.until_done()

#Run the assistant

run_aggie()