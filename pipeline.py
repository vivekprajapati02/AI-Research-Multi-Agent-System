from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

def run_research_pipeline(topic: str) -> dict:

    state = {}

    # search agent working
    print("\n"+ " ="*50)
    print(f"Step 1: Searching for information on the topic: '{topic}'")
    print("="*50 + "\n")

    # Step 1: Search for information
    search_agent = build_search_agent()
    search_results = search_agent.invoke({
        "messages": [("user", f"Search for recent and reliable information on the topic: '{topic}'")] 
    })

    state['search_results'] = search_results['messages'][-1].content  # Store the search results in the state
    print(f"Search Results:\n{state['search_results']}\n")

    # Step 2: Scrape the URLs from the search results
    print("\n"+ " ="*50)
    print(f"Step 2: Scraping URLs from search results")
    print("="*50)
    
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
                      f"Based on the following results about '{topic}', "
                      f"please extract the URLs and scrape the content from each URL for deeper reading. "
                      f"Search results:\n{state['search_results'][:800]}")]
    })

    state['scraped_contents'] = reader_result['messages'][-1].content  # Store the scraped contents in the state
    print(f"Scraped Contents:\n{state['scraped_contents']}\n")

    #step 3: writer chain
    print("\n"+ " ="*50)
    print(f"Step 3: Writer is drafting a report ...")
    print("="*50)

    research_combine = (
        f"Search Results:\n{state['search_results']}\n\n"
        f"Detailed Scraped Contents:\n{state['scraped_contents']}"
    )

    state['report'] = writer_chain.invoke({
        "topic": topic,
        "research": research_combine
    })

    print("\n Final Report:\n", state['report'])

    #step 4: critic chain
    print("\n"+ " ="*50)
    print(f"Step 4: Critic is reviewing the report ...")
    print("="*50)

    state['feedback'] = critic_chain.invoke({
        "report": state['report'],
    })

    print("\n Critic report:\n", state['feedback'])

    # return state['report'], state['feedback']
    return state


if __name__ == "__main__":
    topic = input("Enter a research topic: ")
    run_research_pipeline(topic)
