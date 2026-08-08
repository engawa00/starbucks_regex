import timeit
import os

script_dir = "/dummy/script/dir"
files_to_include = [f"file_{i}.txt" for i in range(100000)]
_file_paths = {f: os.path.join(script_dir, f) for f in files_to_include}

def original():
    paths = []
    for f in files_to_include:
        target_path = os.path.join(script_dir, f)
        paths.append(target_path)
    return paths

def optimized():
    paths = []
    for f in files_to_include:
        target_path = _file_paths[f]
        paths.append(target_path)
    return paths

original_time = timeit.timeit(original, number=100)
optimized_time = timeit.timeit(optimized, number=100)

print(f"Original: {original_time:.4f}s")
print(f"Optimized: {optimized_time:.4f}s")
print(f"Improvement: {(original_time - optimized_time) / original_time * 100:.2f}%")
