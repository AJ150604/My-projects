import numpy as np
import cv2
import pywt
from PIL import Image
import io
import base64
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
import os
def resize_image(image, size):
    """Resize image to given (height, width)"""
    return cv2.resize(image, (size[1], size[0]), interpolation=cv2.INTER_AREA)
# def apply_dwt_watermark(image_bytes, watermark_bytes):
#     """Apply DWT-based watermarking and compute PSNR & SSIM"""
#     try:
#         # Load both images as grayscale
#         image = Image.open(io.BytesIO(image_bytes)).convert('L')
#         watermark = Image.open(io.BytesIO(watermark_bytes)).convert('L')

#         # Normalize both to a base size (optional: pick common size like 256x256)
#         base_size = (256, 256)
#         image = image.resize(base_size)
#         watermark = watermark.resize(base_size)

#         image = np.array(image)
#         watermark = np.array(watermark)

#         if image.shape != watermark.shape:
#             raise ValueError(f" Input images must have the same dimensions. Got {image.shape} and {watermark.shape}")

#         # Apply DWT to original image
#         cA, (cH, cV, cD) = pywt.dwt2(image, 'haar')

#         # Resize watermark to match size of cA (low-frequency component)
#         watermark_resized = resize_image(watermark, cA.shape)

#         # Embed watermark
#         alpha = 0.1
#         cA_watermarked = cA + alpha * watermark_resized

#         # Inverse DWT
#         watermarked_image = pywt.idwt2((cA_watermarked, (cH, cV, cD)), 'haar')
#         watermarked_image = np.clip(watermarked_image, 0, 255).astype(np.uint8)

#         # Compute metrics
#         psnr_before = psnr(image, watermarked_image, data_range=255)
#         ssim_before = ssim(image, watermarked_image, data_range=255)

#         # Convert result to base64 for web
#         img_pil = Image.fromarray(watermarked_image)
#         img_bytes = io.BytesIO()
#         img_pil.save(img_bytes, format="PNG")
#         encoded_image = base64.b64encode(img_bytes.getvalue()).decode("utf-8")

#         return encoded_image, psnr_before, ssim_before

#     except Exception as e:
#         print(f" Error in apply_dwt_watermark: {str(e)}")
#         return None, None, None
def apply_dwt_watermark(image_bytes):
    try:
        base_size = (256, 256)

        
        image = Image.open(io.BytesIO(image_bytes)).convert('L').resize(base_size)

        
        with open("static/Watermark.png", "rb") as f:
            watermark = Image.open(f).convert("L").resize(base_size)

        image = np.array(image)
        watermark = np.array(watermark)

        
        cA, (cH, cV, cD) = pywt.dwt2(image, 'haar')
        watermark_resized = resize_image(watermark, cA.shape)

        alpha = 0.1
        cA_watermarked = cA + alpha * watermark_resized

        watermarked_image = pywt.idwt2((cA_watermarked, (cH, cV, cD)), 'haar')
        watermarked_image = np.clip(watermarked_image, 0, 255).astype(np.uint8)

        psnr_before = psnr(image, watermarked_image, data_range=255)
        ssim_before = ssim(image, watermarked_image, data_range=255)

        img_pil = Image.fromarray(watermarked_image)
        img_bytes = io.BytesIO()
        img_pil.save(img_bytes, format="PNG")
        encoded_image = base64.b64encode(img_bytes.getvalue()).decode("utf-8")

        return encoded_image, psnr_before, ssim_before

    except Exception as e:
        print(f" Error in apply_dwt_watermark: {str(e)}")
        return None, None, None


# def remove_dwt_watermark(watermarked_bytes, watermark_bytes):
#     """Remove watermark using inverse DWT"""
#     try:
#         base_size = (256, 256)  # Must match the size used in apply_dwt_watermark

#         # Load and resize images
#         watermarked = Image.open(io.BytesIO(watermarked_bytes)).convert("L").resize(base_size)
#         watermark = Image.open(io.BytesIO(watermark_bytes)).convert("L").resize(base_size)

#         watermarked = np.array(watermarked)
#         watermark = np.array(watermark)

#         if watermarked.shape != watermark.shape:
#             raise ValueError(f" Input images must have the same dimensions. Got {watermarked.shape} and {watermark.shape}")

#         # DWT on watermarked image
#         cA_wm, (cH, cV, cD) = pywt.dwt2(watermarked, 'haar')

#         # Resize watermark to match cA shape
#         watermark_resized = resize_image(watermark, cA_wm.shape)

#         # Inverse embedding
#         alpha = 0.1
#         cA_original = cA_wm - alpha * watermark_resized

#         # Reconstruct image
#         restored = pywt.idwt2((cA_original, (cH, cV, cD)), 'haar')
#         restored = np.clip(restored, 0, 255).astype(np.uint8)

#         # Metrics
#         psnr_after = psnr(watermarked, restored, data_range=255)
#         ssim_after = ssim(watermarked, restored, data_range=255)

#         # Encode to base64
#         img_pil = Image.fromarray(restored)
#         img_bytes = io.BytesIO()
#         img_pil.save(img_bytes, format="PNG")
#         encoded_image = base64.b64encode(img_bytes.getvalue()).decode("utf-8")

#         return encoded_image, psnr_after, ssim_after

#     except Exception as e:
#         print(f" Error in remove_dwt_watermark: {str(e)}")
#         return None, None, None
def remove_dwt_watermark(watermarked_bytes, watermark_bytes):
    try:
        base_size = (256, 256)

        
        watermarked = Image.open(io.BytesIO(watermarked_bytes)).convert("L").resize(base_size)
        watermark = Image.open(io.BytesIO(watermark_bytes)).convert("L").resize(base_size)

        watermarked = np.array(watermarked)
        watermark = np.array(watermark)

        
        if watermarked.shape != watermark.shape:
            raise ValueError(" Shape mismatch between watermarked and watermark image.")

        
        cA_wm, (cH, cV, cD) = pywt.dwt2(watermarked, 'haar')
        watermark_resized = resize_image(watermark, cA_wm.shape)

        alpha = 0.1
        cA_original = cA_wm - alpha * watermark_resized

        
        restored = pywt.idwt2((cA_original, (cH, cV, cD)), 'haar')
        restored = np.clip(restored, 0, 255).astype(np.uint8)

        psnr_after = psnr(watermarked, restored, data_range=255)
        ssim_after = ssim(watermarked, restored, data_range=255)

        img_pil = Image.fromarray(restored)
        img_bytes = io.BytesIO()
        img_pil.save(img_bytes, format="PNG")
        encoded_image = base64.b64encode(img_bytes.getvalue()).decode("utf-8")

        return encoded_image, psnr_after, ssim_after

    except Exception as e:
        print(f" Error in remove_dwt_watermark: {str(e)}")
        return None, None, None
