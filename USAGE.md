using tweemanager:

One is assuming that [INSTALL.md]() is done.

## Simple case: Listening to the stdout.

1. Check help:
	python tweemanager -h
2. Generate a configuration file:
	python tweemanager genconfig --yes
3. Edit the configuration file (tweem_simplelistener.cfg) with proper data:
	minimal configuration contents:
4. Launch a listener:
	python tweemanager listener

## Simple case: Search to the stdout.

1. Check help:
	python tweemanager -h
2. Generate a configuration file:
	python tweemanager genconfig --yes
3. Edit the configuration file (tweem_simplesearch.cfg) with proper data:
	minimal configuration contents:
4. Launch a listener:
	python tweemanager searchtweets

## Simple case: GetOldTweets to the stdout.

1. Check help:
	python tweemanager -h
2. Generate a configuration file:
	python tweemanager genconfig --yes
3. Edit the configuration file (tweem_simplegetold.cfg) with proper data:
	minimal configuration contents:
4. Launch a listener:
	python tweemanager searchtweets

## Saving data to mongodb:

1. Check help:
	python tweemanager -h
2. Generate a configuration file:
	python tweemanager genconfig --yes
3. Edit the configuration file (tweem_listenertomongo.cfg) with proper data:
	minimal configuration contents:
4. Launch a listener:
	python tweemanager searchtweets

1. Check help:
	python tweemanager -h
2. Generate a configuration file:
	python tweemanager genconfig --yes
3. Edit the configuration file (tweem_searchtomongo.cfg) with proper data:
	minimal configuration contents:
4. Launch a listener:
	python tweemanager searchtweets

## Mapping mongo to elastic for data exploration with kibana:

TODO:

## Using package with jupyter:


