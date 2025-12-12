from openai import OpenAI


def ask(data, key):
    client = OpenAI(api_key=key)

    prompt = (
        'I will give you data that is somewhat structured and you will output a JSON list that contains the data.\n\nInput: \n{"You\'re beautiful",\n "It\'s true",\n "It\\\'s true"}\n Output: ["You\'re beautiful", "It\'s true", "It\\\'s true"]\n\nInput:\nARRAY["You\'re beautiful",\n "It\'s true",\n "It\\\'s true"]\nOutput: ["You\'re beautiful", "It\'s true", "It\\\'s true"]\n\nInput:'
        + data
        + "\n\nOutput:"
    )
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0,
    )

    return response.choices[0].text
