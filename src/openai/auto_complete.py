import os

import httpx
from langchain.chains import LLMChain
from langchain.llms.loading import load_llm
from langchain.prompts.prompt import PromptTemplate
from string import punctuation
from src.utils.helpers import calculate_tokens

# Load LLM from config file
file_path = os.getcwd() + "/src/openai/llm_config.yaml"
llm = load_llm(file_path)


def format_sentences(data):
    """This function splits the data based on '.'"""
    splitted_data = data.split(".")
    last_incomplete_sentence = None
    formatted_data = []

    if splitted_data[-1]:
        # This condition means the sentence is incomplete and requires an autocompletion.
        last_incomplete_sentence = splitted_data.pop()

    for sentence in splitted_data:
        # chop the complete sentence into 30/70 ratio of completion.
        len_of_sentence = int(len(sentence) * 0.3)
        if len_of_sentence > 0:
            input_sentence = sentence[:len_of_sentence]
            output_sentence = sentence[len_of_sentence:]
            formatted_data.append(
                {"input": input_sentence, "output": input_sentence + output_sentence}
            )
        else:
            pass

    return formatted_data, last_incomplete_sentence


# def auto_complete_engine(data, redis=None):

#     if redis:
#         formatted_data, incomplete_sentence = format_sentences(data)

#     prompt_template = PromptTemplate(
#         input_variables=["input", "output"],
#         template="Complete the following incomplete sentences with context aware completions. \n\n input:{input}\noutput:{output}",
#     )

#     final_prompt = FewShotPromptTemplate(
#         examples=formatted_data,
#         example_prompt=prompt_template,
#         suffix="input:{input}",
#         input_variables=["input"],
#     )

#     chain = LLMChain(llm=llm, prompt=final_prompt)

#     if incomplete_sentence:
#         auto_completion = chain.run(incomplete_sentence)
#     else:
#         # random_sentence_starters = [""]
#         auto_completion = chain.run("The")

#     # Clean the response from GPT3
#     if "output:" in auto_completion:
#         auto_completion = auto_completion[8:]

#     if incomplete_sentence:
#         auto_completion = auto_completion[len(incomplete_sentence) + 1 :]

#     return auto_completion


def auto_complete_engine(data, doc_id, redis=None):

    # Ingest in redis and maintain a state
    if redis:
        store_in_redis = redis.set(doc_id, data)

    prompt_template = PromptTemplate(
        input_variables=["text"],
        template="Provide text completion for the following incomplete sentences if there is no starting sentence then create one of its own based on what is written before.\n\n{text}",
    )

    # Run the autocompletion chain with text
    chain = LLMChain(llm=llm, prompt=prompt_template)
    auto_completion = chain.run(data)
    if "output:" in auto_completion:
        auto_completion = auto_completion[8:]

    return auto_completion


async def auto_completions(data, doc_id, background_task, cursor_position, redis=None):

    data = data.rstrip()

    # This condition happens if user starts typing in between the text so we check with cursor position
    if cursor_position and cursor_position < len(data):
        data = data[:cursor_position].rstrip()

    # stop sequence
    stop_sequences = ["##", "\n\n\n", "---", "-----"]
    prompt_template = "Provide text completion for the following incomplete sentences if there is no starting sentence then create one of its own based on what is written before.\n\n{0}".format(
        data
    )

    async with httpx.AsyncClient() as client:
        response_gpt = await client.post(
            url="https://api.openai.com/v1/completions",
            headers={
                "Authorization": "Bearer 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"
            },
            json={
                "model": "text-davinci-003",
                "prompt": prompt_template,
                "max_tokens": 20,
                "temperature": 0.7,
                "stop": stop_sequences,
            },
        )

    if response_gpt.json().get("error"):
        return ""

    textcomp_json = response_gpt.json()["choices"][0]["text"]

    # Remove any special characters in autocompletion
    for index in range(len(punctuation)):
        if punctuation[index] in textcomp_json:
            char_index = textcomp_json.index(punctuation[index])
            textcomp_json = textcomp_json[:char_index]
        continue

    # TODO improve the logic of how tokens are being calculated only account for generated tokens
    # dont count the prompt or previous tokens.

    # Calculate and store tokens in redis (background task)
    completion = textcomp_json
    background_task.add_task(
        calculate_tokens,
        text=prompt_template,
        completion=completion,
        doc_id=doc_id,
        redis_db=redis,
    )

    return textcomp_json.lstrip()
