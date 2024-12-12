# YOLOv8 Training and Inference Readme

This guide provides instructions for training and performing inference using YOLOv8 on the Roboflow platform in a Google Colab environment. YOLOv8 is a state-of-the-art real-time object detection algorithm. The training dataset is sourced from Roboflow, and the trained model is saved for future use.

## Setup

1. Set up the Colab environment and mount Google Drive:

```python
import os
HOME = os.getcwd()
print(HOME)

from google.colab import drive
drive.mount('/content/drive')
```

2. Install the required dependencies:

```python
!pip install ultralytics #==8.0.20
```

3. Clear any previous display outputs:

```python
from IPython import display
display.clear_output()
```

4. Check Ultralytics installation:

```python
import ultralytics
ultralytics.checks()
```

5. Import necessary modules and set up the dataset directory:

```python
from ultralytics import YOLO
from roboflow import Roboflow

!mkdir {HOME}/datasets
%cd {HOME}/datasets
```

6. Install the Roboflow Python package:

```python
!pip install roboflow
```

7. Initialize Roboflow with your API key, workspace, project, and version details:

```python
from roboflow import Roboflow
rf = Roboflow(api_key="your_api_key")
project = rf.workspace("your_workspace").project("your_project")
dataset = project.version(your_version).download("yolov4")
```

8. Return to the home directory:

```python
%cd {HOME}
```

## Training YOLOv8

1. Initialize YOLOv8 model:

```python
model = YOLO()
```

2. Train the model:

```python
model.train(data="/content/datasets/Capstone-Project-6/data.yaml", epochs=200, plots=True)
```

3. View training results:

```python
!ls {HOME}/runs/detect/train/
```

4. Display the confusion matrix:

```python
%cd {HOME}
from IPython.display import Image
Image(filename=f'{HOME}/runs/detect/train/confusion_matrix.png', width=600)
```

5. Display the results:

```python
%cd {HOME}
Image(filename=f'{HOME}/runs/detect/train/results.png', width=600)
```

6. Display a prediction on a validation image:

```python
%cd {HOME}
Image(filename=f'{HOME}/runs/detect/train/val_batch0_pred.jpg', width=900)
```

7. Save the trained model to Google Drive:

```python
!cp -r /content/runs/detect/train /content/drive/MyDrive/NUST
%cd {HOME}
```

## Inference and Prediction

1. Perform inference on the validation set:

```python
%cd {HOME}
!yolo task=detect mode=val model={HOME}/runs/detect/train/weights/best.pt data={dataset.location}/data.yaml
```

2. Perform inference on the test set:

```python
%cd {HOME}
!yolo task=detect mode=predict model={HOME}/runs/detect/train/weights/best.pt conf=0.25 source={dataset.location}/test/images save=True
```

3. Display a few validation images with predictions:

```python
import glob
from IPython.display import Image, display

for image_path in glob.glob(f'{HOME}/runs/detect/val/*.jpg')[:5]:
    display(Image(filename=image_path, width=600))
    print("\n")
```

4. Display a few validation images with predictions in PNG format:

```python
import glob
from IPython.display import Image, display

for image_path in glob.glob(f'{HOME}/runs/detect/val/*.png')[:5]:
    display(Image(filename=image_path, width=600))
    print("\n")
```

Feel free to customize and extend these instructions based on your specific project requirements.