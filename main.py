from PIL import Image, ImageDraw, ImageFont


def get_text_dimensions(text_string, font_used):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font_used.getmetrics()

    text_width = font_used.getmask(text_string).getbbox()[2]
    text_height = font_used.getmask(text_string).getbbox()[3] + descent

    return text_width, text_height


def create_personalisation_image(personalisation, font, colour):
    img = Image.new('RGBA', get_text_dimensions(personalisation, font), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), personalisation, font=font, fill=colour)

    return img


def create_final_image(logo, name):
    return Image.new('RGBA', (logo.size[0], (logo.size[1] + name.size[1] + 10)), (255, 255, 255, 0))


def name_x_pos(logo, name):
    return int((logo.width / 2) - (name.size[0] / 2))


def generate_text_beneath_logo(logo, name):
    image = Image.open(logo)

    final_image = create_final_image(image, name)
    final_image.paste(image, (0, 0))
    final_image.paste(name, (name_x_pos(image, name), image.height + 10))

    final_image.show()
    final_image.save('beneath.png')

    return final_image


def generate_text_above_logo(logo, name):
    image = Image.open(logo)

    final_image = create_final_image(image, name)
    final_image.paste(image, (0, name.height + 10))
    final_image.paste(name, (name_x_pos(image, name), 0))

    final_image.show()
    final_image.save('above.png')

    return final_image


name_input = "IT Department"
personalised = name_input+'\'s Artwork'
use_font = ImageFont.truetype('firasans.ttf', 50)
pers_colour = (200, 100, 10)

source_logo = 'logo.png'
# source_logo = 'tutorials_point.jpg'
personalisation_image = create_personalisation_image(personalised, use_font, pers_colour)

generate_text_beneath_logo(logo, personalisation_image)
generate_text_above_logo(logo, personalisation_image)




