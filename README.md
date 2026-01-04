# Steganography Tool

A powerful and user-friendly steganography tool to hide files and data within images, audio, and video files. The application features a clean, terminal-like user interface and secures your data with AES encryption.

## Features

*   **Multi-format Support:** Hide data in a variety of file formats:
    *   **Images:** PNG, JPG, JPEG
    *   **Audio:** WAV
    *   **Video:** MP4, AVI, MOV
*   **Robust Security:** Your data is encrypted with AES before being embedded, and can only be extracted with the correct password.
*   **Interactive UI:** A sleek, terminal-inspired user interface with a dark theme and neon green accents makes the tool easy and enjoyable to use.
*   **File Format Preservation:** The original filename and format of your secret file are preserved during the decoding process.

## Requirements

The following libraries are required to run the application:

*   `stegano`
*   `Pillow`
*   `opencv-python`
*   `cryptography`
*   `pydub`
*   `ttkthemes`

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/tkv-04/stego_tool.git
    cd stego_tool
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the application, execute the following command in your terminal:

```bash
python src/main.py
```

This will launch the graphical user interface, where you can choose to either encode or decode a file.


---

