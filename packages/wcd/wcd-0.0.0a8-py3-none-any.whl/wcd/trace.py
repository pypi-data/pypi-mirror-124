import tracemalloc
import linecache
import os


# https://docs.python.org/3/library/tracemalloc.html#pretty-top
def display_top(snapshot, key_type='lineno', limit=10):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print(f"Top {limit} memory-consuming lines:\n")
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        print(f"#{index}: {frame.filename}:{frame.lineno}: {stat.size / 1024:.1f} KiB")
        if (line := linecache.getline(frame.filename, frame.lineno).strip()):
            print(f"    {line}")
        print()

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print(f"{len(other)} other: {size / 2014:.1f} KiB")
    total = sum(stat.size for stat in top_stats)
    print(f"Total allocated size: {total / 1024:.1f} KiB")


_snapshots = []
tracemalloc.start()


def take_snapshot():
    _snapshots.append(tracemalloc.take_snapshot())


# https://docs.python.org/3/library/tracemalloc.html#display-the-top-10
def print_snapshots():
    for snapshot in _snapshots:
        display_top(snapshot)
        # for stat in snapshot.statistics("lineno")[:10]:
        #     print(stat)
        print("\n\n")

