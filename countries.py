import geopandas as gpd
import os
import matplotlib.pyplot as plt
from tqdm import tqdm
import json

world = gpd.read_file("app/ne_10m_admin_0_countries.shp")  # use 10m or 50m for more detail

# Ensure output directories exist
os.makedirs("app/static/svgs", exist_ok=True)

for _, row in tqdm(world.iterrows(), total=len(world), desc="Generating country outlines"):
    # Original detail
    fig, ax = plt.subplots()
    gpd.GeoSeries([row.geometry]).plot(ax=ax)
    ax.axis('off')
    plt.savefig(f"app/static/svgs/{row['NAME']}_3.svg", format='svg', bbox_inches='tight')
    plt.close()

    # Less detail (simplify geometry)
    simplified_geom = row.geometry.simplify(0.2, preserve_topology=True)
    fig, ax = plt.subplots()
    gpd.GeoSeries([simplified_geom]).plot(ax=ax)
    ax.axis('off')
    plt.savefig(f"app/static/svgs/{row['NAME']}_2.svg", format='svg', bbox_inches='tight')
    plt.close()

    # Least detail (more simplification)
    least_geom = row.geometry.simplify(1.0, preserve_topology=True)
    fig, ax = plt.subplots()
    gpd.GeoSeries([least_geom]).plot(ax=ax)
    ax.axis('off')
    plt.savefig(f"app/static/svgs/{row['NAME']}_1.svg", format='svg', bbox_inches='tight')
    plt.close()