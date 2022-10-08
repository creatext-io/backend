import os
import httpx
import configparser


# Timeout config for httpx client
timeout_conf = httpx.Timeout(connect_timeout=5, read_timeout=None, write_timeout=5)

# Reading config for openai auth_key
config = configparser.ConfigParser()
dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
openai_auth_key = os.path.join(dir_path, "openai.cfg")
config.read(openai_auth_key)


AUTH_KEY = config["OPENAI"]["AUTH_KEY"]

auth_key = "Bearer " + AUTH_KEY


async def Auto_Completion_api(user_query):
    query = user_query

    # stop sequence
    stop_sequences = ["\n", "###", "input:", "##"]

    async with httpx.AsyncClient(timeout=timeout_conf) as client:
        response_gpt = await client.post(
            url="https://api.openai.com/v1/engines/ada/completions",
            headers={"Authorization": auth_key},
            json={
                "prompt": query,
                "temperature": 0.6,
                "max_tokens": 40,
                "stop": stop_sequences,
                "n": 1,
                "frequency_penalty": 0.4,
                "stream": False,
            },
        )

    textcomp_json = response_gpt.json()["choices"]

    # choices_text_completion = {}

    # for index,choice in enumerate(textcomp_json,1):
    #     item = 'text_completion_choice_' + str(index)
    #     choices_text_completion[item] = choice['text'][8:].strip('\n')

    # print("#---text-completion success----#")

    # return choices_text_completion

    choices = response_gpt.json()["choices"]

    final_list = [choice["text"][7:] for choice in choices]

    return final_list
