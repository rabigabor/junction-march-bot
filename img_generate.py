from PIL import Image, ImageFont, ImageDraw, ImageStat, ImageFilter
from io import BytesIO
import textwrap


def get_rect_coordinates(lines, padding, font, font_size, W, H):
	max_width = 0
	for line in lines:
	    width, _ = font.getsize(line)
	    max_width = max(max_width, width)

	rect_x0 = (W - max_width) / 2 - padding
	rect_y0 = (H - font_size * len(lines)) / 2 - padding
	rect_x1 = (W - max_width) / 2 + max_width + padding
	rect_y1 = (H - font_size * len(lines)) / 2 + font_size * len(lines) + padding

	return rect_x0, rect_y0, rect_x1, rect_y1


def draw_text_on_image(image, text, padding = 15, font_size = 22):
	print("Generating motivational image...")
	img = Image.open(image)
	W, H = img.size

	img = img.filter(ImageFilter.GaussianBlur(radius=2))

	draw = ImageDraw.Draw(img, 'RGBA')

	font = ImageFont.truetype("calibril.ttf", font_size)


	lines = textwrap.wrap(text, width=40)

	rect_x0, rect_y0, rect_x1, rect_y1 = get_rect_coordinates(lines, padding, font, font_size, W, H)

	median_color = tuple(ImageStat.Stat(img.crop((rect_x0, rect_y0, rect_x1, rect_y1))).median)

	draw.rectangle(((rect_x0, rect_y0), (rect_x1, rect_y1)), fill=median_color+(127,))

	text_height = (H - font_size * len(lines)) / 2
	for line in lines:
	    width, height = font.getsize(line)
	    draw.text(((W - width) / 2, text_height), line, font=font, fill="white")
	    text_height += font_size

	byte_io = BytesIO()

	img.save(byte_io, 'PNG')
	retval = byte_io.getvalue()

	print("Motivational image has been generated successfully!")
	byte_io.close()
	return retval