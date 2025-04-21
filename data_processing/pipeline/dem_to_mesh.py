"""
DEM to Mesh Conversion Script
"""

import os, json
import pandas as pd
import open3d as o3d
import numpy as np
from pipeline.center_mesh import center_obj

def dem_to_mesh(dem_name: str, filename: str, depth: int):
    """
    Converts a DEM file in XYZ format into a mesh and outputs it as an OBJ file.

    Parameters:
    - dem_name (str): Name of the DEM dataset (e.g., 'Petermann').
    - filename (str): Name of the file to process (e.g., 'surface.xyz').

    Output:
    The mesh is saved to PolXR/Assets/AppData/DEMs/{dem_name}/{filename.replace('.xyz', '.obj')}.
    """
    # Construct file paths
    input_path = f"pipeline/dems/{dem_name}/{filename}"
    output_path = f"../PolXR/Assets/AppData/DEMs/{dem_name}/{filename.replace('.xyz', '.obj')}"
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
       
    # Load XYZ Pointcloud
    pcd = o3d.io.read_point_cloud(input_path,format='xyz')

    # Estimate normals for the point cloud
    pcd.estimate_normals()

    # Create mesh with poisson surface correction
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=depth
    )

    # Removing edge warping
    bbox = pcd.get_axis_aligned_bounding_box()
    cropped_mesh = mesh.crop(bbox)

    # Save mesh as OBJ
    o3d.io.write_triangle_mesh(output_path, cropped_mesh)

    # Calculate centroid
    vertices = np.asarray(mesh.vertices)
    centroid = {
        "x": np.mean(vertices[:, 0]),
        "y": np.mean(vertices[:, 1]),
        "z": np.mean(vertices[:, 2])
    }

    dem_meta = {
        "centroid": centroid
    }
    dem_meta_path = os.path.join(f"../PolXR/Assets/AppData/DEMs/{dem_name}", 'meta.json')
    with open(dem_meta_path, 'w') as f:
        json.dump(dem_meta, f, indent=4)

    # center_obj(output_path)
    print(f"Mesh saved to {output_path}")


def stage_dems(dem_name: str, depth: int = 9):
    """
    Processes and stages both surface and bedrock DEMs for a given DEM name.

    Parameters:
    - dem_name (str): Name of the DEM dataset (e.g., 'Petermann').

    Calls:
    - dem_to_mesh with 'surface.xyz'
    - dem_to_mesh with 'bedrock.xyz'
    """
    dem_to_mesh(dem_name, "bedrock.xyz", depth)
    dem_to_mesh(dem_name, "surface.xyz", depth)