from crewai import Agent
from tools import yt_channel_search_tool

## create seneoir blog content writer agent
blog_researcher = Agent(
    role="Blog Researcher",
    goal="get the relevnt videe as per the given topic{topic} from the YT video channel",
    verbose=True,
    memory=True,
    backstory=(
        "Expert in understanding videos in AI, machine learning, GenI and data science. "
    ),
    tools=[yt_channel_search_tool],
    allow_delegation=True
)

## creating senior writer agent with YT tools
blog_writter = Agent(
    role="Blog Writer",
    goal="narrate compelling stories about in the video {topic} from YT channel",
    verbose=True,
    memory=True,
    backstory=(
        "with fair for simplyfying complex topics,your craft "
        "engaging narratives that captivate and educate, bringing new"
        "discoveries to light in accessible manner."
        
    ),
    tools=[yt_channel_search_tool],
    allow_delegation=True
)

