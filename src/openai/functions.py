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


def auto_completions(user_query,multi_line=False):

    user_query = user_query.rstrip()
    total_len_of_chars = len(user_query)


    # stop sequence
    stop_sequences = ["###", "input:", "##"]

    if not multi_line:

        mini_context_window = "input:Life might have wiped itself out on early Mars and that's not as absurd as it sounds because"+ "\n"+ "output:Life might have wiped itself out on early Mars and that's not as absurd as it sounds because that's sort of what happened on Earth." + "\n\n"

        user_query = "Suggest short text completions for the following incomplete sentences.\n\n"+ mini_context_window + "input:" + user_query + "\n" + "output:"

        with httpx.Client() as client:
            response_gpt = client.post(
                url="https://api.openai.com/v1/completions",
                headers={
                    "Authorization": "Bearer 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"
                },
                json={
                    "model": "text-davinci-002",
                    "prompt": user_query,
                    "max_tokens": 70,
                    "temperature": 0.7,
                    "stop": stop_sequences,
                },
            )
    
    else:
        user_query = "Suggest long text completions for the incomplete sentences with precise information without any special characters.\n\n"+ "input:" + user_query + "\n\n" + "output:"

        with httpx.Client() as client:
            response_gpt = client.post(
                url="https://api.openai.com/v1/completions",
                headers={
                    "Authorization": "Bearer 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"
                },
                json={
                    "model": "text-davinci-002",
                    "prompt": user_query,
                    "max_tokens": 300,
                    "temperature": 0.7,
                    "stop": stop_sequences,
                },
            )

    
    
    textcomp_json = response_gpt.json()["choices"][0]
    final_completion = textcomp_json["text"].lstrip("\n").rstrip("\n")
    final_completion = final_completion[total_len_of_chars:].lstrip()
    return final_completion



