from pathlib import Path


class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.nxt = None
        self.prev = None


class Box:
    def __init__(self, _hash):
        self._hash = _hash

        self.head = Node()
        self.tail = Node()
        self.head.nxt = self.tail
        self.tail.prev = self.head

        self._map = {}

    def insert(self, key, value):
        if key in self._map:
            node = self._map[key]
            node.value = value
            return

        node = Node(key=key, value=value)
        self._map[key] = node
        node.prev = self.tail.prev
        self.tail.prev.nxt = node
        self.tail.prev = node
        node.nxt = self.tail

    def remove(self, key):
        if key not in self._map:
            return

        node = self._map[key]
        node.prev.nxt = node.nxt
        node.nxt.prev = node.prev
        del self._map[key]

    def __iter__(self):
        curr = self.head.nxt
        pos = 1
        while curr is not self.tail:
            yield pos, curr.key, curr.value
            pos += 1
            curr = curr.nxt


def compute_hash(chunk):
    ret = 0
    for ch in chunk:
        ret = ((ret + ord(ch)) * 17) % 256
    return ret


if __name__ == '__main__':
    boxes = [Box(idx) for idx in range(256)]

    with Path('d15_input.txt').open() as f:
        chunks = next(iter(f)).strip().split(',')

    # Part 1
    print(sum(map(compute_hash, chunks)))

    for chunk in chunks:
        if chunk[-1] == '-':
            key = chunk[:-1]
            _hash = compute_hash(key)
            boxes[_hash].remove(key)
        else:
            assert chunk[-2] == '='
            key = chunk[:-2]
            _hash = compute_hash(key)
            value = int(chunk[-1])
            boxes[_hash].insert(key, value)

    ret = 0
    for i, box in enumerate(boxes, 1):
        for pos, _, value in box:
            score = i * pos * value
            ret += score
    # Part 2
    print(ret)


