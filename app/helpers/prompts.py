import sys
from yachalk import chalk
sys.path.append("..")

import json
import ollama.client as client


def extractConcepts(prompt: str, metadata={}, model="mistral"):
    SYS_PROMPT = (
        "Your task is to extract the key concepts and their attributes mentioned in the given context. "
        "For each concept, also extract the relevant attributes such as names, roles, dates, or other properties. "
        "Extract only the most important and atomistic concepts, and break them down into simpler concepts if necessary. "
        "Categorize the concepts in one of the following categories: "
        "[event, concept, place, object, document, organisation, condition, misc].\n"
        "For each concept, identify and list their attributes.\n"
        "Format your output as a list of json objects with the following format:\n"
        "[\n"
        "   {\n"
        '       "entity": "The Concept",\n'
        '       "importance": "The contextual importance of the concept on a scale of 1 to 5 (5 being the highest)",\n'
        '       "category": "The Type of Concept",\n'
        '       "attributes": {\n'
        '           "name": "Attribute Name",\n'
        '           "value": "Attribute Value"\n'
        "       }\n"
        "   }, \n"
        "{ }, \n"
        "]\n"
    )
    
    # Generate response using the model (simulated here)
    response, _ = client.generate(model_name=model, system=SYS_PROMPT, prompt=prompt)
    
    try:
        # Parse the JSON response
        result = json.loads(response)
        
        # Add metadata if any
        result = [dict(item, **metadata) for item in result]
    except Exception as e:
        print(f"\n\nERROR ### Here is the buggy response: {response}, Error: {e}\n\n")
        result = None
    
    return result



def graphPrompt(input: str, metadata={}, model="mistral"):
    if model == None:
        model = "mistral"

    # model_info = client.show(model_name=model)
    # print( chalk.blue(model_info))

    SYS_PROMPT = (
        "You are a network graph maker who extracts terms and their relations from a given context. "
        "You are provided with a context chunk (delimited by ```) Your task is to extract the ontology "
        "of terms mentioned in the given context. These terms should represent the key concepts as per the context. \n"
        "Thought 1: While traversing through each sentence, Think about the key terms mentioned in it.\n"
            "\tTerms may include object, entity, location, organization, person, \n"
            "\tcondition, acronym, documents, service, concept, etc.\n"
            "\tTerms should be as atomistic as possible\n\n"
        "Thought 2: Think about how these terms can have one on one relation with other terms.\n"
            "\tTerms that are mentioned in the same sentence or the same paragraph are typically related to each other.\n"
            "\tTerms can be related to many other terms\n\n"
        "Thought 3: Find out the relation between each such related pair of terms. \n\n"
        "Format your output as a list of json. Each element of the list contains a pair of terms"
        "and the relation between them, like the follwing: \n"
        "[\n"
        "   {\n"
        '       "node_1": "A concept from extracted ontology",\n'
        '       "node_2": "A related concept from extracted ontology",\n'
        '       "edge": "relationship between the two concepts, node_1 and node_2 in one or two sentences"\n'
        "   }, {...}\n"
        "]"
    )

    USER_PROMPT = f"context: ```{input}``` \n\n output: "
    response, _ = client.generate(model_name=model, system=SYS_PROMPT, prompt=USER_PROMPT)
    try:
        result = json.loads(response)
        result = [dict(item, **metadata) for item in result]
    except:
        print("\n\nERROR ### Here is the buggy response: ", response, "\n\n")
        result = None
    return result
