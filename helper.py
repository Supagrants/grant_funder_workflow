def combine_data_for_scoring(*args: str) -> str:
    """
    Combines multiple strings into a single formatted string for scoring
    
    Args:
        *args: Variable number of strings to combine
        
    Returns:
        str: Combined string ready for scoring
    """
    combined = []
    for i, data in enumerate(args, 1):
        if data:  # Only add non-empty data
            combined.append(f"Analysis {i}:\n{data}\n")
    
    return "\n".join(combined)


def format_deal_memo_input(scorer_output: str, combined_analysis: str) -> str:
    """
    Formats the scorer output and analysis data for the deal memo agent
    
    Args:
        scorer_output: Dictionary containing scores and reasoning
        combined_analysis: Original combined analysis string
        
    Returns:
        str: Formatted prompt for deal memo agent
    """
    prompt = f"""
Project Analysis Summary:
{combined_analysis}

Scoring Results:
{scorer_output}



Please create a comprehensive deal memo based on the above information.
"""
    return prompt









