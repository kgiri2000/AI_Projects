#Run openAI package
!pip install openai == 1.33.0
import os
import openai
import pandas as pd

#Define OpenAI client

client = openai.OPENAI()

#Upload the papers
