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
