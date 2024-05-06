import pandas as pd
import os
import re
from tqdm import tqdm
import numpy as np
import requests
import os
import pandas as pd
import argparse
from tqdm import tqdm


def select_reviews_to_label(datapath, filter):
    """
    This function identifies the set of reviews we want to label. It allows to filter for a specific year and label accordingly.
    It return (1) the reviews we want to label, (2) their ids, (3) the loaded reviews dataframe

    datapath: string pointing to the unannotated reviews dataset
    filter: Integer that is 0 if we want to label everything otherwise should be a year between 2018 and 2024
    """
    assert filer == 0 or (filter >=2018 and filter <= 2024)
    reviews_to_label = pd.read_csv(datapath)
    if filter!=0: reviews_to_label = reviews_to_label[reviews_to_label.year==filter]
    reviews = reviews_to_label.review.tolist()
    reviews_id = reviews_to_label.review_id.tolist()

    return reviews, reviews_id, reviews_to_label



def store_files_before_label(reviews, reviews_id, folder_name):

    """
    This function stores in a folder all the reviews we want to label. This is necessary because 
    (1) we want to keep track of what we labelled and (2) this is a necessary step to use the gptzero api

    reviews: list of the reviews we want to store
    reviews_id: list of the ids identifying the reviews
    folder_name: name of the folder where we store the data
    """

    os.makedirs(folder_name, exist_ok=True)
    for i, review in enumerate(reviews):
        review_id = reviews_id[i]
        file_path = os.path.join(folder_name, f"{review_id}.txt")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(review)

    print(f"Files have been written in the '{folder_name}' folder.")




def file_predict(files,  api_key):

    """
    This function calls the GPTZero api and obtains the label for each review. It returns the respose
    which is a json file containing all the information about the labelled reviews. We obtain the probabilities
    of a document to be ai, mixed or human classified

    files: list 

    """

    base_url='https://api.gptzero.me/v2/predict'
    url = f'{base_url}/files'
    headers = {
        'Accept': 'application/json',
        'X-Api-Key': api_key
    }
    response = requests.post(url, headers=headers, files=files)
    return response

def format_output(all_responses, reviews_df, final_data_path):

    """
    This function formats the output merging the entire dataframe of the reviews with the labels
    provided via the calls to GPTZero API
    """

    results = []
    for idx, response in enumerate(all_responses):
        try:
            for resp in response[1]["documents"]: #these are 50 labelled documents
                results.append(resp)
        except KeyError as e:
            print(idx)
            
    files = [f.split(".tx")[0] for f in files]
    for idx, r in enumerate(results):
        r["review_id"]=files[idx]

    class_probs = []
    for r in results:
        class_probs.append([r["review_id"], r["class_probabilities"]["ai"], r["class_probabilities"]["human"], r["class_probabilities"]["mixed"]])
    class_probs = pd.DataFrame(class_probs, columns=["review_id", "ai", "human", "mixed"])

    fulldata = pd.merge(reviews_df, class_probs, on="review_is", how="inner")
    fulldata.to_csv(final_data_path)

    




def gptzero_labelling(folder, api_key):
    files_to_send = []
    files = os.listdir(folder)
    # Loop through the files and organize them into lists of 50 files each
    for i in range(0, len(files), 50):
        chunk = files[i:i+50]  # Get the next chunk of 50 files (or fewer if there are fewer than 50 files remaining)
        chunk_to_send = [('files', (f'{f}', open(os.path.join(folder, f), 'rb'))) for f in chunk]
        files_to_send.append(chunk_to_send)

    all_responses = []
    missed = []
    successful = []
    for idx, f in enumerate(tqdm(files_to_send, total=len(files_to_send))):
        if idx>=250 and idx%250==0: time.sleep(3600)
        try:
            res = file_predict(f, api_key).json()
            all_responses.append([f,res])
            successful.append([idx,f])
        except Exception as e:
            missed.append([idx, f])
    return all_responses, missed




def main(args):

    filter_=args.filter
    data_to_label_path = args.data_to_label_path
    storing_folder = args.storing_folder
    api_key = args.api

    reviews, reviews_id, reviews_df = select_reviews_to_label(data_to_label_path, filter=filter_)
    store_reviews_before_label(reviews, reviews_id, folder_name=storing_folder)
    all_responses, missed = gptzero_labelling(folder=storing_folder, api_key=api_key)
    format_output(all_responses, reviews_df, final_data_path)
     





if __name__ == '__main__':

    parser = argparse.ArgumentParser()


    #directories
    parser.add_argument("--data_to_label_path", type=str, default="../data/reviews_iclr_2018_2024.csv.zip")
    parser.add_argument("--storing_folder", type=str, default="reviews")
    parser.add_argument("--final_data_path", type=str, default="../data/reviews_iclr_2018_2024_annotated.csv.zip")
    parser.add_argument("--filter", type=int, default=0)
    parser.add_argument("--api_key", type=str)

    args = parser.parse_args()


    main(args)