from torch import nn
import torch

### GENERATOR ###
class Generator(nn.Module):
    """
    Impimentation of deep convolution GAN
    """

    def __init__(self,noise_dim:int, image_channel:int, hidden_channels:int):
        """
        Args:
            noise_dim(int): 
            output_channel(int): channel for output tensor
            ngpu(int): if you have more one gpu
        """
        
        super(Generator, self).__init__()
        self.main = nn.Sequential(
            self.__make_block(noise_dim, hidden_channels*8,4,1),
            self.__make_block(hidden_channels*8, hidden_channels*4),
            self.__make_block(hidden_channels*4, hidden_channels*2),
            self.__make_block(hidden_channels*2, hidden_channels),
            self.__make_block(hidden_channels, hidden_channels,kernel_size=(3,3),stride=(1,1)),
            self.__make_block(hidden_channels, image_channel,last_layer=True)
        )

    def __make_block(self,in_channels:int, out_channels:int, kernel_size=(4,4), stride=(2,2), padding=(1,1), bias=False, last_layer=False)->nn.Sequential:
        """
        Args:
            in_channels(int): channels in input tensor.
            out_channels(int): channels in output tensor.
            kernal_size(int or tuple): size of window for convolution layer.
            stride(int or tuple): step for convolution layer.
            padding(int or tuple): padding for convolution.
        Return:
            block(nn.Sequential): layer
        """

        if not last_layer:
            block = nn.Sequential(
                nn.ConvTranspose2d(in_channels, out_channels, kernel_size, stride, padding, bias),
                nn.BatchNorm2d(out_channels),
                nn.ReLU(True)
            )
        else: 
            block = nn.Sequential(
                nn.ConvTranspose2d(in_channels, out_channels, kernel_size, stride, padding, bias),
                nn.Tanh()
            )
        return block

    def forward(self, in_tensor):
        """
        Args:
            in_tensor(torch.Tensor): input tensor.
        Return:
            out_tensor(torch.Tensor): output tensor.
        """
        
        out_tensor = self.main(in_tensor)
        return out_tensor

    def show(self):
        """ 
        Print layers model
        """

        print(self.main)

### END GENERATOR ###


