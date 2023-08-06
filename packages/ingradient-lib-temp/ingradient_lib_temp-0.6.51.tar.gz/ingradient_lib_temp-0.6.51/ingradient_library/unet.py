import torch.nn as nn
import torch
import torch.nn.functional as F

def conv_block(in_channels, out_channels, kernel_size, stride, padding):
    return nn.Sequential(nn.Conv3d(in_channels, out_channels, kernel_size, stride, padding),
                         nn.Dropout3d(),
                         nn.BatchNorm3d(out_channels),
                         nn.LeakyReLU())

def trans_conv_block(in_channels, out_channels, kernel_size, stride, padding, output_padding):
    return nn.Sequential(nn.ConvTranspose3d(in_channels, out_channels, kernel_size, stride, padding, output_padding),
                         nn.Dropout3d(),
                         nn.BatchNorm3d(out_channels),
                         nn.LeakyReLU())
    
def encoder_block(in_channels, out_channels, kernel_size = 3, stride = 2):
    return nn.Sequential(conv_block(in_channels, out_channels, kernel_size, stride, padding = 1),
                         conv_block(out_channels, out_channels, kernel_size, stride = 1, padding = 1))


class UNet_Plus3d(nn.Module):
    def __init__(self, in_channels = 1, out_channels = 2, n_channels = 32, channel_bound = 320):
        super().__init__()
        self.expand_channels = encoder_block(in_channels, n_channels, stride = 1)
        self.conv_downsample1 = encoder_block(n_channels, n_channels * 2)
        self.conv_downsample2 = encoder_block(n_channels * 2, n_channels * 4)
        self.conv_downsample3 = encoder_block(n_channels * 4, n_channels * 8)
        self.conv_downsample4 = encoder_block(n_channels * 8, channel_bound)

        self.conv_upsample1 = nn.ConvTranspose3d(channel_bound, n_channels * 8, kernel_size = 3, stride = 2, padding = 1, output_padding = 1)
        self.conv_upsample2= nn.ConvTranspose3d(n_channels * 8, n_channels * 4, kernel_size = 3, stride = 2, padding = 1, output_padding = 1)
        self.conv_upsample3= nn.ConvTranspose3d(n_channels * 4, n_channels * 2, kernel_size = 3, stride = 2, padding = 1, output_padding = 1)
        self.conv_upsample4= nn.ConvTranspose3d(n_channels * 2, n_channels, kernel_size = 3, stride = 2, padding = 1, output_padding = 1)

        self.decoder1 = encoder_block(n_channels * 1 * 2, n_channels)
        self.decoder2 = encoder_block(n_channels * 2 * 2, n_channels * 2)
        self.decoder3 = encoder_block(n_channels * 4 * 2, n_channels * 4)
        self.decoder4 = encoder_block(n_channels * 8 * 2, n_channels * 8, stride = 1)
        
        self.classifier = nn.Conv3d(n_channels, out_channels, kernel_size = 1)
    
    def forward(self, x):
        x = self.expand_channels(x)
        x_downsample1 = self.conv_downsample1(x)
        x_downsample2 = self.conv_downsample2(x_downsample1)
        x_downsample3 = self.conv_downsample3(x_downsample2)
        x_downsample4 = self.conv_downsample4(x_downsample3)

        x_downsample4_up = self.conv_upsample1(x_downsample4)
        l4_output = self.decoder4(torch.cat((x_downsample4_up, x_downsample3), dim = 1))
        x_downsmaple3_up = self.conv_upsample2(l4_output)
        l3_output = self.decoder3(torch.cat((x_downsmaple3_up, x_downsample2), dim = 1))
        x_downsmaple2_up = self.conv_upsample3(l3_output)
        l2_output = self.decoder2(torch.cat((x_downsmaple2_up, x_downsample1), dim = 1))
        x_downsmaple1_up = self.conv_upsample4(l2_output)
        l1_output = self.decoder1(torch.cat((x_downsmaple1_up, x),dim = 1))

        print(l1_output.shape, l2_output.shape, l3_output.shape, l4_output.shape)

        
        return self.classifier(l1_output)
                