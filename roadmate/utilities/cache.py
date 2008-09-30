'''
Copyright (c) 2008, appengine-utilities project
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following
conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of the appengine-utilities project nor the names of its contributors may be used to endorse or promote
products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
'''
# main python imports
import datetime, pickle, random

# google appengine import
from google.appengine.ext import db

# Settings
DEFAULT_CACHE_EXPIRE = 60*60 # Default age of cache before auto-deleted in seconds 
CLEAN_CHECK_PERCENT = 15 # 15 percent of all requests will clean the database

class _AppEngineUtilities_Cache(db.Model):
    cid = db.StringProperty() # It's up to the application to determine the format of their cid
    createTime = db.DateTimeProperty(auto_now_add=True)
    expires = db.DateTimeProperty()
    content = db.BlobProperty()

class Cache(object):
    """
    Cache is used for storing pregenerated output and/or objects in the Big Table datastore to minimize the
    amount of queries needed for page displays. The idea is that complex queries that generate the same
    results really should only be run once. Cache can be used to store pregenerated content made from
    queries (or other calls such as urlFetch()), or the query objects themselves.  
    """
    def __init__(self):
        if random.randint(1, 100) < CLEAN_CHECK_PERCENT:
            self.__clean_cache()

    def __clean_cache(self):
        """
        __clean_cache is a routine that is run to find and delete cache items that are old. This
        helps keep the size of your over all datastore down.
        """
        queryStr = "WHERE expires < :1"
        cacheHits = _AppEngineUtilities_Cache.gql(queryStr, datetime.datetime.now())
        if cacheHits.count() > 0:
            for hit in cacheHits:
                self.delete(hit.cid)

    def write(self, cid = None, content = None, expires = None):
        """
        write adds an entry to the cache. This is public because it includes the ability
        to set an expiration time.
        """
        if cid == None:
            raise ValueError, "You must supply a cid (cache id)"
        if type(cid) != type(""):
            raise TypeError, "Cache ID must be a string"
        if content == None:
            raise ValueError, "You must include cache content"
        if expires == None:
            expires = datetime.datetime.now() + datetime.timedelta(seconds=DEFAULT_CACHE_EXPIRE)
        if type(expires) == type(1):
            expires = datetime.datetime.now() + datetime.timedelta(seconds = expires) 
        if type(expires) != datetime.datetime:
            raise TypeError, "Expiration must be a datetime type."
        if expires < datetime.datetime.now():
            raise ValueError, "Expiration must be in the future."

        cacheEntry = self.__read(cid)
        if not cacheEntry:
            cacheEntry = _AppEngineUtilities_Cache()
            cacheEntry.cid = cid
        cacheEntry.content = pickle.dumps(content) 
        cacheEntry.expires = expires 

        cacheEntry.put() 

    def set(self, key = None, value = None, expires = None):
        """
        set is an alias for write, added so the library can be used as a cache
        backend for django.
        """
        return self.write(key, value)

    def __read(self, cid = None):
        """
        read returns a cache object determined by the cid. It's set to private because
        it returns a db.Model object, and also does not handle the unpickling of objects
        making it not the best candidate for use. The special method __getitem__ is the
        preferred access method for cache data.
        """
        if cid == None:
            raise ValueError, "You must supply a cid (cache id)"
        queryStr = "WHERE cid = :1 AND expires > :2"
        cacheHits = _AppEngineUtilities_Cache.gql(queryStr, cid, datetime.datetime.now())
        if cacheHits.count() == 0:
            return None
        return cacheHits[0]

    def delete(self, cid = None):
        """
        Deletes a cache object determined by the cid.
        """
        if cid == None:
            raise ValueError, "You must supply a cid (cache id)"
        queryStr = "WHERE cid = :1"
        cacheHits = _AppEngineUtilities_Cache.gql(queryStr, cid)
        if cacheHits.count() > 0:
            for hit in cacheHits:
                db.delete(hit)
        
    def get(self, key):
        """
        get is used to return the cache content associated with the key passed.
        """
        hit = self.__read(key)
        if hit:
            return pickle.loads(hit.content)
        else:
            raise KeyError, str(key)

    def __getitem__(self, cid):
        """ 
        __getitem__ is necessary for this object to emulate a container.
        """
        return self.get(cid)

    def __setitem__(self, cid, value):
        """ 
        __setitem__ is necessary for this object to emulate a container.
        """
        return self.write(cid, value)

    def __delitem__(self, cid):
        """
        Implement the 'del' keyword
        """
        return self.delete(cid)

    def has_key(self, key):
        """
        Returns true if a cache with the key passed exists, otherwise returns false.
        """
        try:
            r = self.get(key)
        except KeyError:
            return False
        return True

    def __contains__(self, cid):
        """
        Implements "in" operator
        """
        return self.has_key(cid) 
