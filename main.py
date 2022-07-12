"""
An interesting dive in to Pillow and the image processing possibilities.
"""
from PIL import Image, ImageDraw, ImageFont


class ToPersonalise:
    """
    Defines the element of personalisation. In this case some text, the font and the colour
    """

    def __init__(self, text: str, font: ImageFont, colour: tuple):
        self.text = text
        self.font = font
        self.colour = colour


def get_text_dimensions(text_string, font_used):
    """
    Gets the dimensions of the resulting image created from given text in a given font
    :param text_string:
    :param font_used:
    :return:
    """
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font_used.getmetrics()

    text_width = font_used.getmask(text_string).getbbox()[2]
    text_height = font_used.getmask(text_string).getbbox()[3] + descent

    return text_width, text_height


def create_image_from_text(personalisation: ToPersonalise):
    """
    takes input ToPersonalise, creating an image with appropriate dimensions to fit
    :param personalisation:
    :return: the created image.
    """
    img = Image.new(
        "RGBA",
        get_text_dimensions(personalisation.text, personalisation.font),
        (255, 255, 255, 0),
    )
    draw = ImageDraw.Draw(img)
    draw.text(
        (0, 0),
        personalisation.text,
        font=personalisation.font,
        fill=personalisation.colour,
    )

    return img


def create_final_image(image: Image, text: Image):
    """
    Creates an image onto which the original artwork and the text image are placed onto
    :param image:
    :param text:
    :return: Blank image of the required size with a transparent background.
    """
    return Image.new(
        "RGBA", (image.size[0], (image.size[1] + text.size[1] + 10)), (255, 255, 255, 0)
    )


def text_x_pos_to_centre(image, text):
    """
    Finds the x co-ordinate required to place text in the middle of a supplied artwork
    :param image:
    :param text:
    :return:
    """
    return int((image.width / 2) - (text.size[0] / 2))


def generate_text_beneath_image(image, personalisation):
    """
    Generates a new image containing the source text placed centered and below the source image
    :param image:
    :param personalisation:
    :return:
    """
    use_image = Image.open(image)
    text_as_image = create_image_from_text(personalisation)

    final_image = create_final_image(use_image, text_as_image)
    final_image.paste(use_image, (0, 0))
    final_image.paste(
        text_as_image,
        (text_x_pos_to_centre(use_image, text_as_image), use_image.height + 10),
    )

    final_image.save("beneath.png")

    return {"action": "complete"}


def generate_text_above_image(image, personalisation):
    """
    Generates a new image containing the source text placed centered and above the source image
    :param image:
    :param personalisation:
    :return:
    """
    use_image = Image.open(image)
    text_as_image = create_image_from_text(personalisation)

    final_image = create_final_image(use_image, text_as_image)
    final_image.paste(use_image, (0, text_as_image.height + 10))
    final_image.paste(
        text_as_image, (text_x_pos_to_centre(use_image, text_as_image), 0)
    )

    final_image.save("above.png")

    return {"action": "complete"}


def composite_image_and_text(
    source_image: str,
    personalisation: ToPersonalise,
    coords: tuple = None,
):
    """
    Composites supplied text onto the source image at co-ordinates specified.
    :param source_image:
    :param personalisation:
    :param coords:
    :return:
    """
    image = Image.open(source_image).convert("RGBA")
    # we use alpha_composite, so both images have to be the same size.
    txt = Image.new("RGBA", image.size, (255, 255, 255, 0))

    final_image = ImageDraw.Draw(txt)

    width, height = final_image.textsize(personalisation.text, personalisation.font)

    x_pos = (image.width - width) / 2
    y_pos = (image.height - height) / 2
    if coords[0]:
        x_pos = coords[0]
    if coords[1]:
        y_pos = coords[1]

    final_image.text(
        (x_pos, y_pos),
        personalisation.text,
        fill=personalisation.colour,
        font=personalisation.font,
        anchor="mm",
    )

    combined = Image.alpha_composite(image, txt)

    combined.save("combined.png")

    return {"action": "complete"}


# SOURCE_LOGO = 'logo.png'
# SOURCE_LOGO = 'tutorials_point.jpg'
SOURCE_LOGO = "teacher.png"
# SOURCE_LOGO = '12239402.png'

personalise = ToPersonalise(
    "Joe Bloggs", ImageFont.truetype("archivo.ttf", 280), (250, 20, 20, 250)
)

generate_text_beneath_image(SOURCE_LOGO, personalise)
generate_text_above_image(SOURCE_LOGO, personalise)
composite_image_and_text(SOURCE_LOGO, personalise, (1800, 2600))
