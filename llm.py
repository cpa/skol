import openai


def ask(data, key):
    openai.api_key = key

    prompt="I will give you data that is somewhat structured and you will output a JSON list that contains the data.\n\nInput: \n{\"You're beautiful\",\n \"It's true\",\n \"It\\'s true\"}\n Output: [\"You're beautiful\", \"It's true\", \"It\\'s true\"]\n\nInput:\nARRAY[\"You're beautiful\",\n \"It's true\",\n \"It\\'s true\"]\nOutput: [\"You're beautiful\", \"It's true\", \"It\\'s true\"]\n\nInput:" + data + "\n\nOutput:"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )

    return response
