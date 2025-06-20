from os import name
from PIL import Image, ImageStat
from pathlib import Path
import numpy as np

def color_distance(color1, color2):
        #calculate the 'distance' between two colors of two images, to quantify the 
        # difference in color. 
        red_diff = color1[0] - color2[0]
        green_diff = color1[1] - color2[1]
        blue_diff = color1[2] - color2[2]
        
        rd_sq = red_diff ** 2
        gd_sq = green_diff ** 2
        bd_sq = blue_diff ** 2
        
        sum_of_squares = rd_sq + gd_sq + bd_sq
        distance = sum_of_squares ** 0.5
        
        return distance

static_path = Path(r"C:\Coding\Mosaic\sourceimgs2")
real_path = Path(r"C:\Coding\Mosaic\sourceimgs1")

# Main image generation function
def generate(tgtpath, rows, cols, srcpath):

    target_img_path = Path(tgtpath)
    source_imgs_path = srcpath

    target_img = Image.open(target_img_path)

    # making a list of paths to each source image.
    src_image_paths = list(source_imgs_path.glob("*.jpg"))    
    for type in ('*.jpg', '*.jpeg', '*.png'):
        src_image_paths.extend(source_imgs_path.glob(type))

    src_imgs = [Image.open(path) for path in src_image_paths]

    print("Calculating average RBG for each source image ...")
    src_avgs = []
    
    for path in src_image_paths:
        img = Image.open(path)
        img = img.convert("RGB")
        low_res = img.resize((320,180))
        img_array = np.array(low_res)

        sum_red = 0
        sum_green = 0
        sum_blue = 0

        pixels = low_res.width*low_res.height

        for x in range(low_res.width):
            for y in range(low_res.height):
                colors = img_array[y, x]
                sum_red += int(colors[0])
                sum_green += int(colors[1])
                sum_blue += int(colors[2])
        
        avg_color = [int(sum_red / pixels),int(sum_green / pixels), int(sum_blue / pixels)]
        avg_color = [int(num) for num in avg_color]

        src_avgs.append(avg_color)

    print(avg_color)
    

    rows = rows
    cols = cols
    cell_w = target_img.width // cols
    cell_h = target_img.height // rows

    cells = []

    product = Image.new('RGB', (cell_w * cols, cell_h * rows))

    print("Assembling final image...")

    for row in range(rows):
        for col in range(cols):
            x_coordinate = cell_w * col
            y_coordinate = cell_h * row
            right = x_coordinate + cell_w
            lower = y_coordinate + cell_h   
            
            box = [x_coordinate, y_coordinate, right, lower]
            cell = target_img.crop(box)

            cells.append(box)

            # each cell has its average color computed
            cell_statistics = ImageStat.Stat(cell)
            cell_avg = tuple(map(int, cell_statistics.mean))

            # the distance to each of the colors of each source image is found
            # this is used to find the appropriate image to replace the cell
            distances = [color_distance(cell_avg, src_avg) for src_avg in src_avgs]
            closest_index = distances.index(min(distances))
            
            cropped_img = src_imgs[closest_index].resize((cell_w,cell_h))
            product.paste(cropped_img, box)

    # product.show()
    product.save("finalproduct.jpg")

if __name__ == "__main__":
    print("Welcome to the image mosaic generator ...")
    num_rows = int(input("How many rows do you want in the product image"))
    num_cols = int(input("How many columns do you want in the product image"))

    while True:
        response = input("What target image do you want to use? (choose from 1, 2, 3, or 4, Q to quit)")
        if response not in ['1','2','3','4']:
            quit()
        else:
            tgt_path_str = r"C:\Coding\Mosaic\target" + str(response) + ".jpg"
            generate(tgt_path_str, num_rows, num_cols, static_path)