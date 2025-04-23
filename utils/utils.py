from time import time

def execution_time(start_time):
    end_time = time()
    execution_time = end_time - start_time
    print(
        f"Execution Time: {execution_time:.3f} seconds\n-----------------------------"
    )

def print_time(msg, start_time):
    end_time = time()
    execution_time = end_time - start_time
    print(f"{msg} ({execution_time:.3f}s)")

def get_slice_dir(dir):
    if dir.lower() == "x":
        return "Y"
    else:
        return "X"
    