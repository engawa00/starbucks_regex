import timeit

setup = """
class Args:
    def __init__(self, order):
        self.order = order
args = Args("  トール エクストラホイップ ダークモカチップフラペチーノ  ")
"""

stmt_original = """
if not args.order or not args.order.strip():
    pass
order_str = args.order.strip()
"""

stmt_optimized = """
order_str = args.order.strip() if args.order else ""
if not order_str:
    pass
"""

print("Original:", timeit.timeit(stmt_original, setup=setup, number=1000000))
print("Optimized:", timeit.timeit(stmt_optimized, setup=setup, number=1000000))
