from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from model import apply_dwt_watermark,remove_dwt_watermark
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
import os
app = FastAPI()

# Allow frontend access (for dev use)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.post("/upload/")
# async def upload(image: UploadFile = File(...), watermark: UploadFile = File(...)):
#     try:
#         image_bytes = await image.read()
#         watermark_bytes = await watermark.read()

#         encoded_image, psnr_val, ssim_val = apply_dwt_watermark(image_bytes, watermark_bytes)

#         if encoded_image is None:
#             raise ValueError("Failed to process the image.")

#         return {
#             "image": encoded_image,
#             "psnr": round(psnr_val, 2),
#             "ssim": round(ssim_val, 4)
#         }

#     except Exception as e:
#         return JSONResponse(status_code=400, content={"error": str(e)})
@app.post("/upload/")
async def upload(image: UploadFile = File(...)):
    try:
        image_bytes = await image.read()

        encoded_image, psnr_val, ssim_val = apply_dwt_watermark(image_bytes)

        if encoded_image is None:
            raise ValueError("Failed to process the image.")

        return {
            "image": encoded_image,
            "psnr": round(psnr_val, 2),
            "ssim": round(ssim_val, 4)
        }

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
# @app.post("/extract/")
# async def extract_watermark(image: UploadFile = File(...), watermark: UploadFile = File(...)):
#     image_bytes = await image.read()
#     watermark_bytes = await watermark.read()

#     result_image, psnr_after, ssim_after = remove_dwt_watermark(image_bytes, watermark_bytes)

#     if result_image is None:
#         raise HTTPException(status_code=400, detail="Failed to extract watermark.")

#     return {
#         "image": result_image,
#         "psnr": round(psnr_after, 2),
#         "ssim": round(ssim_after, 4)
#     }
@app.post("/extract/")
async def extract_watermark(image: UploadFile = File(...)):
    try:
        # Read the uploaded (watermarked) image
        image_bytes = await image.read()

        # Load the fixed watermark image from server-side
        watermark_path = "static/Watermark.png"
        if not os.path.exists(watermark_path):
            raise FileNotFoundError(" Watermark image not found on server.")

        with open(watermark_path, "rb") as wm_file:
            watermark_bytes = wm_file.read()

        # Perform watermark removal
        result_image, psnr_after, ssim_after = remove_dwt_watermark(image_bytes, watermark_bytes)

        if result_image is None:
            raise ValueError(" Failed to extract watermark.")

        return {
            "image": result_image,
            "psnr": round(psnr_after, 2),
            "ssim": round(ssim_after, 4)
        }

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
