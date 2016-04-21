# -*- coding: utf-8 -*-
import models
import manager

gotSearchCriteria = manager.TweetCriteria()

def getoldtweetsGenerator(SearchCriteria):
	"""
	scraping tool for the results
	using tweet search Page. It is an alternative to oficial tweeter API.
	but information return results from scraping a webpage so it depends
	on how the scraping is done. 
	"""
	for tweet in manager.TweetManager.getTweets(SearchCriteria):
		result = dict()
		yield result