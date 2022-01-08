import io
import PIL
from PIL import ImageFilter, Image

def generate_final_cover(cover, coverFilename):

    cover = Image.open(io.BytesIO(cover))

    new_size = (int(round(cover.size[0]/cover.size[1]*1080)), 1080)
    cover_resized = cover.resize(new_size)
    blurred_cover = cover_resized.filter(ImageFilter.GaussianBlur(6))

    remainder = 1920 - new_size[0]
    cutpoints = (remainder//2, (1920 - remainder//2, blurred_cover.size[0] - remainder%2 - remainder//2))
    strp1 = blurred_cover.crop((0, 0, cutpoints[0], 1080))
    strp2 = blurred_cover.crop((cutpoints[1][1], 0, blurred_cover.size[0], 1080))

    final_cover = Image.new(cover.mode, (1920, 1080))
    final_cover.paste(strp1, (0,0))
    final_cover.paste(cover_resized, (cutpoints[0],0))
    final_cover.paste(strp2, (cutpoints[1][0],0))
    final_cover.save(coverFilename)