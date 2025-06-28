from crewai import task
from tools import yt_channel_search_tool

from agents import blog_researcher, blog_writter

## reasearch task
research_task = task(
    description = (
        "identify the video {topic}"
        "get the detailed information about the video"
    ),
    expected_output = (
        "a comprehensive summary of the video with 3 paragraphs based on the topic {topic}"),
    tool = [yt_channel_search_tool],
    agent = blog_researcher,

)

## writing task
writing_task = task(
    description = (
        "get the info from the youtube channel based on the topic of {topic} and create a content for the blog" 
    ),
    expected_output = (
        "summarize the youtube channel based on the topic {topic}"),
    tool = [yt_channel_search_tool],
    agent = blog_writter,
    async_excution=False,
    output_file = "new-blog-post.md"
)