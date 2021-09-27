from tqdm.auto import tqdm
import os
from glob import glob
import torchvision.transforms as T
from PIL import Image
from argparse import ArgumentParser


def processing(filepath:str):
    img = Image.open(filepath)
    h, w = img.size
    if h > 512 and w > 512:
        img = T.CenterCrop(h, h)(img)
        imgs = [T.RandomCrop(256)(img) for _ in range(10)]
    return imgs
    
def main():
    parser = ArgumentParser()
    parser.add_argument("--path", help="dir with images", type=str)
    parser.add_argument("--ext", help="png, jpeg, tif, ...", type=str)
    args = parser.parse_args()
    for pathfile in tqdm(glob(f"{args.path}/{'*.'}{args.ext}")):
        imgs = processing(pathfile)
        for idx,img in enumerate(imgs):
            filename,ext = os.path.splitext(pathfile)
            filename += str(idx)+ext
            img.save(filename)
    

if __name__ == "__main__":
    main()