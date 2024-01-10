import random
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path


def contract(graph, edge_count):
    while len(graph) > 2:
        idx = random.randrange(edge_count)
        done = False
        while not done:
            for src in graph:
                for tgt in graph[src]:
                    for e in graph[src][tgt]:
                        idx -= 1
                        if idx < 0:
                            done = True
                            break
                    if done:
                        break
                if done:
                    break

        new_node = (*src, *tgt)
        edge_count -= len(graph[src][tgt])
        for edge_tgt, edges in graph.pop(src).items():
            if edge_tgt == tgt:
                continue

            for e in edges:
                graph[new_node][edge_tgt].append(e)
                graph[edge_tgt][new_node].append(e)
            del graph[edge_tgt][src]

        for edge_tgt, edges in graph.pop(tgt).items():
            if edge_tgt == src:
                continue

            for e in edges:
                graph[new_node][edge_tgt].append(e)
                graph[edge_tgt][new_node].append(e)
            del graph[edge_tgt][tgt]

    return graph, edge_count


if __name__ == '__main__':
    with Path('d25_input.txt').open() as f:
        graph = defaultdict(lambda : defaultdict(list))
        edges = []
        for row in f:
            src, tgts = row.strip().split(': ')
            for tgt in tgts.split(' '):
                graph[(src,)][(tgt,)].append(len(edges))
                graph[(tgt,)][(src,)].append(len(edges))
                edges.append(((src,), (tgt,)))

        while True:
            contracted_graph, edge_count = contract(deepcopy(graph), len(edges))
            if edge_count == 3:
                srcs, contracted_edges = next(iter(contracted_graph.items()))
                tgts, contracted_edges = next(iter(contracted_edges.items()))
                print("Removed edges:")
                for idx in contracted_edges:
                    src, tgt = edges[idx]
                    print((*src, *tgt))

                print(f"Product of component sizes: {len(srcs)} * {len(tgts)} = {len(srcs) * len(tgts)}")
                break

