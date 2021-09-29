from tqdm.auto import tqdm
import os
import torchvision.transforms as T
from PIL import Image
from argparse import ArgumentParser


def processing(filepath:str)->list:
    """
    Image processing
    Args:
        filepath(str): Path to img
    Return:
        list[PIL.Image]: List with images.
    """
    
    img = Image.open(filepath)
    img = img.convert("RGB")
    h, w = img.size
    if h > 512 and w > 512:
        img = T.CenterCrop((h//2,w//2))(img)
        imgs = [T.RandomCrop(256)(img) for _ in range(10)]
        imgs = [T.RandomVerticalFlip()(img) for img in imgs]
        return imgs
    
def main():
    parser = ArgumentParser()
    parser.add_argument("--path", default="/home/yaroslav/repos/research-work/DATA/TIBET_BANDS_TCI", help="path to dir with images", type=str)
    parser.add_argument("--ext", default="tif", help="png, jpeg, tif, ...", type=str)
    parser.add_argument("--opath", default = "/home/yaroslav/repos/research-work/DATA/TIBET", help="output path ti dir", type=str)
    args = parser.parse_args()

    os.chdir(os.path.abspath(args.path))
    try:
        os.mkdir(os.path.abspath(args.opath))
    except: pass

    for pathfile in tqdm(os.listdir()):
        imgs = processing(pathfile)
        try:
            for idx,img in enumerate(imgs):
                filename,ext = os.path.splitext(pathfile)
                filename += f"_PROCESSED_{idx}.png"
                opath = f"{args.opath}/{filename}"
                # print(opath)
                img.save(opath)
        except:
            pass
    

if __name__ == "__main__":
    main()