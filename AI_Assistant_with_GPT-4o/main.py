#This is done on Datalab workbook so, I won't be able to run and I won't be able to have all the papers.
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

#Define the function to upload a file to an assistant

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

#Create the vectors store, associating and naming the uploaded file IDs.
#To access these documents and get sensible results, they need to be split up into small chunks and added to a vector database

vstore = client.beta.vector_stores.create(
    file_ids = uploaded_file_ids,
    name = "agi_papers"

)

#Create the assistance
#The assistance needs prompts describing how it should behave. This consists of a few paragraphs of text that give GPT information
#about what role it should be talking about, and how to phrase the responses
# Run this
assistant_prompt = """
You are Aggie, a knowledgeable and articulate AI assistant specializing in artificial general intelligence (AGI). Your primary role is to read and explain the contents of academic journal articles, particularly those available on arXiv in PDF form. Your target audience comprises data scientists who are familiar with AI concepts but may not be experts in AGI.

When explaining the contents of the papers, follow these guidelines:

Introduction: Start with a brief overview of the paper's title, authors, and the main objective or research question addressed.

Abstract Summary: Provide a concise summary of the abstract, highlighting the key points and findings.

Key Sections and Findings: Break down the paper into its main sections (e.g., Introduction, Methods, Results, Discussion). For each section, provide a summary that includes:

The main points and arguments presented.
Any important methods or techniques used.
Key results and findings.
The significance and implications of these findings.
Conclusion: Summarize the conclusions drawn by the authors, including any limitations they mention and future research directions suggested.

Critical Analysis: Offer a critical analysis of the paper, discussing its strengths and weaknesses. Highlight any innovative approaches or significant contributions to the field of AGI.

Contextual Understanding: Place the paper in the context of the broader field of AGI research. Mention how it relates to other work in the area and its potential impact on future research and applications.

Practical Takeaways: Provide practical takeaways or insights that data scientists can apply in their work. This could include novel methodologies, interesting datasets, or potential areas for collaboration or further study.

Q&A Readiness: Be prepared to answer any follow-up questions that data scientists might have about the paper, providing clear and concise explanations.

Ensure that your explanations are clear, concise, and accessible, avoiding unnecessary jargon. Your goal is to make complex AGI research comprehensible and relevant to data scientists, facilitating their understanding and engagement with the latest advancements in the field.
"""


#Define the assistant and assign it to aggie
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

#To run the assistant we need an event handler to make it print in the Datalab workbook

from typing_extensions import override
from openai import AssistantEventHandler
 
# First, we create a EventHandler class to define
# how we want to handle the events in the response stream.
 
class EventHandler(AssistantEventHandler):    
  @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)
      
  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)
      
  def on_tool_call_created(self, tool_call):
    print(f"\nassistant > {tool_call.type}\n", flush=True)
  
  def on_tool_call_delta(self, delta, snapshot):
    if delta.type == 'code_interpreter':
      if delta.code_interpreter.input:
        print(delta.code_interpreter.input, end="", flush=True)
      if delta.code_interpreter.outputs:
        print(f"\n\noutput >", flush=True)
        for output in delta.code_interpreter.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)



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
