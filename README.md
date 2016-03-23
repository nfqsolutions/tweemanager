![alt tag](http://nfqsolutions.com/wp-content/uploads/2014/03/nfq_solutions-300x111.png)

# NFQ solutions' tweemanager

opensource solution to track and analize tweets easely

this project is at alpha stage and includes other python packages. Check requirements.txt for dependecies control.

to use the package just clone the repo
    
    $ git clone https://github.com/ekergy/tweemanager.git

create a python's virtualenv
   
    $ virtualenv -p <path/to/python2.7> .env

install requirements

type
python tweemanager --help

in a production enviroment you should install the package
python setup.py install

and use the package as:

you can find some documentation [here]()

and use the tweemanager deamon.sh as a template file.

it uses the standard File system as a standard database but you can use mongo or elastic also.

this package basicly uses tweepy package and the getoldtweeter project as base.


