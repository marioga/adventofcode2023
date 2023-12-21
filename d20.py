import math
from collections import deque
from enum import StrEnum
from pathlib import Path


class Signal(StrEnum):
    LOW = 'low'
    HIGH = 'high'


class Node:
    def __init__(self, name):
        self.name = name
        self.targets = []

    def add_target(self, target):
        self.targets.append(target)

    def process_signal(self, signal):
        return [(signal, target) for target in self.targets]


class FlipFlopNode(Node):
    def __init__(self, name):
        super().__init__(name=name)
        self.off = True

    def process_signal(self, signal):
        if signal == Signal.HIGH:
            return []

        new_signal = Signal.HIGH if self.off else Signal.LOW
        self.off = not self.off
        return super().process_signal(new_signal)


class ConjNode(Node):
    def __init__(self, name):
        super().__init__(name=name)
        self.memory = {}

    def update_input_signal(self, _input, signal=Signal.LOW):
        self.memory[_input] = signal

    def process_signal(self, signal):
        new_signal = Signal.LOW if all(v == Signal.HIGH for v in self.memory.values()) else Signal.HIGH
        return super().process_signal(new_signal)


if __name__ == '__main__':
    nodes = {}
    targets = {}
    with Path('d20_input.txt').open() as f:
        for row in f:
            src, tgt = row.strip().split(' -> ')
            _type = Node
            if src.startswith('%'):
                src = src[1:]
                _type = FlipFlopNode
            elif src.startswith('&'):
                src = src[1:]
                _type = ConjNode
            nodes[src] = _type(name=src)
            targets[src] = tgt.split(', ')

    rx_source = None
    for name, target_list in targets.items():
        node = nodes[name]
        for target in target_list:
            if target == 'rx':
                if rx_source is not None:
                    raise Exception("Invalid input")
                rx_source = node

            if target in nodes:
                tgt_node = nodes[target]
            else:
                tgt_node = nodes[target] = Node(name=target)
            node.add_target(tgt_node)
            if isinstance(tgt_node, ConjNode):
                tgt_node.update_input_signal(node)

    rx_source_sources = set()
    for name, target_list in targets.items():
        if rx_source.name in target_list:
            rx_source_sources.add(nodes[name])

    debug = False
    counts = {Signal.LOW: 0, Signal.HIGH: 0}
    button_press = 0
    seen_rx_source_sources = {}
    seen = {}
    while len(seen_rx_source_sources) < len(rx_source_sources) or button_press < 1000:
        button_press += 1
        if debug:
            print(f"Press: {button_press}")

        queue = deque([(None, Signal.LOW, nodes['broadcaster'])])
        while queue:
            parent, signal, node = queue.popleft()

            if node in rx_source_sources and signal == Signal.LOW:
                seen_rx_source_sources[node] = button_press

            if button_press <= 1000:
                counts[signal] += 1

            if debug:
                print(parent.name if parent is not None else 'NONE', signal, node.name)
            for new_signal, target in node.process_signal(signal):
                if isinstance(target, ConjNode):
                    target.update_input_signal(node, new_signal)
                queue.append((node, new_signal, target))

    # Part 1
    print(counts[Signal.LOW] * counts[Signal.HIGH])

    # Part 2. Really unhappy about this one. High signals by rx_source_sources
    # repeat in regular intervals because that's when they receive a low signal.
    # Why??? No idea... requires much more thinking
    print(math.lcm(*seen_rx_source_sources.values()))

