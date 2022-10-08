""" Prompt formatting for GPT API calls"""

import openai
import uuid

# from transformers import GPT2TokenizerFast


class GPT3:
    def __init__(
        self,
        prompt_description=None,
        temp=0,
        best_of=1,
        n=1,
        max_tokens=10,
        engine="ada",
        frequency_penalty=0,
        presence_penalty=0,
    ):
        self.examples = {}
        self.stop_sequences = ["\n", "###", "input:", "##"]
        self.temperature = float(temp)
        self.best_of = best_of
        self.n = n
        self.max_tokens = max_tokens
        self.engine = engine
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.logit_bias = {}
        self.prompt_description = prompt_description
        # self.tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        self.count = 0

    def add_example(self, inp, out):
        example_input = inp
        example_output = out
        example_id = uuid.uuid4().hex
        self.examples[example_id] = {"input:": example_input, "output:": example_output}

    def format_examples(self):
        formatted_list = [
            self.prompt_description,
            self.stop_sequences[0],
            self.stop_sequences[1],
        ]

        for value in self.examples.values():
            list_value = (
                "input:"
                + value["input:"]
                + self.stop_sequences[0]
                + "output:"
                + value["output:"]
                + self.stop_sequences[1]
            )
            formatted_list.append(list_value)
        return "".join(formatted_list)

    def create_prompt_query(self, query=None):
        prompt_query = (
            self.format_examples()
            + self.stop_sequences[1]
            + "input:"
            + query
            + self.stop_sequences[0]
        )

        return prompt_query

    def get_example(self, example_id):
        return self.examples.get(str(example_id), "Example does not exist")

    def delete_example(self, example_id):
        del self.examples[str(example_id)]
        return True

    def get_all_examples(self):
        return self.examples

    # def token_count(self):
    #     """
    #     Gives total token count of entire prompt size which includes
    #     examples,query,max_tokens,best_of,n (Same method for calculation as openAI)
    #     """
    #     self.count = len(self.tokenizer.encode(str(self.create_prompt_query))) + (
    #         self.best_of * self.max_tokens
    #     )
    #     return self.count

    def add_logit_bias(self, negative_bias: dict, positive_bias: dict):
        self.logit_bias = {**negative_bias, **positive_bias}
        return self.logit_bias
