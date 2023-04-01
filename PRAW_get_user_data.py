#!/usr/bin/env python
# coding: utf-8

import praw
import csv
import os
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def fetch_user_info(reddit, author_name):
    retries = 2
    while retries > 0:
        try:
            redditor = reddit.redditor(author_name)
            user_info = {
                "username": redditor.name,
                "created_utc": redditor.created_utc,
            }
            return user_info
        
            if count % 100 == 0:
                print(f"Processed {count} users")
                
        except Exception as e:
            #print(f"Error fetching data for user: {author_name}, Error: {e}, Retries left: {retries}")
            retries -= 1
            time.sleep(4)
    return None

def save_to_csv(df, file_number):
    output_file = f"output_{file_number}.csv"
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

reddit = praw.Reddit(client_id='', client_secret='', user_agent='') # Data

# Read input CSV file - file to find users 
input_file = ""
df = pd.read_csv(input_file)

# Extract author names from the input CSV
author_names = df["Author"].unique()

# Fetch user information for each author using parallel processing
with ThreadPoolExecutor() as executor:
    user_infos = list(executor.map(lambda author_name: fetch_user_info(reddit, author_name), author_names))

