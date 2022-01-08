import io
import PIL
from PIL import ImageFilter, Image

def generate_final_cover(cover, coverFilename):

    cover = Image.open(io.BytesIO(cover))

    newSize = (int(round(cover.size[0]/cover.size[1]*1080)), 1080)
    coverResized = cover.resize(newSize)
    blurredCover = coverResized.filter(ImageFilter.GaussianBlur(6))

    remainder = 1920 - newSize[0]
    cutpoints = (remainder//2, (1920 - remainder//2, blurredCover.size[0] - remainder%2 - remainder//2))
    strp1 = blurredCover.crop((0, 0, cutpoints[0], 1080))
    strp2 = blurredCover.crop((cutpoints[1][1], 0, blurredCover.size[0], 1080))

    finalCover = Image.new(cover.mode, (1920, 1080))
    finalCover.paste(strp1, (0,0))
    finalCover.paste(coverResized, (cutpoints[0],0))
    finalCover.paste(strp2, (cutpoints[1][0],0))
    finalCover.save(coverFilename)