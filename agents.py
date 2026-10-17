from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import web_serach, scrap_url

load_dotenv()

#loading model
llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash")

#search agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_serach]
    )


#reader agent
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrap_url]
    )


#writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system","""You are a professional research analyst and report writer.
        Your task is to generate accurate, well-structured, and
        informative research reports based on the information provided.

        Structure the report as,
        - Introduction,
        - Key findings(minimum 3 well explained points)
        - Conclusion
        - Sources(list all the urls found in the research)
        
        """),
    ("human","""
        Generate a comprehensive research report using the following input.

        Research Topic:
        {topic}

        Research Information:
        {research_data}

        Be detailed, factual and professional.
""")
])

writer_chain = writer_prompt | llm | StrOutputParser()


#critic chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are a strict research report evaluator.
    Evaluate the report for accuracy, relevance, structure,
    depth, clarity, and source credibility.

    Give each criterion a score out of 10 and calculate
    the overall score out of 10.

    Briefly explain the weaknesses and suggest improvements.
    Do not assume unsupported claims are accurate.
    """),
    ("human", """
    Evaluate the following research report:

    {report}

    Return:
    1. Scores for each criterion
    2. Overall score out of 10
    3. Key weaknesses
    4. Recommended improvements
    """)
])

critic_chain = critic_prompt | llm | StrOutputParser()