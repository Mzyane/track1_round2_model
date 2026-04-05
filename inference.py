# inference.py
import os
import json
import numpy as np
import torch
from PIL import Image
from torchvision import transforms
from model import UNet

# -------------------------------
# Class mapping (dataset colors → indices)
# -------------------------------
CLASS_MAP = {
    (0,0,0):0,       # Background
    (0,255,0):1,     # Farmland
    (255,0,0):2,     # Built-up
    (0,0,255):3      # Water
}

def rgb_to_class(mask, tol=10):
    h, w, _ = mask.shape
    class_mask = np.zeros((h, w), dtype=np.int64)
    for rgb, idx in CLASS_MAP.items():
        diff = np.abs(mask - np.array(rgb))
        matches = np.all(diff <= tol, axis=-1)
        class_mask[matches] = idx
    return class_mask

# -------------------------------
# Prediction function
# -------------------------------
def predict(model, img_path, device):
    img = Image.open(img_path).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize((256,256)),
        transforms.ToTensor()
    ])
    tensor = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        out = model(tensor)
        mask = torch.argmax(out, dim=1).squeeze().cpu().numpy()
    # Resize back to 512x512
    mask_img = Image.fromarray(mask.astype(np.uint8))
    mask_img = mask_img.resize((512,512), Image.NEAREST)
    return np.array(mask_img)

# -------------------------------
# Main pipeline
# -------------------------------
def run_pipeline(data_dir="/input", result_dir="/output"):
    # Load model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = UNet().to(device)
    model.load_state_dict(torch.load("models/farmland.pth", map_location="cpu"))
    model.eval()

    # Prepare output JSON
    results = []

    # Iterate over test images
    region_dir = os.path.join(data_dir, "region_test")
    for img_file in os.listdir(region_dir):
        img_path = os.path.join(region_dir, img_file)
        mask = predict(model, img_path, device)

        # Binary mask for farmland (class = 1)
        binary_mask = (mask == 1).astype(np.uint8)

        # Compliance check
        uniques = np.unique(binary_mask)
        valid = (binary_mask.shape == (512,512)) and set(uniques).issubset({0,1})

        results.append({
            "filename": img_file,
            "shape": list(binary_mask.shape),
            "unique_values": uniques.tolist(),
            "valid": valid
        })

    # Save results to /output/result.json
    os.makedirs(result_dir, exist_ok=True)
    out_path = os.path.join(result_dir, "result.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"✅ Inference complete, results saved to {out_path}")

if __name__ == "__main__":
    run_pipeline()
