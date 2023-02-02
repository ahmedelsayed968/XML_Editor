class Dictionary:
    """
    A class that implements a dictionary-like object, allowing the user to store, access, and manipulate key-value pairs.
    """
    def __init__(self):
        self._keys = []
        self.values = []

    @property
    def keys(self):
        return self._keys

    def add(self, key, value):
        """
        Adds a key-value pair to the dictionary.
        :param key: The key to add.
        :param value: The value to add.
        """
        if key not in self.keys:
            self._keys.append(key)
            self.values.append(value)
        else:
            self.values[self._keys.index(key)] = value

    def remove(self, key):
        """
        Removes a key-value pair from the dictionary.
        :param key: The key to remove.
        """
        index = self._keys.index(key)
        self._keys.pop(index)
        self.values.pop(index)

    def get(self, key):
        """
        Gets the value associated with a specified key.
        :param key: The key to get the value for.
        :return: The value associated with the specified key, or None if the key is not in the dictionary.
        """
        if key in self._keys:
            return self.values[self._keys.index(key)]
        else:
            return None

    def contains(self, key):
        """
        Checks if a specified key is in the dictionary.
        :param key: The key to check.
        :return: True if the key is in the dictionary, False otherwise.
        """
        return key in self._keys

    def size(self):
        """
        Gets the number of key-value pairs stored in the dictionary.
        :return: An integer representing the number of key-value pairs stored in the dictionary.
        """
        return len(self._keys)
    def items(self):
        """
        Gets the key-value pairs stored in the dictionary as a list of tuples.
        :return: A list of tuples, where each tuple is a key-value pair stored in the dictionary.
        """
        return list(zip(self._keys, self.values))

