import os
import json

# Define paths
base_dir = "/detectree/coco_files"
output_files = {
    "train": os.path.join(base_dir, "all_train.json"),
    "val": os.path.join(base_dir, "all_val.json"),
    # "test": os.path.join(base_dir, "all_test.json"),
}

# Initialize the merged data structure
merged_data = {
    "train": {"images": [], "annotations": [], "categories": []},
    "val": {"images": [], "annotations": [], "categories": []},
    # "test": {"images": [], "annotations": [], "categories": []},
}

# Prefix variable
prefix = 1

# Iterate through subfolders
for subfolder in os.listdir(base_dir):
    # Exclude citypark, meadow, redwood folders
    if subfolder in ["citypark", "meadow", "redwood"]:
        continue
    subfolder_path = os.path.join(base_dir, subfolder)
    if not os.path.isdir(subfolder_path):
        continue

    # Process train.json, val.json, test.json
    for split in ["train", "val"]:
        json_file_path = os.path.join(subfolder_path, f"{split}.json")
        if not os.path.exists(json_file_path):
            continue

        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)

        # Update file_name and ID, and merge data
        for image in data["images"]:
            image["file_name"] = f"{subfolder}/rgb/{image['file_name']}"
            image["id"] = int(f"{prefix}{image['id']}")
            merged_data[split]["images"].append(image)

        for annotation in data["annotations"]:
            annotation["image_id"] = int(f"{prefix}{annotation['image_id']}")
            annotation["id"] = int(f"{prefix}{annotation['id']}")
            merged_data[split]["annotations"].append(annotation)

        if "categories" in data and not merged_data[split]["categories"]:
            merged_data[split]["categories"] = data["categories"]

    # Increase prefix after processing each subfolder
    prefix += 1

# Write the merged JSON files
for split in ["train", "val"]:
    with open(output_files[split], "w") as output_file:
        json.dump(merged_data[split], output_file)

print("JSON files merged and ID conflicts resolved!")