import tiktoken


def calculate_tokens(text, doc_id, completion, redis_db=None):
    encoder = tiktoken.get_encoding("gpt2")

    # BPE (byte pair encoding) tokeniser results in a list of int values
    bpe_count_text = encoder.encode(text)
    bpe_count_completion = encoder.encode(completion)
    total_tokens_count = len(bpe_count_text) + len(bpe_count_completion)

    # Add to existing count and store in redis for each unique document
    if redis_db:
        existing_count = redis_db.hget(name=doc_id, key="tokens_consumed")
        if existing_count:
            total_tokens_count = int(existing_count.decode()) + total_tokens_count

        redis_db.hset(name=doc_id, key="tokens_consumed", value=total_tokens_count)
