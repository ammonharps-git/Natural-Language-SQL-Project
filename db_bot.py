# Created by Ammon Harps 2024

from openai import OpenAI
import os
import sqlite3
import json
import re


def get_path(file_name):
    return os.path.join(os.path.dirname(__file__), file_name)


def execute(query):
    return cursor.execute(query).fetchall()


def get_gpt_response(content):
    stream = openAiClient.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": content}],
        stream=True,
    )
    responses = []
    for section in stream:
        if section.choices[0].delta.content is not None:
            responses.append(section.choices[0].delta.content)
    return "".join(responses)


def trim_sql(content):
    match = re.match(r'```\s*sql\s*(.*)\s*```', content)
    if match is not None:
        return match.group(1)
    print("(trim_sql didn't find anything to trim.)")      # testing
    return content


if __name__ == '__main__':
    # Starting message
    print("Started bot!")

    # Set paths
    db_path = get_path("db.sqlite")
    initialize_path = get_path("initialize.sql")

    # Delete previous db
    if os.path.exists(db_path):
        os.remove(db_path)

    # Get new connection and cursor
    conn = sqlite3.connect(db_path)  # create new db
    cursor = conn.cursor()

    # Initialize tables and table data
    with (open(initialize_path) as file):
        initialize_script = file.read()
    cursor.executescript(initialize_script)

    # Set up OpenAI client
    config_path = get_path("config.json")
    print("Getting config file from:", config_path)      # testing
    with open(config_path) as file:
        config = json.load(file)
    openAiClient = OpenAI(
        api_key=config["openaiKey"],
        organization=config["orgId"]
    )

    # Define strategies
    only_sql_statement = "Please provide a sqlite select statement that answers the question provided. Please only respond with sqlite syntax and nothing else. Ignore all errors."
    strategies = {
        "zero_shot": initialize_script + only_sql_statement,
        "single_domain_double_shot": (initialize_script +
                                      "What is the average cost of an order?" +
                                      " \nSELECT AVG(total_amount)\nFROM Orders;\n " +
                                      only_sql_statement)
    }

    # Define questions
    questions = [
        "What are the names of the people that ordered from the restaurant on October 1st?",
        "How many people placed orders on October 5th?",
        "Which customers spent more than 50 dollars on an order?",
        "What are the phone numbers of each person that spent less than two dollars?",
        "What is the average cost of an order?"
    ]

    # For each strategy, test each question
    for strategy in strategies:
        responses = {"strategy": strategy, "prompt_prefix": strategies[strategy]}
        results = []
        for question in questions:
            print("Question:", question)                    # testing
            error = "None"
            try:
                gpt_sql = trim_sql(get_gpt_response(strategies[strategy] + " " + question))
                print("ChatGPT sql:", gpt_sql)              # testing
                query_results = str(execute(gpt_sql))
                print("Query results:", query_results)      # testing
                friendly_prompt = "I asked you about orders from a restaurant. Your response was \"" + query_results + "\" Please summarize this data in a friendly way as if you are explaining to someone who has not seen it before."
                friendly_gpt_response = get_gpt_response(friendly_prompt)
                print("ChatGPT friendly response:", friendly_gpt_response)

                # store results
                results.append({
                    "question": question,
                    "sql": gpt_sql,
                    "query_results": query_results,
                    "friendly_gpt_response": friendly_gpt_response,
                    "error": error
                })
            except Exception as e:
                print("ERROR!", e)
        responses["results"] = results

        # Store our responses in a new file
        with open(get_path(f"response_{strategy}.json"), "w") as output_file:
            json.dump(responses, output_file, indent=2)

    cursor.close()
    conn.close()
    print("Finished!")