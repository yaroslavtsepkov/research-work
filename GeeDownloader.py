import os
import geemap
import ee
from argparse import ArgumentParser
ee.Initialize()

class CustomCollection:
    """ Class satelite images from google earth engine"""

    def __init__(self, dataset="COPERNICUS/S2_SR", bands=("TCI_R","TCI_G","TCI_B")):
        self.dataset: str = dataset
        self.bands: tuple = bands
        self.collection: ee.Collection = self.__createCollection()

    def export(self, drive:bool, folder:str)->None:
        """ 
        Export images to google drive or local
        Args:
            drive(bool): export to google drive
            folder(str): path to output directory
        """

        if not drive:
            geemap.ee_export_image_collection_to_drive(self.collection,folder=folder)
        else:
            geemap.ee_export_image_collection(self.collection,out_dir=folder)

    def __createCollection(self)->ee.Collection:
        """
        Filtering out Image collection 
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
        end_date = ee.Date.fromYMD(2021,9,30)
        B1,B2,B3 = self.bands
        collection = ee.ImageCollection(self.dataset)\
            .filterBounds(roi)\
            .filterDate(start_date,end_date)\
            .filter(ee.Filter.rangeContains('CLOUDY_PIXEL_PERCENTAGE',0,10))\
            .select(B1,B2,B3)
        return collection
        
def main():
    ### ARGS ###
    parser = ArgumentParser()
    parser.add_argument("-p","--path", default=os.getcwd(), help="path to output dir", type=str)
    parser.add_argument("-d","--drive", default=False, help="export to google drive (True\False)", type=str)
    args = parser.parse_args()

    collection = CustomCollection()
    collection.export(args.drive, args.path)

if __name__=="__main__":
    main()