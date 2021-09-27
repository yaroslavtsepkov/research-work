import os
import geemap
import ee
from multiprocessing import Pool
from tqdm.auto import tqdm
ee.Initialize()

def filterCollection(bands:tuple):
    """
    Filtering out Image collection 
        Args:
            bands(tuple[str]): bands from satelite image.
        Return:
            None.
    """
    roi = ee.Geometry.Polygon([[[94.96582, 28.470622],
    [92.434571, 26.867201],
    [85.561523, 27.164739],
    [79.233398, 29.51611],
    [75.875976, 31.963347],
    [74.241211, 34.405096],
    [76.262695, 37.366664],
    [79.338867, 37.086734],
    [81.905273, 36.183998],
    [87.231445, 37.715113],
    [95.493164, 39.228849],
    [101.961915, 38.006551],
    [103.825194, 33.691437],
    [94.96582, 28.470622]]])
    start_date = ee.Date.fromYMD(2017,1,1)
    end_date = ee.Date.fromYMD(2020,12,31)
    B1,B2,B3 = bands
    collection = ee.ImageCollection("COPERNICUS/S2_SR")\
        .filterBounds(roi)\
        .filterDate(start_date,end_date)\
        .filter(ee.Filter.rangeContains('CLOUDY_PIXEL_PERCENTAGE',0,10))\
        .select(B1,B2,B3)
    return collection

def exportDatasets(collections, paths:str):
    """ 
    Export filtered collection to tif files.
    Args:
        collection (tuple or list ee.ImageCollection): Image collection for export.
        path(str): path to directory. 
    Return:
        None
    """

    for collection, dir_out in zip(collections,paths):
        geemap.ee_export_image_collection(collection,dir_out)

def main():
    bands = [("TCI_R","TCI_G","TCI_B")]
    paths = ["DATA/TIBET_BANDS_TCI"]
    collections = [filterCollection(band) for band in bands]
    exportDatasets(collections,paths)

if __name__=="__main__":
    main()