from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from crewai_tools import (
  FileReadTool,
  ScrapeWebsiteTool,
  MDXSearchTool,
  SerperDevTool,
  PDFSearchTool
)

load_dotenv()

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# Create Tools

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
read_resume = FileReadTool(file_path='src/post_automation/data/curriculo_ian.md')
semantic_search_resume = MDXSearchTool(mdx='src/post_automation/data/curriculo_ian.md')

pdf_rag = PDFSearchTool(pdf='src/post_automation/data/Profile.pdf')


@CrewBase
class PostAutomation():
	"""PostAutomation crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools = [scrape_tool, search_tool],
			verbose=True
		)

	@agent
	def profiler(self) -> Agent:
		return Agent(
			config=self.agents_config['profiler'],
			tools = [scrape_tool, search_tool,
             read_resume, semantic_search_resume, pdf_rag],
			verbose=True
		)
	
	@agent
	def resumer_strategist(self) -> Agent:
		return Agent(
			config=self.agents_config['resumer_strategist'],
			tools = [scrape_tool, search_tool,
             read_resume, semantic_search_resume, pdf_rag],
			verbose=True,

		)
	

	@crew
	def crew(self) -> Crew:
		"""Creates the PostAutomation crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		# Tasks 

		research_task = Task(
		description=(
			"Analyze the job posting URL provided ({job_posting_url}) "
			"to extract key skills, experiences, and qualifications "
			"required. Use the tools to gather content and identify "
			"and categorize the requirements."
		),
		expected_output=(
			"A structured list of job requirements, including necessary "
			"skills, qualifications, and experiences."
		),
		agent=self.researcher(),
		async_execution=True
		)

		profile_task = Task(
		description=(
			"Compile a detailed personal and professional profile "
			"using the GitHub ({github_url}) URLs, and personal portfolio "
			"({personal_portfolio_url}). Utilize tools to extract and "
			"synthesize information from these sources."
		),
		expected_output=(
			"A comprehensive profile document that includes skills, "
			"project experiences, contributions, interests, and "
			"communication style."
		),
		agent=self.profiler(),
		async_execution=True
		)

		# Task for Resume Strategist Agent: Align Resume with Job Requirements
		resume_strategy_task = Task(
		description=(
			"Using the profile and job requirements obtained from "
			"previous tasks, tailor the resume to highlight the most "
			"relevant areas. Employ tools to adjust and enhance the "
			"resume content. Make sure this is the best resume even but "
			"don't make up any information. Update every section, "
			"inlcuding the initial summary, work experience, skills, "
			"and education. All to better reflrect the candidates "
			"abilities and how it matches the job posting."
		),
		expected_output=(
			"An updated resume that effectively highlights the candidate's "
			"qualifications and experiences relevant to the job."
		),
		output_file="tailored_resume2.md",
		context=[research_task, profile_task],
		agent=self.resumer_strategist()
		)

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=[research_task, profile_task, resume_strategy_task ], # Automatically created by the @task decorator
			#process=Process.sequential,
			verbose=True,
			manager_llm='gpt-4o-mini',
			process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
