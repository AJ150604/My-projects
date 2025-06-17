// document.addEventListener("DOMContentLoaded", function () {
//     const form = document.getElementById("upload-form");
//     if (form) {
//         form.addEventListener("submit", function (event) {
//             event.preventDefault();
//         });
//     }

//     const previewImage = (inputId, previewId) => {
//         const input = document.getElementById(inputId);
//         const preview = document.getElementById(previewId);

//         if (!input || !preview) return;

//         input.addEventListener('change', function (event) {
//             const file = event.target.files[0];
//             if (!file) {
//                 preview.style.display = 'none';
//                 return;
//             }

//             const reader = new FileReader();
//             reader.onload = function () {
//                 preview.src = reader.result;
//                 preview.style.display = 'block';
//             };
//             reader.readAsDataURL(file);
//         });
//     };

//     previewImage('image-upload', 'original-preview');
//     previewImage('watermark-upload', 'watermark-preview');

//     const applyBtn = document.getElementById('apply-watermark');
//     if (applyBtn) {
//         applyBtn.addEventListener('click', async function () {
//             const imageInput = document.getElementById('image-upload');
//             const watermarkInput = document.getElementById('watermark-upload');
//             const imageFile = imageInput?.files[0];
//             const watermarkFile = watermarkInput?.files[0];

//             if (!imageFile || !watermarkFile) {
//                 alert("Please upload both images before applying the watermark.");
//                 return;
//             }

//             const formData = new FormData();
//             formData.append('image', imageFile);
//             formData.append('watermark', watermarkFile);

//             try {
//                 const response = await fetch('http://127.0.0.1:8000/upload/', {
//                     method: 'POST',
//                     body: formData
//                 });

//                 if (!response.ok) {
//                     throw new Error(`Server responded with status ${response.status}`);
//                 }

//                 const result = await response.json();
//                 if (result.error) throw new Error(result.error);

//                 const watermarkedImg = document.getElementById('watermarked-preview');
//                 if (watermarkedImg) {
//                     watermarkedImg.src = 'data:image/png;base64,' + result.image;
//                     watermarkedImg.style.display = 'block';
//                 }

//                 const psnrElem = document.getElementById('psnr-value');
//                 const ssimElem = document.getElementById('ssim-value');
//                 if (psnrElem) psnrElem.textContent = `PSNR: ${result.psnr} dB`;
//                 if (ssimElem) ssimElem.textContent = `SSIM: ${result.ssim}`;

//                 const link = document.getElementById('download-link');
//                 if (link && watermarkedImg?.src) {
//                     link.href = watermarkedImg.src;
//                     link.style.display = 'inline-block';
//                 }

//             } catch (error) {
//                 console.error("Error processing watermark:", error);
//                 alert("Failed to apply watermark: " + error.message);
//             }
//         });
//     }
// });
// document.getElementById('extract-watermark').addEventListener('click', async function () {
//     const watermarkedFile = document.getElementById('image-upload').files[0];
//     const watermarkFile = document.getElementById('watermark-upload').files[0];

//     if (!watermarkedFile || !watermarkFile) {
//         alert("Please upload both the watermarked image and watermark image.");
//         return;
//     }

//     const formData = new FormData();
//     formData.append('image', watermarkedFile);  // Assumes image-upload now holds the watermarked one
//     formData.append('watermark', watermarkFile);

//     try {
//         const response = await fetch('http://127.0.0.1:8000/extract/', {
//             method: 'POST',
//             body: formData
//         });

//         if (!response.ok) throw new Error(`Server error: ${response.status}`);

//         const result = await response.json();

//         const extractedImg = document.getElementById('extracted-preview');
//         extractedImg.src = 'data:image/png;base64,' + result.image;
//         extractedImg.style.display = 'block';

//         document.getElementById('psnr-after').textContent = `PSNR After: ${result.psnr} dB`;
//         document.getElementById('ssim-after').textContent = `SSIM After: ${result.ssim}`;

//         const link = document.getElementById('download-extracted-link');
//         link.href = extractedImg.src;
//         link.style.display = 'inline-block';

//     } catch (error) {
//         console.error("Error extracting watermark:", error);
//         alert("Failed to extract watermark: " + error.message);
//     }
// });
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("upload-form");
    if (form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault();
        });
    }

    // Show preview of uploaded image
    const previewImage = (inputId, previewId) => {
        const input = document.getElementById(inputId);
        const preview = document.getElementById(previewId);

        if (!input || !preview) return;

        input.addEventListener('change', function (event) {
            const file = event.target.files[0];
            if (!file) {
                preview.style.display = 'none';
                return;
            }

            const reader = new FileReader();
            reader.onload = function () {
                preview.src = reader.result;
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        });
    };

    previewImage('image-upload', 'original-preview');

    // Display fixed watermark from server
    const fixedWatermark = document.getElementById('watermark-preview');
    if (fixedWatermark) {
        fixedWatermark.src = 'static/Watermark.png';
        fixedWatermark.style.display = 'block';
    }

    // Apply watermark button
    const applyBtn = document.getElementById('apply-watermark');
    if (applyBtn) {
        applyBtn.addEventListener('click', async function () {
            const imageInput = document.getElementById('image-upload');
            const imageFile = imageInput?.files[0];

            if (!imageFile) {
                alert("Please upload an image before applying the watermark.");
                return;
            }

            const formData = new FormData();
            formData.append('image', imageFile);

            try {
                const response = await fetch('http://127.0.0.1:8000/upload/', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error(`Server responded with status ${response.status}`);
                }

                const result = await response.json();
                if (result.error) throw new Error(result.error);

                const watermarkedImg = document.getElementById('watermarked-preview');
                if (watermarkedImg) {
                    watermarkedImg.src = 'data:image/png;base64,' + result.image;
                    watermarkedImg.style.display = 'block';
                }

                const psnrElem = document.getElementById('psnr-value');
                const ssimElem = document.getElementById('ssim-value');
                if (psnrElem) psnrElem.textContent = `PSNR: ${result.psnr} dB`;
                if (ssimElem) ssimElem.textContent = `SSIM: ${result.ssim}`;

                const link = document.getElementById('download-link');
                if (link && watermarkedImg?.src) {
                    link.href = watermarkedImg.src;
                    link.style.display = 'inline-block';
                }

            } catch (error) {
                console.error("Error processing watermark:", error);
                alert("Failed to apply watermark: " + error.message);
            }
        });
    }

    // Extract watermark button
    const extractBtn = document.getElementById('extract-watermark');
    if (extractBtn) {
        extractBtn.addEventListener('click', async function () {
            const imageFile = document.getElementById('image-upload').files[0];

            if (!imageFile) {
                alert("Please upload the watermarked image.");
                return;
            }

            const formData = new FormData();
            formData.append('image', imageFile);

            try {
                const response = await fetch('http://127.0.0.1:8000/extract/', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) throw new Error(`Server error: ${response.status}`);

                const result = await response.json();
                if (result.error) throw new Error(result.error);

                const extractedImg = document.getElementById('extracted-preview');
                extractedImg.src = 'data:image/png;base64,' + result.image;
                extractedImg.style.display = 'block';

                document.getElementById('psnr-after').textContent = `PSNR After: ${result.psnr} dB`;
                document.getElementById('ssim-after').textContent = `SSIM After: ${result.ssim}`;

                const link = document.getElementById('download-extracted-link');
                link.href = extractedImg.src;
                link.style.display = 'inline-block';

            } catch (error) {
                console.error("Error extracting watermark:", error);
                alert("Failed to extract watermark: " + error.message);
            }
        });
    }
});
