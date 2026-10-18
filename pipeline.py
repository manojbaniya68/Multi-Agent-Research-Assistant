from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain


def run_research_pipeline(topic: str) -> dict:

    state = {}

    #step 1 - search agent woking
    print("="*50)
    print("Search agent is working...")
    print("="*50, "\n")

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages":[("user",f"Find recent, reliable and detailed information on : {topic}")]
    })

    state["search_results"] = (
    search_result["messages"][-1].content
    )

    if isinstance(state["search_results"], list):
        state["search_results"] = "\n".join(
            block["text"]
            for block in state["search_results"]
            if isinstance(block, dict)
            and block.get("type") == "text"
        )

    print(f"\nSearch result : \n {state['search_results']}")

    #step 2 - reader agent working
    print("\n","="*50)
    print("Reader agent is scraping top resources...")
    print("="*50)

    reader_agent = build_reader_agent()
    reader_results = reader_agent.invoke({
        "messages":[("user",
            f"""
            Research topic: {topic}

            Here are the search results:
            {state['search_results']}

            Instructions:
            1. Identify the actual URLs in the search results.
            2. Select the most relevant URL for the research topic.
            3. Use the scrap_url tool to scrape that webpage.
            4. Summarize the important information found.
            5. If no URL is available, explicitly say that no URL was provided.
            """
        )]
    })

    # Extract the final response safely
    final_message = reader_results["messages"][-1]
    content = final_message.content

    if isinstance(content, list):
        state["scraped_content"] = "\n".join(
            block["text"]
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    else:
        state["scraped_content"] = content

    print(f"Scraped content : \n{state['scraped_content']}")

    #step 3 - run write chain
    print("\n","="*50)
    print("Writer is drafting the report...")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )

    state['report'] = writer_chain.invoke({
        "topic" : topic,
        "research_data" : research_combined
    })

    print(f"Research Report : \n\n {state['report']}")

    #step 4 - run cirtic chain
    print("\n","="*50)
    print("critic is reviewing the report...")
    print("="*50)

    state['feedback'] = critic_chain.invoke({
        "report" : state['report']
    })

    print(f"Critic Report : \n {state['feedback']}")
    return state

if __name__ == "__main__":
    topic = input("Enter the research topic: ")
    run_research_pipeline(topic)



