from app.chat.redis import client
import random

def random_component_by_score(component_type, component_map):
    # Make sure component_type is in ['llm', 'retriever', 'memory']
    if component_type not in ['llm', 'retriever', 'memory']:
        raise ValueError("Invalid COmponent Type. Valid Valeus are llm, memory and retriever.")
    
    # From redis, get the hash containing the sum total scores for the given commponent_type
    values = client.hgetall(f"{component_type}_score_values")

    # From redis, get the hash containing the number of times each component has been voted on
    counts = client.hgetall(f"{component_type}_score_counts")

    # Get all the valid component names from the component map
    names = component_map.keys()

    # Loop over those valid names and use them to calculate the average score for each
    # Add average score to a dictionary
    avg_scores = {}
    for name in names:
        score = int(values.get(name, 1))
        count = int(counts.get(name, 1))
        avg = score/count
        avg_scores[name] = max(avg, 0.2) # just so that if first vote of 0 makes it being excluded from the choices forever    

    # Do a weighted random selection
    sum_scores = sum(avg_scores.values())
    random_val = random.uniform(0, sum_scores)
    cumulative = 0
    for name, score in avg_scores.items():
        cumulative += score
        if random_val <= cumulative:
            return name 

def score_conversation(conversation_id: str, score: float, llm: str, retriever: str, memory: str) -> None:
    """
    This function interfaces with langfuse to assign a score to a conversation, specified by its ID.
    It creates a new langfuse score utilizing the provided llm, retriever, and memory components.
    The details are encapsulated in JSON format and submitted along with the conversation_id and the score.

    :param conversation_id: The unique identifier for the conversation to be scored.
    :param score: The score assigned to the conversation.
    :param llm: The Language Model component information.
    :param retriever: The Retriever component information.
    :param memory: The Memory component information.

    Example Usage:

    score_conversation('abc123', 0.75, 'llm_info', 'retriever_info', 'memory_info')
    """

    score = min(max(score, 0), 1) # To enusre score is always between 0 and 1

    client.hincrby('llm_score_values', llm, score) # Add the score
    client.hincrby('llm_score_counts', llm, 1)  # +1 votes, keeping count of total votes

    client.hincrby('retriever_score_values', retriever, score) # Add the score
    client.hincrby('retriever_score_counts', retriever, 1)  # Add +1 votes, keeping count of total votes

    client.hincrby('memory_score_values', memory, score) # Add the score
    client.hincrby('memory_score_counts', memory, 1)  # +1 votes, keeping count of total votes


def get_scores():
    aggregate = {"llm": {}, "retriever": {}, "memory": {}}

    for component_type in aggregate.keys():

        values = client.hgetall(f"{component_type}_score_values")
        counts = client.hgetall(f"{component_type}_score_counts")

        # Get all the valid component names from the Values Dict
        names = values.keys()

        for name in names:
            score = int(values.get(name, 1))
            count = int(counts.get(name, 1))
            avg = score/count
            aggregate[component_type][name] = [avg]
    
    return aggregate

