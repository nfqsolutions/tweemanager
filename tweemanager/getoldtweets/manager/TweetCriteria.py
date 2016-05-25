# -*- coding: utf-8 -*-


class TweetCriteria:

    def __init__(self):
        self.maxTweets = 0

    def setUsername(self, username):
        if username:
            self.username = username
        return self

    def setSince(self, since):
        if since:
            self.since = since
        return self

    def setUntil(self, until):
        if until:
            self.until = until
        return self

    def setQuerySearch(self, querySearch):
        if querySearch:
            self.querySearch = querySearch
        return self

    def setMaxTweets(self, maxTweets):
        if maxTweets:
            self.maxTweets = maxTweets
        else:
            self.maxTweets = 25
        return self

    def __repr__(self):
        return 'username: {}, since: {}, until: {}, querySearch: {}, maxTweets: {}'.format(self.username, self.since, self.until, self.querySearch, self.maxTweets)
