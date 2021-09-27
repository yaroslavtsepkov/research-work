from torch.utils.data import DataLoader, Dataset
import os
from PIL import Image

class CustomDataset(Dataset):
    """Landsat Dataset images"""
    
    def __init__(self, dataroot, transform=None):
        """
        Args:
            dataroot (string): Path to images
            transform (callable, optional): Optional transform to be
            appied on a sample
        """
        self.dataroot = dataroot
        self.transform = transform
        self.image_name = os.listdir(self.dataroot)
    
    def __len__(self):
        """Get size of dataset"""
        
        return len(self.image_name)
    
    def __getitem__(self, idx):
        """Link for images in dataset and transforming if also need"""
        
        image_path = os.path.join(self.dataroot,self.image_name[idx])
        image = Image.open(image_path)
        if self.transform:
            image = self.transform(image)
        return image