![alt tag](http://nfqsolutions.com/wp-content/uploads/2014/03/nfq_solutions-300x111.png)

# NFQ solutions' tweemanager

Opensource solution to track and analize tweets easely. This project is at alpha stage and includes other python packages. Check requirements.txt for dependecies control.

To use the package just clone the repo:
    
    $ git clone https://github.com/ekergy/tweemanager.git

Create a python's virtualenv:
   
    $ virtualenv -p <path/to/python2.7> .env

Upgrade pip (if required):

    $ pip install --upgrade pip

Install requirements:

    $ pip install -r requirements.txt

Type
    $ python tweemanager --help
to show the functionalities

In a production enviroment you should install the package
    $ python setup.py install

You can find some documentation [here]()

And use the tweemanager deamon.sh as a template file.

It uses the standard File system as a standard database but you can use mongo or elastic also.

This package basicly uses tweepy package and the getoldtweeter project as base.


