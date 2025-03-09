#!/usr/bin/env python
import sys
import warnings

from datetime import datetime
#import post_automation
from crew import PostAutomation

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'job_posting_url': 'https://www.netvagas.com.br/empresa/anuncios/a1225309/cientista-de-dados-junior/v1/',
        'github_url': 'https://github.com/IanAndMendesDS',
        'personal_portfolio_url': 'https://ianandmendesds.github.io/portifolio_projetos/'
    }
    
    try:
        PostAutomation().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

run()