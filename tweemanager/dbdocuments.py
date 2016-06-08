# -*- coding: utf-8 -*-
import mongoengine
from .settings import cfgmanager

TweetsRepoStdName = "TweetsRepo"


def create_collection_name(cls):
    """
    Note: mongoengine doesn't allow to change meta directly.
    only using this implemented approach so TweetsRepoCollName
    can be set using the config file.
    """
    # global configurations:
    print(cfgmanager.MongoDBSpecs['repocollname'])
    try:
        TweetsRepoCollName = cfgmanager.MongoDBSpecs['repocollname']
        if not TweetsRepoCollName:
            raise
    except:
        TweetsRepoCollName = TweetsRepoStdName
    finally:
        return TweetsRepoCollName


class MongoDocument(mongoengine.DynamicDocument):

    """
    DynamicDocument for the mongodb insert
    """
    meta = {'collection': create_collection_name}
    id = mongoengine.LongField(primary_key=True)
    created_at = mongoengine.DateTimeField()
