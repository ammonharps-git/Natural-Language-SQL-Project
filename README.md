# Natural Language SQL Project
## Description
This database models a very basic architechure for a resturant's order taking system. 

This script requires a `config.json` file that contains the values for "openaiKey" and "orgId" in order to interact with the OpenAI ChatGPT API. 

## Picture of Schema

![[Natural Language SQL Diagram]]

## Working Sample Question

```json
{
  "question": "How many people placed orders on October 5th?",
  "sql": "SELECT COUNT(DISTINCT customer_id) AS num_people\nFROM Orders\nWHERE order_date = '2024-10-05';\n",
  "query_results": "[(1,)]",
  "friendly_gpt_response": "On October 5th, we had one person who placed an order at the restaurant. It's great to see that we had someone enjoying our food that day!",
  "error": "None"
}
```

## Failing Sample Question

```json
{
  "question": "Which distinct customers spent more than 50 dollars on an order?",
  "sql": "SELECT DISTINCT customer_id\nFROM Orders\nWHERE total_amount > 50;\n",
  "query_results": "[(6,)]",
  "friendly_gpt_response": "It looks like we found one distinct customer who spent more than $50 on an order! Specifically, this customer has the ID 6. If you have any other questions about the orders or need more details, feel free to ask!",
  "error": "None"
}
```

Although this attempt doesn't totally fail since it does return a correct result, it was implied that the user would like the name of the person returned, not their customer_id. 

Files containing many more examples can be found in the following files:
- `response_single_domain_double_shot.json`
- `response_zero_shot.json`

## Prompting Strategies

I tried both single-domain and zero=shot strategies. Both approaches are relatively consistent, although occasionally the zero-shot strategy appears to miss minor contextual details that would be implied to a human user. Overall, most results were correctly formatted and returned valid queries for the job at hand.
