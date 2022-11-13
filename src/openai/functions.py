import os
import httpx
import configparser


# Reading config for openai auth_key
# config = configparser.ConfigParser()
# dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# openai_auth_key = os.path.join(dir_path, "openai.cfg")
# config.read(openai_auth_key)


# AUTH_KEY = config["OPENAI"]["AUTH_KEY"]

# auth_key = "Bearer " + AUTH_KEY


def auto_completions(user_query):

    # stop sequence
    stop_sequences = ["\n", "###", "input:", "##"]

    with httpx.Client() as client:
        response_gpt = client.post(
            url="https://api.openai.com/v1/completions",
            headers={
                "Authorization": "Bearer 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"
            },
            json={
                "model": "text-davinci-002",
                "prompt": user_query,
                "max_tokens": 6,
                "temperature": 0,
                "stop": "\n",
            },
        )

    textcomp_json = response_gpt.json()["choices"][0]
    # choices_text_completion = {}

    # for index,choice in enumerate(textcomp_json,1):
    #     item = 'text_completion_choice_' + str(index)
    #     choices_text_completion[item] = choice['text'][8:].strip('\n')

    # print("#---text-completion success----#")

    # return choices_text_completion

    # choices = response_gpt.json()["choices"]

    # final_list = [choice["text"][7:] for choice in choices]

    return textcomp_json["text"]



