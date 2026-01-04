import wave
import struct

def encode_audio(cover_audio_path, secret_message, output_audio_path):
    """
    Encodes a secret message into a cover audio file and saves the result.

    Args:
        cover_audio_path (str): The path to the cover audio file (.wav).
        secret_message (str): The message to hide.
        output_audio_path (str): The path to save the output audio file.
    """
    try:
        wavefile = wave.open(cover_audio_path, mode='rb')
        frame_bytes = bytearray(list(wavefile.readframes(wavefile.getnframes())))
        
        secret_message += '#####' # Delimiter
        secret_message = secret_message.encode('utf-8')
        
        if len(secret_message) * 8 > len(frame_bytes):
            raise ValueError("Secret message is too large for the cover audio file.")

        for i, bit in enumerate(secret_message):
            for j in range(8):
                frame_bytes[i*8+j] = (frame_bytes[i*8+j] & 254) | ((bit >> j) & 1)

        new_wavefile = wave.open(output_audio_path, 'wb')
        new_wavefile.setparams(wavefile.getparams())
        new_wavefile.writeframes(frame_bytes)

        wavefile.close()
        new_wavefile.close()
        return True
    except Exception as e:
        print(f"Error encoding audio: {e}")
        return False

def decode_audio(stego_audio_path):
    """
    Decodes a secret message from a steganographic audio file.

    Args:
        stego_audio_path (str): The path to the steganographic audio file (.wav).

    Returns:
        str: The hidden message, or None if an error occurs.
    """
    try:
        wavefile = wave.open(stego_audio_path, mode='rb')
        frame_bytes = bytearray(list(wavefile.readframes(wavefile.getnframes())))
        
        extracted = ""
        for i in range(len(frame_bytes) // 8):
            byte = 0
            for j in range(8):
                byte |= (frame_bytes[i*8+j] & 1) << j
            extracted += chr(byte)
            if extracted.endswith("#####"):
                wavefile.close()
                return extracted[:-5] # Remove delimiter
                
        wavefile.close()
        return None
    except Exception as e:
        print(f"Error decoding audio: {e}")
        return None
