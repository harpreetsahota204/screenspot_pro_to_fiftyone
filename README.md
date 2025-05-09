# Parsing the ScreenSpot-Pro Dataset to FiftyOne Format


<img src="screenspot_pro.gif">


This is a [FiftyOne](https://github.com/voxel51/fiftyone) dataset with 1581 samples.

## This dataset has been parsed and pushed to the Hugging Face Hub:

If you haven't already, install FiftyOne:

```bash
pip install -U fiftyone
```

## Usage

```python
import fiftyone as fo
from fiftyone.utils.huggingface import load_from_hub

# Load the dataset
# Note: other available arguments include 'max_samples', etc
dataset = load_from_hub("Voxel51/ScreenSpot-Pro")

# Launch the App
session = fo.launch_app(dataset)
```

## Dataset Details

### Dataset Description

ScreenSpot-Pro is a novel benchmark designed to evaluate the GUI grounding capabilities of multimodal large language models (MLLMs) in high-resolution professional environments. Unlike previous benchmarks that focus on general and easy tasks, ScreenSpot-Pro captures the unique challenges posed by professional software applications, including higher screen resolutions, smaller relative target sizes, and complex interfaces. The benchmark comprises 1,581 authentic high-resolution screenshots spanning 23 professional applications across 5 industries (Development, Creative, CAD, Scientific, and Office) and 3 operating systems, each annotated with precise bounding boxes for target UI elements and corresponding natural language instructions.

- **Curated by:** Kaixin Li (National University of Singapore), Ziyang Meng (East China Normal University), Hongzhan Lin, Ziyang Luo, Yuchen Tian, Jing Ma (Hong Kong Baptist University), Zhiyong Huang, Tat-Seng Chua (National University of Singapore)
- **Language(s) (NLP):** en only
- **License:** [More Information Needed]

### Dataset Sources

- **Repository:** https://github.com/likaixin2000/ScreenSpot-Pro-GUI-Grounding and https://huggingface.co/datasets/likaixin/ScreenSpot-Pro
- **Paper :** [ScreenSpot-Pro: GUI Grounding for Professional High-Resolution Computer Use](https://arxiv.org/abs/2504.07981)

## Uses

### Direct Use

ScreenSpot-Pro is designed for evaluating and benchmarking GUI grounding capabilities of multimodal models in professional high-resolution environments. It can be used to:

1. Assess the ability of models to locate specific UI elements based on natural language instructions
2. Benchmark performance of GUI agents on professional software applications
3. Develop and evaluate methods for handling high-resolution inputs in multimodal systems
4. Research techniques for improving visual search and element identification in complex interfaces

### Out-of-Scope Use

The dataset is specifically designed for GUI grounding evaluation and should not be used for:

1. Training or evaluating full agent planning and execution tasks
2. Developing automated systems that might violate software licensing agreements
3. Creating tools that could enable unauthorized automation of proprietary software
4. Inferring user behaviors or patterns from the collected data

## Dataset Structure

The dataset consists of 1,581 instruction-image pairs across 23 applications. Each sample includes:

1. A high-resolution screenshot (resolutions vary, with the most common being 2560×1440 at 32.4% of the data)
2. A natural language instruction describing the target UI element
3. A bounding box annotation specifying the target location
4. The type of the target element (text or icon)
5. The source application information

The dataset is categorized into 6 application types:
- Development and Programming (254 samples)
- Creative Software (306 samples)
- CAD and Engineering (261 samples)
- Scientific and Analytical (237 samples)
- Office Software (230 samples)
- Operating System Commons (196 samples)

Icons constitute 61.8% of the elements, with texts comprising the remainder. Target elements in ScreenSpot-Pro occupy only 0.07% of the screenshot area on average.

## FiftyOne Dataset Structure

**Basic Info:** 1,581 desktop application screenshots with interaction annotations

**Core Fields:**

- `ui_id`: StringField - Unique identifier for the UI screen
- `instruction`: StringField - Natural language task description, note only the English instruction is parsed
- `application`: EmbeddedDocumentField(Classification) - Application name (e.g., "word")
- `group`: EmbeddedDocumentField(Classification) - Application category (e.g., "Office")
- `platform`: EmbeddedDocumentField(Classification) - Operating system (e.g., "macos")
- `action_detection`: EmbeddedDocumentField(Detection) - Target interaction element:
  - `label`: Element type (e.g., "text")
  - `bounding_box`: a list of relative bounding box coordinates in [0, 1] in the following format:`[<top-left-x>, <top-left-y>, <width>, <height>]`

The dataset captures desktop application interfaces across various platforms with natural language instructions and target interaction elements. It focuses on specific UI elements that should be interacted with to complete tasks in desktop applications like Microsoft Word, organized by application type and operating system.


## Dataset Creation

### Curation Rationale

ScreenSpot-Pro was created to address the limitations of existing GUI grounding benchmarks, which primarily focus on simple tasks and cropped screenshots. Professional applications introduce unique challenges for GUI perception models, including high-resolution displays, smaller target sizes, and complex environments that are not well-represented in current benchmarks. The dataset aims to provide a more rigorous evaluation framework that reflects real-world professional computing scenarios.

### Source Data

#### Data Collection and Processing

The data collection prioritized authentic high-resolution screenshots from professional software usage:

1. Experts with at least five years of experience using relevant applications were invited to record data
2. Participants performed their regular work routines to ensure task authenticity
3. A custom screen capture tool was developed, accessible via shortcut key, to minimize workflow disruption
4. The tool allowed experts to take screenshots and label bounding boxes and instructions in real-time
5. Screens with resolution greater than 1080p (1920×1080) were prioritized
6. Monitor scaling was disabled during capture
7. For dual-monitor setups, images were captured spanning both displays
8. UI elements were classified as either "text" or "icon" based on refined criteria

#### Who are the source data producers?

The source data producers are expert users with at least five years of experience using the relevant professional applications. They come from various professional domains including software development, creative design, engineering, scientific research, and office productivity.

### Annotations

#### Annotation process

The annotation process was designed to ensure high quality and authenticity:

1. Experts used a custom screen capture tool that overlays the screenshot directly on their screen
2. They labeled bounding boxes by dragging and providing instructions directly through the tool
3. This real-time annotation eliminated the need to recall contexts after the fact
4. Each instance was reviewed by at least two annotators to ensure correct instructions and target bounding boxes
5. Ambiguous instructions were resolved to guarantee only one target per instruction
6. Annotators precisely verified the interactable regions of GUI elements, excluding irrelevant areas

#### Who are the annotators?

The annotators are the same expert users who produced the source data - professionals with at least five years of experience using the relevant applications. This ensures that annotations reflect domain expertise and understanding of professional software workflows.

#### Personal and Sensitive Information

The dataset consists of screenshots of professional software interfaces and does not inherently contain personal or sensitive information. However, the paper does not explicitly address whether any potential personal content visible in the screenshots (like document text, filenames, etc.) was anonymized.

## Bias, Risks, and Limitations

The dataset has several limitations:

1. It focuses exclusively on GUI grounding and excludes agent planning and execution tasks
2. The extremely small relative size of targets (0.07% of screen area on average) presents a significant challenge
3. The benchmark may not fully capture the diversity of professional software configurations and customizations
4. The paper acknowledges legal considerations related to software licensing that limited certain aspects of data collection
5. The dataset's focus on high-resolution professional applications may not generalize to other GUI contexts

### Recommendations

When using this dataset, researchers should:

1. Be aware of the legal considerations regarding software licensing and automation
2. Consider the extreme challenge posed by small target sizes in high-resolution images
3. Recognize that performance on this benchmark may not directly translate to other GUI contexts
4. Be cautious about potential biases in task selection or application representation
5. Consider developing specialized methods for handling high-resolution inputs, as demonstrated by the authors' ScreenSeekeR approach

## Citation

**BibTeX:**

```bibtex
@misc{li2024screenspot-pro,
      title={ScreenSpot-Pro: GUI Grounding for Professional High-Resolution Computer Use}, 
      author={Kaixin Li and Ziyang Meng and Hongzhan Lin and Ziyang Luo and Yuchen Tian and Jing Ma and Zhiyong Huang and Tat-Seng Chua},
      year={2025},
}
```

**APA:**

Li, K., Meng, Z., Lin, H., Luo, Z., Tian, Y., Ma, J., Huang, Z., & Chua, T.-S. (2025). ScreenSpot-Pro: GUI Grounding for Professional High-Resolution Computer Use.

## Dataset Card Contact

https://github.com/likaixin2000/ScreenSpot-Pro-GUI-Grounding
