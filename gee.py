import os
import geemap
import ee
import pandas as pd

def main():
    ee.Initialize()
    date_start = pd.date_range(start="2021-05-01", end="2021-07-30", periods=10)
    date_end = pd.date_range(start="2021-05-02",end="2021-08-01", periods=10)
    for start, end in zip(date_start, date_end):
        print(f"start download period {start} | {end}")
        setImageCollection = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")\
            .select(['SR_B4', 'SR_B3', 'SR_B2'])\
            .filterDate(start, end)
        geemap.ee_export_image_collection(setImageCollection, out_dir = "LANDSAT")
        print(f"finish download period {start} | {end}")
    print("DONE")

if __name__=="__main__":
    main()