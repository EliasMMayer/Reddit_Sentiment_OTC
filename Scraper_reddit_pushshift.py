#!/usr/bin/env python
# coding: utf-8


import requests
from datetime import datetime
import traceback
import time
import json
import sys
import pandas as pd

url = "https://api.pushshift.io/reddit/{}/search?limit=1000&sort=desc&{}&before="


# Comments
poReScrap = pd.DataFrame(columns=['ID','Author','Score', 'Creation date','comment body','replies', 'depth', 'parentID','awards'])

# Submissions
poReScrapSubmissions = pd.DataFrame(columns=['title','id','author','score',  'num_crossposts','media_only','selftext', 'permalink', 'Creation date'])



def downloadRedditData(object_type, sreddit, mdat, mxdat):
    
    #Defines boundries (datewise) which content should be scraped 
    
	minDate = mdat
	maxDate = mxdat  
    
    #Target subreddit
    
	subreddit = sreddit  
	filter_string = f"subreddit={subreddit}"

    #Safes df's
	dfList = list()
    
	#Init vars
	count = 0
	minD = minDate
	initD = maxDate

	# Create date objects
	initD_obj = datetime.strptime(initD, '%Y-%m-%d')
	minD_obj = datetime.strptime(minD, '%Y-%m-%d')

	#Define start time (max) from which we iterate backwards  
	previous_epoch = int(initD_obj.timestamp())    
    
	while initD_obj > minD_obj:
        
		new_url = url.format(object_type, filter_string)+str(previous_epoch)
		json_text = requests.get(new_url, headers={'User-Agent': "Post downloader by /u/DerGalant"})
		time.sleep(2)  # pushshift has a rate limit, if we send requests too fast it will start returning error messages
        
		try:
			json_data = json_text.json()
		except json.decoder.JSONDecodeError:
			time.sleep(4)
			continue

		if 'data' not in json_data:
			break
		objects = json_data['data']
		if len(objects) == 0:
			break

		for object in objects:
			previous_epoch = object['created_utc'] - 1
			count += 1
            
			if object_type == 'comment':
					try:
						#Vars for extraction
						score = str(object['score']) #see reddit API - for up and downvotes 
						dat = datetime.fromtimestamp(object['created_utc']).strftime("%Y-%m-%d")
						bod = object['body'].encode(encoding='ascii', errors='ignore').decode()
						author = str(object['author'])
						ID = str(object['id'])
						link_id = str(object['link_id'])
						parentID = str(object['parent_id'])
						#Update year
						initD_obj = datetime.fromtimestamp(previous_epoch)

						#Fill into df
						poReScrap = pd.DataFrame({'ID':[ID],'Author':[author],'Score': [score],  'Creation date': [dat],'comment body': [bod], 'parentID': [parentID],'link_id': [link_id]})
						dfList.append(poReScrap)
                                
					except Exception as err:
						print(f"Couldn't print comment: https://www.reddit.com{object['permalink']}")
						print(traceback.format_exc())
					#print("Saved {} {}s through {}".format(count, object_type, datetime.fromtimestamp(previous_epoch).strftime("%Y-%m-%d")))

                
			elif object_type == 'submission':
					if object['is_self']:
							if 'selftext' not in object:
									continue
					try:
						#Vars for extraction

						title = str(object['title'])                         
						ID = str(object['id']) 
						author = str(object['author'])                         
						score = str(object['score']) #see reddit API - for up and downvotes                        
						num_crossposts = str(object['num_crossposts']) 
						media_only = "" #str(object['media_only'])
						selftext = str(object['selftext']) 
						permalink = str(object['permalink'])  
                        
						dat = datetime.fromtimestamp(object['created_utc']).strftime("%Y-%m-%d")
                        
						#Update year
						initD_obj = datetime.fromtimestamp(previous_epoch)
						
						#Fill into df
						poReScrapSubmissions = pd.DataFrame({'title': [title], 'id': [ID], 'author': [author],  'score':[score],                                                  'num_crossposts':[num_crossposts], 'media_only':[media_only],                                                'selftext':[selftext],                                                'permalink':[permalink],'Creation date': [dat]})
                        
						dfList.append(poReScrapSubmissions)
                        
                        
					except Exception as err:
							print(f"Couldn't print post: {object['url']}")
							print(traceback.format_exc())

	dfx = pd.concat(dfList, ignore_index = True,sort = False)
	naming_CV_sub = initD+"_"+minD+"_"+str(object_type)+"_"+str(subreddit)+".csv"
	dfx.to_csv(naming_CV_sub, index =  False)
    
	return(dfx)

downloadRedditData("submission", "tlss", '2018-01-01', '2022-11-01')

downloadRedditData("comment", "tlss", '2018-01-01', '2022-11-01')






