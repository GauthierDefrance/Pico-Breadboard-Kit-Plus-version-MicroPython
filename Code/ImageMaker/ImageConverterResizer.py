from PIL import Image
import struct

#The file where the image.png is from and where the .rgb565 will go, you normaly don't need to change that
IMGFrom = "ImagePNG\\"
IMGTo = "Imagerbg565\\"

#here you have to write the name of your image, the program take a png in input
#and output a .rgb565 file.
PNGname ="YourImageName.png"
rgb565name = "YourImageName.rgb565"

#Set the final width and heigth of your image.
#VERY IMPORTANT, when you load an image in your code,
#you have to specify the size of width and heigth of your image
#.rgb565 file has no meta data
widht = 60
height = 460


def convert_and_resize_image(png_file, output_file, width, height):
    img = Image.open(png_file)
    img = img.resize((width, height))  # resize the image
    img = img.convert('RGB')  # turn the image into RGB code
    pixels = img.load()

    with open(output_file, 'wb') as f:
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = pixels[x, y]

                # Invert the color, usefull because the rgb565 image are by default inverted.
                r = 255 - r
                g = 255 - g
                b = 255 - b

                # Convert in RGB565
                rgb565 = ((r & 0xf8) << 8) | ((g & 0xfc) << 3) | (b >> 3)
                f.write(rgb565.to_bytes(2, 'big'))  # register the pixel at format RGB565


# Use the function
convert_and_resize_image(IMGFrom+PNGname, IMGTo+rgb565name, widht, height)

