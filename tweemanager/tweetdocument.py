# -*- coding: utf-8 -*-
import mongoengine


def create_collection_name(cls):
    """
    Note: mongoengine doesn't allow to change meta directly.
    only using this implemented approach so TweetsRepoCollName
    can be set using the config file.
    """
    # global configurations:
    from configparsermanager import CFGINFO
    try:
        TweetsRepoCollName = CFGINFO.getMongoDBSpecs('repocollname')
        if not TweetsRepoCollName:
            raise
    except:
        TweetsRepoCollName = "TweetsRepo"
    finally:
        return TweetsRepoCollName


class TweetDocument(mongoengine.DynamicDocument):

    """
    DynamicDocument for the mongodb insert
    """
    meta = {'collection': create_collection_name}
    id = mongoengine.LongField(primary_key=True)
    created_at = mongoengine.DateTimeField()
