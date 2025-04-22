import numpy as np

def pad_edges(points, edges, depth_increment):
    # Pad edges with zeros more efficiently
    for edge in edges:
        depths = np.arange(0, edge["z"] + depth_increment, depth_increment)  # Generate depths from 0 to edge["z"]
        points.extend({"x": edge["x"], "y": edge["y"], "z": depth} for depth in depths)
    return points
