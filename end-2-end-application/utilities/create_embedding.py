import boto3
import json
import numpy as np
from pathlib import Path
from sklearn.preprocessing import normalize

endpoint_name = "<YOUR EMBEDDING MODEL ENDPOINT>"

def extract_pageindex(origin_str, sub1, sub2):
    # getting index of substrings
    idx1 = origin_str.index(sub1)
    idx2 = origin_str.index(sub2)

    # length of substring 1 is added to
    # get string from next character
    res = origin_str[idx1 + len(sub1): idx2]

    # printing result
    return res

def create_json_output(pdf_json_file_name):
    pathlist = Path("../data/extractedpages").glob('**/*.txt')
    output = []
    for path in pathlist:
        # because path is object not string
        path_in_str = str(path)
        file=open(path_in_str,"r")
        payload = file.read()
        file.close()

        page_index = extract_pageindex(path_in_str, "document-page", ".pdf")
        data = {}
        data["content"] = payload
        data["page_number"] = page_index
        data["pdf_file_path"] = path_in_str
        output.append(data)

    with open(pdf_json_file_name, 'w') as outfile:
        json.dump(output, outfile, indent=4)


def chunk_words(sequence, chunk_size):
    sequence = sequence.split()
    return [' '.join(sequence[i:i+chunk_size]) for i in range(0, len(sequence), chunk_size)]

def query_endpoint(payload):
    embeddings = []
    client = boto3.client("sagemaker-runtime", region_name="us-east-1")
    chunk_payload = chunk_words(payload, 400)
    for i, chunk in enumerate(chunk_payload):
        #print("Chunk ",i)
        #print("Content ",chunk)
        response = client.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType="application/x-text",
            Body=json.dumps(chunk),
        )    
        response = response["Body"].read().decode("utf8")
        response = json.loads(response)
        embeddings_chunk = response["embedding"]
        embeddings.append(embeddings_chunk)
    return embeddings


def parse_response(query_response):
    """Parse response and return the embedding."""
    embeddings = np.array(query_endpoint(query_response))
    #avg_embeddings = np.mean(embeddings, axis=0)
    # try max pooling of embedding vector
    avg_embeddings = np.max(embeddings, axis=0)

    avg_embeddings = avg_embeddings.reshape(1, -1)
    # normalization before inner product
    avg_embeddings = normalize(avg_embeddings, axis=1, norm='l2')
    return np.squeeze(avg_embeddings)


def create_embedding_output(pdf_json_file_name, output_file_name):
    create_json_output(pdf_json_file_name)
    with open(pdf_json_file_name, 'r') as f:
        data = json.load(f)

    for page_index, page in enumerate(data):
        if page_index % 30 == 0:
            print(f'Processing page {page_index}')
        #print(page_index)
        #print(data[page_index]["content"])
        data[page_index]["embedding"] = parse_response(data[page_index]["content"]).tolist()
        #if page["page_number"] == "349":
        #    content = data[page_index]["content"]

    with open(output_file_name, 'w') as f:
        # Use json.dump to write pdfText to the file
        json.dump(data, f, indent=4)


