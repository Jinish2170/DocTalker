def route_query(query):
    """
    Decides if the query needs 'Local' knowledge (Resume/Docs)
    or 'Web' knowledge (News/General Facts).
    """
    web_triggers = [
        "news", "latest", "current", "today", "price", 
        "weather", "who is", "what is", "when did",
        "search", "find", "company", "tell me about", # <--- Added these
        "networth", "stock", "vs"
    ]
    
    query_lower = query.lower()
    
    # Logic: Check keywords
    for trigger in web_triggers:
        if trigger in query_lower:
             # Exception: If "Jinish" is mentioned, FORCE LOCAL
             if "jinish" in query_lower or "resume" in query_lower:
                 return "LOCAL"
             return "WEB"
    
    return "LOCAL"