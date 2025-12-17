import io
import base64
import fitz  # PyMuPDF
from PIL import Image
from typing import List, Tuple

def pdf_to_images(pdf_bytes: bytes) -> List[bytes]:
    """
    Convert PDF bytes to list of image bytes (PNG format)

    Args:
        pdf_bytes: PDF file content as bytes

    Returns:
        List of image bytes (one per page)
    """
    images = []

    try:
        # Open PDF from bytes
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")

        # Convert each page to image
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]

            # Render page to image (increase resolution with matrix for better quality)
            zoom = 2  # Zoom factor for better quality
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)

            # Convert to PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Convert to bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            images.append(img_bytes.getvalue())

        pdf_document.close()

    except Exception as e:
        print(f"Error converting PDF to images: {str(e)}")
        return []

    return images

def get_pdf_page_count(pdf_bytes: bytes) -> int:
    """
    Get number of pages in PDF

    Args:
        pdf_bytes: PDF file content as bytes

    Returns:
        Number of pages
    """
    try:
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        page_count = pdf_document.page_count
        pdf_document.close()
        return page_count
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
        return 0

def pdf_to_base64(pdf_bytes: bytes) -> str:
    """
    Convert PDF bytes to base64 string for embedding

    Args:
        pdf_bytes: PDF file content as bytes

    Returns:
        Base64 encoded string
    """
    return base64.b64encode(pdf_bytes).decode('utf-8')

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text content from PDF

    Args:
        pdf_bytes: PDF file content as bytes

    Returns:
        Extracted text
    """
    text = ""

    try:
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")

        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
            text += "\n\n"  # Separate pages

        pdf_document.close()

    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return ""

    return text

def is_pdf(file_bytes: bytes) -> bool:
    """
    Check if bytes represent a PDF file

    Args:
        file_bytes: File content as bytes

    Returns:
        True if PDF, False otherwise
    """
    try:
        # PDF files start with %PDF
        return file_bytes[:4] == b'%PDF'
    except:
        return False

def is_image(file_bytes: bytes) -> bool:
    """
    Check if bytes represent an image file

    Args:
        file_bytes: File content as bytes

    Returns:
        True if image, False otherwise
    """
    try:
        Image.open(io.BytesIO(file_bytes))
        return True
    except:
        return False