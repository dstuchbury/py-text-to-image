from PIL import Image, ImageDraw, ImageFont


def get_text_dimensions(text_string, font_used):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font_used.getmetrics()

    text_width = font_used.getmask(text_string).getbbox()[2]
    text_height = font_used.getmask(text_string).getbbox()[3] + descent

    return text_width, text_height


def create_image_from_text(text_input, colour):
    font = personalised_text_font
    img = Image.new('RGBA', get_text_dimensions(text_input, font), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text_input, font=font, fill=colour)

    return img


def create_final_image(logo, name):
    return Image.new('RGBA', (logo.size[0], (logo.size[1] + name.size[1] + 10)), (255, 255, 255, 0))


def text_x_pos_to_centre(logo_input, name_input):
    return int((logo_input.width / 2) - (name_input.size[0] / 2))


def generate_text_beneath_image(logo_input, text_input, colour_input):
    image = Image.open(logo_input)
    use_text = create_image_from_text(text_input, colour_input)

    final_image = create_final_image(image, use_text)
    final_image.paste(image, (0, 0))
    final_image.paste(use_text, (text_x_pos_to_centre(image, use_text), image.height + 10))

    final_image.save('beneath.png')

    return final_image


def generate_text_above_image(logo_input, text_input, colour_input):
    image = Image.open(logo_input)
    use_text = create_image_from_text(text_input, colour_input)

    final_image = create_final_image(image, use_text)
    final_image.paste(image, (0, use_text.height + 10))
    final_image.paste(use_text, (text_x_pos_to_centre(image, use_text), 0))

    final_image.save('above.png')

    return final_image


def composite_image_and_text(logo, personalisation, colour, x_pos = None, y_pos = None):
    image = Image.open(logo).convert("RGBA")
    txt = Image.new('RGBA', image.size, (255, 255, 255, 0))

    final_image = ImageDraw.Draw(txt)

    w, h = final_image.textsize(personalisation)

    x = (image.width - w) / 2
    y = (image.height - h) / 2
    if x_pos:
        x = x_pos
    if y_pos:
        y = y_pos

    final_image.text(
        (x, y),
        personalisation,
        fill=colour,
        font=personalised_text_font,
        anchor="mm"
    )

    combined = Image.alpha_composite(image, txt)

    combined.save("combined.png")
    combined.save("combined.png")

    return combined


# source_logo = 'logo.png'
# source_logo = 'tutorials_point.jpg'
source_logo = 'teacher.png'
# source_logo = '12239402.png'
personalised_text = "Joe Bloggs"
personalised_text_colour = (250, 250, 20, 250)
personalised_text_font = ImageFont.truetype('firasans.ttf', 280)

# generate_text_beneath_image(source_logo, personalised_text, personalised_text_colour)
# generate_text_above_image(source_logo, personalised_text, personalised_text_colour)
composite_image_and_text(source_logo, personalised_text, personalised_text_colour, 1800, 2600)
# composite_image_and_text(source_logo, personalised_text, personalised_text_colour)
