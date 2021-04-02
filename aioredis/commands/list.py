from aioredis.util import _NOTSET, wait_ok


class ListCommandsMixin:
    """List commands mixin.

    For commands details see: http://redis.io/commands#list
    """

    def blpop(self, key, *keys, timeout=0, encoding=_NOTSET):
        """Remove and get the first element in a list, or block until
        one is available.

        :raises TypeError: if timeout is not int
        :raises ValueError: if timeout is less than 0
        """
        if not isinstance(timeout, int):
            raise TypeError("timeout argument must be int")
        if timeout < 0:
            raise ValueError("timeout must be greater equal 0")
        args = keys + (timeout,)
        return self.execute(b'BLPOP', key, *args, encoding=encoding)

    def brpop(self, key, *keys, timeout=0, encoding=_NOTSET):
        """Remove and get the last element in a list, or block until one
        is available.

        :raises TypeError: if timeout is not int
        :raises ValueError: if timeout is less than 0
        """
        if not isinstance(timeout, int):
            raise TypeError("timeout argument must be int")
        if timeout < 0:
            raise ValueError("timeout must be greater equal 0")
        args = keys + (timeout,)
        return self.execute(b'BRPOP', key, *args, encoding=encoding)

    def brpoplpush(self, sourcekey, destkey, timeout=0, encoding=_NOTSET):
        """Remove and get the last element in a list, or block until one
        is available.

        :raises TypeError: if timeout is not int
        :raises ValueError: if timeout is less than 0
        """
        if not isinstance(timeout, int):
            raise TypeError("timeout argument must be int")
        if timeout < 0:
            raise ValueError("timeout must be greater equal 0")
        return self.execute(b'BRPOPLPUSH', sourcekey, destkey, timeout,
                            encoding=encoding)

    def lindex(self, key, index, *, encoding=_NOTSET):
        """Get an element from a list by its index.

        :raises TypeError: if index is not int
        """
        if not isinstance(index, int):
            raise TypeError("index argument must be int")
        return self.execute(b'LINDEX', key, index, encoding=encoding)

    def linsert(self, key, pivot, value, before=False):
        """Inserts value in the list stored at key either before or
        after the reference value pivot.
        """
        where = b'AFTER' if not before else b'BEFORE'
        return self.execute(b'LINSERT', key, where, pivot, value)

    def llen(self, key):
        """Returns the length of the list stored at key."""
        return self.execute(b'LLEN', key)

    def lpop(self, key, *, encoding=_NOTSET):
        """Removes and returns the first element of the list stored at key."""
        return self.execute(b'LPOP', key, encoding=encoding)

    def lpush(self, key, value, *values):
        """Insert all the specified values at the head of the list
        stored at key.
        """
        return self.execute(b'LPUSH', key, value, *values)

    def lpushx(self, key, value):
        """Inserts value at the head of the list stored at key, only if key
        already exists and holds a list.
        """
        return self.execute(b'LPUSHX', key, value)

    def lrange(self, key, start, stop, *, encoding=_NOTSET):
        """Returns the specified elements of the list stored at key.

        :raises TypeError: if start or stop is not int
        """
        if not isinstance(start, int):
            raise TypeError("start argument must be int")
        if not isinstance(stop, int):
            raise TypeError("stop argument must be int")
        return self.execute(b'LRANGE', key, start, stop, encoding=encoding)

    def lrem(self, key, count, value):
        """Removes the first count occurrences of elements equal to value
        from the list stored at key.

        :raises TypeError: if count is not int
        """
        if not isinstance(count, int):
            raise TypeError("count argument must be int")
        return self.execute(b'LREM', key, count, value)

    def lset(self, key, index, value):
        """Sets the list element at index to value.

        :raises TypeError: if index is not int
        """
        if not isinstance(index, int):
            raise TypeError("index argument must be int")
        return self.execute(b'LSET', key, index, value)

    def ltrim(self, key, start, stop):
        """Trim an existing list so that it will contain only the specified
        range of elements specified.

        :raises TypeError: if start or stop is not int
        """
        if not isinstance(start, int):
            raise TypeError("start argument must be int")
        if not isinstance(stop, int):
            raise TypeError("stop argument must be int")
        fut = self.execute(b'LTRIM', key, start, stop)
        return wait_ok(fut)

    def rpop(self, key, *, encoding=_NOTSET):
        """Removes and returns the last element of the list stored at key."""
        return self.execute(b'RPOP', key, encoding=encoding)

    def rpoplpush(self, sourcekey, destkey, *, encoding=_NOTSET):
        """Atomically returns and removes the last element (tail) of the
        list stored at source, and pushes the element at the first element
        (head) of the list stored at destination.
        """
        return self.execute(b'RPOPLPUSH', sourcekey, destkey,
                            encoding=encoding)

    def rpush(self, key, value, *values):
        """Insert all the specified values at the tail of the list
        stored at key.
        """
        return self.execute(b'RPUSH', key, value, *values)

    def rpushx(self, key, value):
        """Inserts value at the tail of the list stored at key, only if
        key already exists and holds a list.
        """
        return self.execute(b'RPUSHX', key, value)

   def lpos(self, key,value, rank=None, count=None, maxlen=None,encoding=_NOTSET):
        """The command returns the index of matching elements inside a Redis list.
        By default, when no options are given, it will scan the list from head to tail,
        looking for the first match of "element".
        If the element is found, its index (the zero-based position in the list) is returned.
        Otherwise, if no match is found, NULL is returned.
        """
        if rank is not None and not isinstance(rank,int):
            raise TypeError('rank argument must be int')
        if  count is not None and not isinstance(count,int):
            raise TypeError('count argument must be int')
        if  maxlen is not None and not isinstance(maxlen,int):
            raise TypeError('maxlen argument must be int')

        if  rank is None and count is None and maxlen is None:
            return self.execute(b'LPOS',key,value)

        if rank is not None and count is None and maxlen is None :
            return self.execute(b'LPOS',key,value,b'RANK',rank,encoding=encoding)
        if rank is None and count is not None and maxlen is None :
            return self.execute(b'LPOS',key,value,b'COUNT',count,encoding=encoding)
        if rank is None and count is None and maxlen is not None :
            return self.execute(b'LPOS',key,value,b'MAXLEN',maxlen,encoding=encoding)

        if rank is not None and count is not None and maxlen is None:
            return self.execute(b'LPOS',key,value,b'RANK',rank, b'COUNT',count,encoding=encoding)
        if rank is not None and count is None and maxlen is not None:
            return self.execute(b'LPOS',key,value, b'RANK',rank,b'MAXLEN',maxlen, encoding=encoding)
        if rank is  None and count is not None and maxlen is not None:
            return self.execute(b'LPOS',key,value, b'COUNT',count,b'MAXLEN',maxlen,encoding=encoding)

        if rank is not None and count is not None and maxlen is not None:
            return self.execute(b'LPOS',key,value, b'RANK',rank,b'COUNT',count,b'MAXLEN',maxlen,encoding=encoding)

    def lmove(self, sourcekey, destkey, source_is_left, dest_is_left,encoding=_NOTSET):
        """Atomically returns and removes the first/last element
        (head/tail depending on the wherefrom argument) of the
        list stored at source, and pushes the element at the
        first/last element (head/tail depending on the whereto argument)
        of the list stored at destination.
        """
        if not isinstance(source_is_left, bool):
            raise TypeError('source_left_true_right_false argument must be bool')
        if not isinstance(dest_is_left, bool):
            raise TypeError('dest_left_true_right_false argument must be bool')
        leftright1 = b'LEFT' if source_is_left else b'RIGHT'
        leftright2 = b'LEFT' if dest_is_left else b'RIGHT'
        return self.execute(b'LMOVE',sourcekey,destkey,leftright1,leftright2,encoding=encoding )

    
