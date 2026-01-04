from stegano import lsb
from PIL import Image

def encode_image(cover_image_path, secret_message, output_image_path):
    """
    Encodes a secret message into a cover image and saves the result.

    Args:
        cover_image_path (str): The path to the cover image.
        secret_message (str): The message to hide.
        output_image_path (str): The path to save the output image.
    """
    try:
        secret_image = lsb.hide(cover_image_path, secret_message)
        secret_image.save(output_image_path)
        return True
    except Exception as e:
        print(f"Error encoding image: {e}")
        return False

def decode_image(stego_image_path):
    """
    Decodes a secret message from a steganographic image.

    Args:
        stego_image_path (str): The path to the steganographic image.

    Returns:
        str: The hidden message, or None if an error occurs.
    """
    try:
        clear_message = lsb.reveal(stego_image_path)
        return clear_message
    except Exception as e:
        print(f"Error decoding image: {e}")
        return None
