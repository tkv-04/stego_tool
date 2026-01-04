import cv2
import numpy as np
from stegano import lsb
from PIL import Image
import io

def encode_video(cover_video_path, secret_message, output_video_path):
    """
    Encodes a secret message into a cover video file and saves the result.

    Args:
        cover_video_path (str): The path to the cover video file.
        secret_message (str): The message to hide.
        output_video_path (str): The path to save the output video file.
    """
    try:
        cap = cv2.VideoCapture(cover_video_path)
        if not cap.isOpened():
            raise IOError("Cannot open video file")

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
        
        secret_message += '#####' # Delimiter
        
        message_chunks = [secret_message[i:i + 256] for i in range(0, len(secret_message), 256)]
        chunk_index = 0

        while cap.isOpened() and chunk_index < len(message_chunks):
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to Pillow image
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            
            # Save to BytesIO
            byte_io = io.BytesIO()
            pil_image.save(byte_io, format='PNG')
            byte_io.seek(0)
            
            try:
                secret_frame = lsb.hide(byte_io, message_chunks[chunk_index])
                
                # Convert back to OpenCV frame
                secret_byte_io = io.BytesIO()
                secret_frame.save(secret_byte_io, format='PNG')
                secret_byte_io.seek(0)
                
                image_data = np.frombuffer(secret_byte_io.read(), np.uint8)
                new_frame_bgr = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
                
                out.write(new_frame_bgr)
                chunk_index += 1

            except Exception as e:
                out.write(frame) # Write original frame if hiding fails
                print(f"Warning: Could not hide data in a frame. Error: {e}")

        # Write remaining frames
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)

        cap.release()
        out.release()
        cv2.destroyAllWindows()
        return True

    except Exception as e:
        print(f"Error encoding video: {e}")
        return False
        
def decode_video(stego_video_path):
    """
    Decodes a secret message from a steganographic video file.

    Args:
        stego_video_path (str): The path to the steganographic video file.

    Returns:
        str: The hidden message, or None if an error occurs.
    """
    try:
        cap = cv2.VideoCapture(stego_video_path)
        if not cap.isOpened():
            raise IOError("Cannot open video file")

        extracted_message = ""
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            
            byte_io = io.BytesIO()
            pil_image.save(byte_io, format='PNG')
            byte_io.seek(0)
            
            try:
                revealed_chunk = lsb.reveal(byte_io)
                if revealed_chunk:
                    extracted_message += revealed_chunk
                
                if extracted_message.endswith("#####"):
                    break # Delimiter found
            except Exception:
                # This frame might not have hidden data
                pass

        cap.release()
        cv2.destroyAllWindows()
        
        if extracted_message.endswith("#####"):
            return extracted_message[:-5]
        else:
            return None # Delimiter not found

    except Exception as e:
        print(f"Error decoding video: {e}")
        return None
