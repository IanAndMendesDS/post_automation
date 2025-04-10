#!/usr/bin/env python
import sys
import warnings

from datetime import datetime
from crew import PostAutomation

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        'job_posting_url': 'https://autoglassadministrativo.gupy.io/jobs/8581261',
        'github_url': 'https://github.com/IanAndMendesDS',
        'personal_portfolio_url': 'https://ianandmendesds.github.io/portifolio_projetos/'
    }
    
    try:
        PostAutomation().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

run()