#!/usr/bin/env python
# coding: utf-8


import praw
import pandas as pd
# Append score to  comments, manually do for each file, adjust paths 

df = pd.read_csv('')

df["Score"] = 0  # Init the score varaible

#general

reddit = praw.Reddit(client_id='', client_secret='', user_agent='')
    
for index, row in df.iterrows():
    cmt = reddit.comment(row["ID"])
    row["Score"] = cmt.score

df.to_csv("general_comments_score_UAPC_added.csv", index =  False)

