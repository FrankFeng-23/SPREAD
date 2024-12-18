import os
import json
import numpy as np
from skimage.draw import polygon  # Used to generate coordinates inside the polygon
from multiprocessing import Pool

# Define folders and paths
base_folder = 'coco_files'
folders = ['citypark', 'rainforest', 'redwood']

# Helper function: calculate overlap ratio
def calculate_overlap_ratio(mask1, mask2, instance_area):
    intersection = np.logical_and(mask1, mask2).sum()
    return intersection / instance_area

# Define the function to process a single file
def process_coco_file(folder_name):
    coco_file_path = os.path.join(base_folder, folder_name, f"{folder_name}_coco.json")
    
    # Load COCO file
    with open(coco_file_path, 'r') as f:
        coco_data = json.load(f)

    # Prepare data
    images = {img['id']: img for img in coco_data['images']}
    annotations = coco_data['annotations']

    # Store filtered annotations and images
    filtered_annotations = []
    filtered_images = []

    # Process by image
    for image_id, image_info in images.items():
        img_annotations = [ann for ann in annotations if ann['image_id'] == image_id]

        # Sort by area in descending order
        img_annotations.sort(key=lambda x: x['area'], reverse=True)

        # Create background mask
        img_height, img_width = image_info['height'], image_info['width']
        background_mask = np.zeros((img_height, img_width), dtype=bool)

        filtered_image_annotations = []
        for ann in img_annotations:
            # Create binary mask for the current instance
            instance_mask = np.zeros((img_height, img_width), dtype=bool)
            segmentation = ann['segmentation']
            for seg in segmentation:
                poly = np.array(seg).reshape(-1, 2)
                x, y = poly[:, 0], poly[:, 1]
                
                # Use skimage.draw.polygon to fill the polygon
                rr, cc = polygon(y, x, shape=(img_height, img_width))
                instance_mask[rr, cc] = True

            # Calculate overlap ratio
            overlap_ratio = calculate_overlap_ratio(instance_mask, background_mask, ann['area'])
            if overlap_ratio > 0.5:  # If overlap ratio is greater than the threshold, skip
                continue

            # If it passes the check, add the instance to the keep list and update the background mask
            filtered_image_annotations.append(ann)
            background_mask = np.logical_or(background_mask, instance_mask)

        # Add image and its kept instances
        if filtered_image_annotations:
            filtered_annotations.extend(filtered_image_annotations)
            filtered_images.append(image_info)

    # Save as a new COCO file
    filtered_coco = {
        "images": filtered_images,
        "annotations": filtered_annotations,
        "categories": coco_data["categories"]
    }

    # Save to file
    save_path = os.path.join(base_folder, folder_name, f"{folder_name}_filtered.json")
    with open(save_path, 'w') as f:
        json.dump(filtered_coco, f, separators=(',', ':'))

    print(f"Filtered COCO file saved as '{save_path}'")

# Use multiprocessing to process in parallel
if __name__ == "__main__":
    with Pool(processes=len(folders)) as pool:
        pool.map(process_coco_file, folders)