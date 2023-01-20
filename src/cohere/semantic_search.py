# import os
# import cohere
# import numpy as np
# import altair as alt
# from annoy import AnnoyIndex
# from dotenv import load_dotenv
# from datasets import load_dataset
# load_dotenv()

# api_key = os.getenv("COHERE_API_KEY")
# co = cohere.Client(api_key)

# texts=["hello", "goodbye"]

# response = co.embed(
#   model='large',
#   texts=texts)


# # print('Embeddings: {}'.format(response.embeddings))

# search_index = AnnoyIndex(response.shape[1], 'angular')
# for i in range(len(response)):
#     search_index.add_item(i, response[i])
# search_index.build(10) # 10 trees
# search_index.save('test.ann')


# # Choose an example (we'll retrieve others similar to it)
# example_id = 92
# # Retrieve nearest neighbors
# similar_item_ids = search_index.get_nns_by_item(example_id,10,
#                                                 include_distances=True)
# # Format and print the text and distances
# results = pd.DataFrame(data={'texts': df.iloc[similar_item_ids[0]]['text'],
#                              'distance': similar_item_ids[1]}).drop(example_id)
# results

# import pandas as pd
# lst = ["White House","hospital","school"]
# lst2 =['vqLNfqIHcLx4CPyZDLl6vA', 'rQuR-9Pj26csUZN3xtbd_Q', '5fAVplNUd7AgUKGstNkN3g']

# dataset = pd.DataFrame(list(zip(lst2,lst)),columns=["ID","text"])
# print(data)

# data_list = data["RandText"]

# Get dataset
# dataset = load_dataset("trec", split="train")
# Import into a pandas dataframe, take only the first 1000 rows
# df = pd.DataFrame(dataset)
# Preview the data to ensure it has loaded correctly
# df.head(10)

# # Generate embeddings.
# response = co.embed(texts=list(df['text']),
#                   model='large',
#                   truncate='LEFT').embeddings


# print('Embeddings: {}'.format(response))


# Store embeddings in a index in Pinecone
# import pinecone
# pinecone_api_key = os.getenv("PINECONE_API_KEY")
# pinecone.init(pinecone_api_key,environment="us-west1-gcp")

# indexname = "scrible_semantic_search"
# if indexname not in pinecone.list_indexes():
#     pinecone.create_index(indexname,dimension=8,metric="cosine")

# index = pinecone.Index(indexname)

# # Transform data that needs to be indexed.
# # Format will be list of tuples [(id,[vectors],{metadata})]
# index.upsert()


# Check the dimensions of the embeddings
# embeds = np.array(response)
# embeds.shape

# Create the search index, pass the size of embedding
# search_index = AnnoyIndex(embeds.shape[1], 'angular')
# # Add all the vectors to the search index
# for i in range(len(embeds)):
#     search_index.add_item(i, embeds[i])


# search_index.build(10) # 10 trees
# search_index.save('test.ann')

# Search for a given query
# query = "the president"

# Get the query's embedding
# query_embed = co.embed(texts=[query],
#                   model="large",
#                   truncate="LEFT").embeddings

# Retrieve the nearest neighbors
# similar_item_ids = search_index.get_nns_by_vector(query_embed[0],10,
#                                                 include_distances=True)


# Format the results
# results = pd.DataFrame(data={'texts': df.iloc[similar_item_ids[0]]['text'],
#                             'distance': similar_item_ids[1]})


# print(f"Query:'{query}'\nNearest neighbors:")
# print(results)


def semantic_search(query, documents):
    from annoy import AnnoyIndex
    import pandas as pd
    import os
    import cohere
    import numpy as np
    from dotenv import load_dotenv

    load_dotenv()

    api_key = os.getenv("COHERE_API_KEY")
    co = cohere.Client(api_key)

    # Create documents mapping for sending to client
    documents_mapping = {}
    for index in range(len(documents)):
        documents_mapping[index] = documents[index]

    dataset = pd.DataFrame(documents, columns=["text"])
    df = pd.DataFrame(dataset)

    # Generate embeddings.
    response = co.embed(
        texts=list(df["text"]), model="large", truncate="LEFT"
    ).embeddings

    embeds = np.array(response)
    embeds.shape

    # Create a search index with embeddings using Annoy
    search_index = AnnoyIndex(embeds.shape[1], "angular")

    for i in range(len(embeds)):
        search_index.add_item(i, embeds[i])

    search_index.build(10)  # 10 trees
    search_index.save("test.ann")

    # Generate query embeddings
    query_embed = co.embed(texts=[query], model="large", truncate="LEFT").embeddings

    # Retrieve the nearest neighbors from index for a query
    similar_item_ids = search_index.get_nns_by_vector(
        query_embed[0], 10, include_distances=True
    )

    results_dict = {}
    normalized_score = sum(similar_item_ids[1])

    for index, score in zip(similar_item_ids[0], similar_item_ids[1]):
        if score >= 1:
            results_dict[index] = {
                "doc": documents_mapping.get(index),
                "relevance_score": 0,
            }
        else:
            results_dict[index] = {
                "doc": documents_mapping.get(index),
                "relevance_score": 100 - (round(score / normalized_score, 2) * 100),
            }

    # Add color hex for top 3 ranked docs
    sorted_data = sorted(
        results_dict.items(), key=lambda x: x[1]["relevance_score"], reverse=True
    )

    top_three = 1
    for dict_tuple in sorted_data:
        original_index = dict_tuple[0]

        if dict_tuple[1]["relevance_score"] != 0:
            if top_three == 1:
                results_dict[original_index].update({"color": "#d2f8d2"})
            elif top_three == 2:
                results_dict[original_index].update({"color": "#ffc0cb"})
            elif top_three == 3:
                results_dict[original_index].update({"color": "#ffffe0"})

            top_three += 1
        else:
            results_dict[original_index].update({"color": ""})

    return results_dict
