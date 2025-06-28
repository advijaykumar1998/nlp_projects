from crewai import Crew,Process
from agents import blog_writter,blog_researcher
from tasks import research_task, writing_task

# Initialize Crew
crew = Crew(
    agents=[blog_researcher, blog_writter],
    tasks=[research_task, writing_task],
    processes=Process.sequential,
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

# start the execution
result = crew.kickoff(inputs={"topic": "AI vs ML vs DL vs Data Science"})