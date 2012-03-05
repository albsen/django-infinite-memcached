from django.core.cache.backends import memcached
from django.utils.log import getLogger
import sys

logger = getLogger('infinite_memcache.cache.backends')

class MemcachedCache(memcached.MemcachedCache):
    def _get_memcache_timeout(self, timeout):
        """Override _get_memcache_timeout so that it accepts 0."""
        if timeout == 0: return 0
        else: return super(MemcachedCache, self)._get_memcache_timeout(timeout)

#
class PyLibMCCache(memcached.PyLibMCCache):
    """
    pylibmc memcache with infinite caching based
    """
    def _get_memcache_timeout(self, timeout):
        """Overriding _get_memcache_timeout so that it defaults to infinite"""
        if timeout == 0: return 0
        else: return super(PyLibMCCache, self)._get_memcache_timeout(timeout)

class MemcachedInfiniteCache(memcached.MemcachedCache):
    def _get_memcache_timeout(self, timeout):
        """Override _get_memcache_timeout so that it accepts 0 and defaults to infinite"""
        if timeout == 0 or timeout == None: return 0
        else: return super(MemcachedInfiniteCache, self)._get_memcache_timeout(timeout)

class PyLibMCInfiniteCache(memcached.PyLibMCCache):
    """
    pylibmc memcache with infinite caching based on:
    https://code.djangoproject.com/ticket/9595
    with one important difference, we'll always cache forever if not said otherwise!
    """
    def _get_memcache_timeout(self, timeout):
        """Overriding _get_memcache_timeout so that it defaults to infinite"""
        if timeout == 0 or timeout == None: return 0
        else: return super(PyLibMCInfiniteCache, self)._get_memcache_timeout(timeout)

    def get(self, *args, **kwargs):
        """
        pyLibMC is quite chatty about it's status - aka breaks the site a lot if memcache has trouble.
        - this should catch all possible messages and tunnel them into something
        """
        try:
            return super(PyLibMCInfiniteCache, self).get(*args,**kwargs)
        except Exception, e:
            logger.debug('PyLibMCInfiniteCache.get() raised: %s' % e, exc_info=sys.exc_info(),extra={})

    def set(self, *args, **kwargs):
        """
        pyLibMC is quite chatty about it's status - aka breaks the site a lot if memcache has trouble.
        - this should catch all possible messages and tunnel them into something
        """
        try:
            super(PyLibMCInfiniteCache, self).set(*args, **kwargs)
        except Exception, e:
            logger.debug('PyLibMCInfiniteCache.set() raised: %s' % e, exc_info=sys.exc_info(),extra={})
