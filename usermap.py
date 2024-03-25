import random
import string

class PasswordError(Exception):
    """Custom error to be used in UserMap when wrong password is given for a user."""
    def __init__(self, message):
        self.message = message
    def __repr__(self):
        return f"PasswordError: {repr(self.message)}"

class UserRecord:
    def __init__(self, username, password):
        self.username = username
        self.salt = ''.join(random.choices(string.ascii_letters + string.digits, k = 8))
        self.password_hash = hash(self.salt + password)
    
    def __repr__(self):
        """Returns a string represention of a UserRecord."""
        return f"UserRecord: {self.username}"

class UserMap:
    def __init__(self):
        self._num_buckets = 8
        self._max_load_factor = .75
        self._len = 0
        self._buckets = [None for i in range(self._num_buckets)] # was self._nbBuckets

    def __repr__(self):
        """Returns a string representation of the internal storage of UserMap."""
        return "\n".join(f"bucket{b}: {rec}" for b, rec in enumerate(self._buckets))

    def __len__(self):
        """Returns the number of records in the database"""
        return self._len

    def __getitem__(self, username):
        """Returns the salted password and username of a given username. If the username is not in the hashmap, return KeyError"""
        for bucket in self._buckets:
            if bucket and bucket.username == username:
                return bucket
        raise KeyError(username)

    def __contains__(self, username):
        """Returns True is the username is in the User Map and False if it is not"""
        bucket_idx = hash(username) % self._num_buckets
        for bucket in self._buckets:
            if bucket and bucket.username == username:
                return True
        return False

    def add_user(self, username, password):
        """Adds a new user and password. If the username is already in the records, return RuntimeError. 
        If a hash collision occurs use linear probing
        If the size of the usermap exceeds the max load factor, call _double() to rehash the list"""
        bucket_idx = hash(username) % self._num_buckets
        if username in self: raise RuntimeError
        og_bucket = bucket_idx
        while self._buckets[bucket_idx] is not None and self._buckets[bucket_idx].username != username and bucket_idx!= og_bucket:
            bucket_idx += 1
            bucket_idx = bucket_idx % self._num_buckets
        if self._buckets[bucket_idx] is None:
            self._buckets[bucket_idx] = UserRecord(username, password)
            self._len +=1 
        if len(self) >= (self._num_buckets*self._max_load_factor):
            self._double()
    
    def update_password(self, username, current_password, new_password):
        """Updates the password of the username. If the username is not in the hashmap, raise PasswordError"""
        bucket_idx = hash(username) % self._num_buckets
        if username not in self: raise KeyError(username)
        salt_password = self._buckets[bucket_idx].salt + current_password
        hash_current_password = hash(salt_password)
        if hash_current_password == self._buckets[bucket_idx].password_hash:
            self._buckets[bucket_idx].password_hash = hash(self._buckets[bucket_idx].salt + new_password)
        else:
            raise PasswordError('Wrong Password')
    def _double(self):
        """doubles the number of buckets"""
        self._num_buckets = 2*self._num_buckets
        new_buckets = [None for i in range(self._num_buckets)]
        for i in self._buckets:
            if i is not None:
                new_idx = hash(i.username) % self._num_buckets
                new_buckets[new_idx] = UserRecord(i.username, i.password)