import geopandas as gpd
import os
import matplotlib.pyplot as plt
from tqdm import tqdm
import json

world = gpd.read_file("static/ne_10m_admin_0_countries.shp")  # use 10m or 50m for more detail

# Ensure output directories exist
os.makedirs("static/images", exist_ok=True)

for _, row in tqdm(world.iterrows(), total=len(world), desc="Generating country outlines"):
    # Original detail
    fig, ax = plt.subplots()
    gpd.GeoSeries([row.geometry]).plot(ax=ax)
    ax.axis('off')
    plt.savefig(f"static/images/{row['NAME']}_3.svg", format='svg', bbox_inches='tight')
    plt.close()

    # Less detail (simplify geometry)
    simplified_geom = row.geometry.simplify(0.2, preserve_topology=True)
    fig, ax = plt.subplots()
    gpd.GeoSeries([simplified_geom]).plot(ax=ax)
    ax.axis('off')
    plt.savefig(f"static/images/{row['NAME']}_2.svg", format='svg', bbox_inches='tight')
    plt.close()

    # Least detail (more simplification)
    least_geom = row.geometry.simplify(1.0, preserve_topology=True)
    fig, ax = plt.subplots()
    gpd.GeoSeries([least_geom]).plot(ax=ax)
    ax.axis('off')
    plt.savefig(f"static/images/{row['NAME']}_1.svg", format='svg', bbox_inches='tight')
    plt.close()

    country_entry = {
        "name": row["NAME"],
        "images": [
            f"static/images/{row['NAME']}_1.svg",
            f"static/images/{row['NAME']}_2.svg",
            f"static/images/{row['NAME']}_3.svg"
        ]
    }

    json_path = "static/countries.json"
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            countries = json.load(f)
    else:
        countries = []

    countries.append(country_entry)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(countries, f, ensure_ascii=False, indent=2)