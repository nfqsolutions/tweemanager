![alt tag](http://nfqsolutions.com/wp-content/uploads/2014/03/nfq_solutions-300x111.png)

# NFQ solutions' tweemanager

Opensource solution to track and analize tweets easely. This project is at alpha stage and includes other python packages. Check requirements.txt for dependecies control. You should add also 

To use the package just clone the repo:
    
    $ git clone https://github.com/ekergy/tweemanager.git

Create a python's virtualenv:
   
    $ virtualenv -p <path/to/python2.7> .env

Activate the virtual env:
   
    $ source  .env/bin/activate

Upgrade pip (if required):

    $ pip install --upgrade pip

Install requirements:

    $ pip install -r requirements.txt

Type
    $ python tweemanager --help
to show the functionalities

In order to start using this packages, you need to have a config file. A model can be generated:

    $ python tweemanager gendonfig
    
Then, you have to fill the fields in the file with your own data.

In a production enviroment you should install the package
    $ python setup.py install

It uses elasticsearch as a standard database, but you can use mongo or another data file system.

This package basicly uses tweepy package and the getoldtweeter project as base.
You can find some documentation about tweepy [here](http://docs.tweepy.org/en/v3.5.0/)
You can find some documentation about GetOldTweets [here](https://github.com/Jefferson-Henrique/GetOldTweets-python)
