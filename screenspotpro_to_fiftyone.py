import os
import json
import glob
from pathlib import Path
import fiftyone as fo

# Paths to your dataset
DATASET_ROOT = "ScreenSpot-Pro"
ANNOTATIONS_DIR = os.path.join(DATASET_ROOT, "annotations")
IMAGES_DIR = os.path.join(DATASET_ROOT, "images")

def convert_bbox_to_relative(bbox, img_size):
    """
    Convert absolute bounding box coordinates to relative coordinates.
    
    Args:
        bbox (list): Absolute bounding box in format [x1, y1, x2, y2]
        img_size (list): Image dimensions in format [width, height]
    
    Returns:
        list: Relative bounding box in format [x, y, width, height] in range [0, 1]
    """
    img_width, img_height = img_size
    x1, y1, x2, y2 = bbox
    
    # Convert to relative coordinates (normalized between 0 and 1)
    rel_x = x1 / img_width
    rel_y = y1 / img_height
    rel_width = (x2 - x1) / img_width  # Width is relative to image width
    rel_height = (y2 - y1) / img_height  # Height is relative to image height
    
    return [rel_x, rel_y, rel_width, rel_height]

def parse_annotation_files():
    """
    Parse all annotation files and create FiftyOne samples.
    
    Reads all JSON annotation files from the annotations directory,
    processes each entry, and creates a list of FiftyOne samples
    with the required fields.
    
    Returns:
        list: List of FiftyOne Sample objects
    """
    samples = []
    
    # Get all JSON annotation files
    annotation_files = glob.glob(os.path.join(ANNOTATIONS_DIR, "*.json"))
    
    for annotation_file in annotation_files:
        print(f"Processing {os.path.basename(annotation_file)}...")
        
        # Load annotation file
        with open(annotation_file, 'r', encoding='utf-8') as f:
            annotations = json.load(f)
        
        # Process each annotation entry in the JSON file
        for annotation in annotations:
            # Construct full image path
            image_path = os.path.join(IMAGES_DIR, annotation["img_filename"])
            
            # Skip if image doesn't exist
            if not os.path.exists(image_path):
                print(f"Warning: Image not found: {image_path}")
                continue
            
            # Convert bounding box to relative coordinates (FiftyOne format)
            bbox_relative = convert_bbox_to_relative(annotation["bbox"], annotation["img_size"])
            
            # Create detection object for the UI element
            # Label will be the ui_type value (e.g., "icon" or "text")
            detection = fo.Detection(
                label=annotation["ui_type"],
                bounding_box=bbox_relative
            )
            
            # Create base sample with filepath
            sample = fo.Sample(filepath=image_path)
            
            # Add fields to sample explicitly
            sample["ui_id"] = annotation["id"]
            sample["instruction"] = annotation["instruction"]
            sample["application"] = fo.Classification(label=annotation["application"])
            sample["group"] = fo.Classification(label=annotation["group"])
            sample["platform"] = fo.Classification(label=annotation["platform"])
            sample["action_detection"] = detection
            
            samples.append(sample)
    
    print(f"Processed {len(samples)} samples total")
    return samples

def main():
    """
    Main function to create and populate the FiftyOne dataset.
    
    Creates a new dataset named "ScreenSpot_Pro", parses all annotation files,
    adds samples to the dataset, computes metadata, and adds dynamic sample fields.
    
    Returns:
        fo.Dataset: The created FiftyOne dataset
    """
    # Create dataset (overwrite if exists)
    dataset = fo.Dataset("ScreenSpot_Pro", overwrite=True)

    samples = parse_annotation_files()

    dataset.add_samples(samples)
    
    dataset.compute_metadata()
    
    dataset.add_dynamic_sample_fields()
    
    view = dataset.group_by(
        "application.label",
        order_by="ui_id"
        )
    dataset.save_view("applications", view)
    dataset.save()
    return dataset