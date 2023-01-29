class Dictionary:
    def __init__(self):
        self._keys = []
        self.values = []

    @property
    def keys(self):
        return self._keys

    def add(self, key, value):
        if key not in self.keys:
            self._keys.append(key)
            self.values.append(value)
        else:
            self.values[self._keys.index(key)] = value

    def remove(self, key):
        index = self._keys.index(key)
        self._keys.pop(index)
        self.values.pop(index)

    def get(self, key):
        if key in self._keys:
            return self.values[self._keys.index(key)]
        else:
            return None

    def contains(self, key):
        return key in self._keys

    def size(self):
        return len(self._keys)
    def items(self):
        return list(zip(self._keys, self.values))

