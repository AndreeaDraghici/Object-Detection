## Image Detection App

The application combines GUI, image processing and machine learning techniques to provide a simple and interactive
experience for detecting and viewing objects in images.

-------------------

## How to run

1. **Python version:** Used Python 3.10.

You can check the version of Python using the command on the command line:

```python --version or python3 --version```

2. **Required Libraries:** The application uses the following libraries, so make sure you have them installed:

    - ***tkinter:*** This is the standard library for graphical interfaces in Python. Most Python distributions already
      include this library.

    - ***cv2 (OpenCV):*** For image manipulation and object detection processing.

    - ***numpy:*** For efficient manipulation of image data.

    - ***PIL (Pillow):*** For converting images between different formats.

    - ***matplotlib:*** For creating plot statistics about image processing and image confidence.

### ***To install the necessary libraries you have two possibility:***

1. To install the necessary dependencies in your environment you can use the ***requirements.txt*** file.

Simply run the following command in the project directory to install the dependencies:

```pip install -r requirements.txt```

2. To install manual the libraries in Python, you can use the pip install <library_name> command like below.

```pip install opencv-python```

Or for all required libraries you could use the next command in command prompt to install all necessary libraries:

```pip install opencv-python numpy pillow matplotlib```

3. **Running:** After you have installed the necessary libraries , you can run the application by running the main.py
   file.
   Use the command line to navigate to the directory where this file is located and then run it using the command:

To navigate to the directory you can use the next command:

```cd name_of_directory```

To run the application you can use the next command:

```python main.py or python3 main.py```

E.g:

```
cd MyProjectsDirectory

python main.py
```

------------------------

## About technical aspects

Object detection is a computer vision task that involves both localizing one or more objects within an image and
classifying each object in the image.

- Used a simple approach using the OpenCV library for object detection.


- Yolo is a faster object detection algorithm in computer vision and first described by Joseph Redmon, Santosh Divvala,
  Ross Girshick and Ali Farhadi in 'You Only Look Once: Unified, Real-Time Object Detection'

To be able to recognize objects in images and label them with the appropriate types, you can use a pre-trained deep
learning model for object detection, such as YOLO (You Only Look Once). These
models can recognize and label different types of objects in images.

To do this, you will need a convolutional neural network pre-trained on a large dataset containing various types of
objects. The model will provide you not only the regions where the objects were detected, but also the corresponding
labels (such as "fruit", "car", "animal", etc.).

Demonstrated how to use YOLO with the opencv-python library to detect and label objects in an image. To do this, you
need the pre-trained YOLO files that define the model and labels.

**Download the pre-trained YOLO files and tags:**

1. Download yolov3.weights file from: https://pjreddie.com/media/files/yolov3.weights


2. Download the yolov3.cfg file from: https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg


3. Download the coco.names file from: https://github.com/pjreddie/darknet/blob/master/data/coco.names

--------------------

## About Application

This is a GUI application (Tkinter Python based). App receives as input the path to the photo, and detect the object(s).
from photo.

After detecting an object, record its details in the SQLite database.

**This application includes:**

- A GUI using Tkinter Python.

- A SQLite database.

- A modular design with classes for different parts of the application.

------------------------

## About Implementation

The application is a GUI for object detection in images using machine learning algorithms. Here is a general description
of the app's main features and components:

1. **Graphical Interface (GUI):** The application has an intuitive graphical interface made using the tkinter library in
   Python.
   The GUI includes several key components:

    - A canvas (drawing area) where the selected image and detection results are displayed.

    - A "Select Image" button to load an image to analyze.

    - A "Detect Objects" button to initiate the process of detecting objects in the image.

    - A text field for displaying detection results.


2. **Object Detection:** The object detection process is done through the EventDetection class, which handles using a
   machine learning model (eg a model pre-trained on a dataset of objects). This model is used to identify and locate
   objects in the image.


3. **Database:** The application uses a SQLite database to store information about detected objects. The DatabaseManager
   class handles database management, including table creation and inserting object data.


4. **Application functionality:**

    - The user starts by selecting an image using the "Select Image" button.

    - The image is loaded into the application.

    - After the image is loaded, the user can press the "Detect Objects" button to initiate the process of detecting
      objects in the image.

    - The detection results are displayed in a text field and the labels of the detected objects are displayed.

    - After detecting the objects, the application displays the original image with the objects marked by borders and
      labels.

    - The user can click on object labels to display the image with a specific object highlighted.


5. **Image Resizing:** The uploaded image is resized to fit the display canvas. This ensures that the image and detected
   objects are displayed correctly in the GUI.


6. **Workflow:**

    - The user opens the application and uploads an image using the "Select Image" button.

    - Then, use the "Detect Objects" button to initiate object detection.

    - The detection results are displayed as the labels of the detected objects.

    - The user can click on the labels to display the image with the selected object highlighted.

--------------------

## Resources

1. Object Detection Wiki: https://en.wikipedia.org/wiki/Object_detection


2. YOLO Object Detection with OpenCV and
   Python: https://towardsdatascience.com/yolo-object-detection-with-opencv-and-python-21e50ac599e9


3. Object Recognition using Python: https://www.javatpoint.com/object-recognition-using-python


4. Detect an object with OpenCV-Python: https://www.geeksforgeeks.org/detect-an-object-with-opencv-python/


5. Object Detection with Python, Deep Learning, and
   OpenCV: https://dontrepeatyourself.org/post/object-detection-with-python-deep-learning-and-opencv/


6. Object Detection with Yolov3: https://github.com/patrick013/Object-Detection---Yolov3


7. Object detection and tracking in Python: https://www.r-bloggers.com/2021/09/object-detection-and-tracking-in-python/


8. Object Detection from Images with YOLO using Python:https://wellsr.com/python/object-detection-from-images-with-yolo/


9. More examples: https://github.com/topics/object-detection


10. OpenCV Documentation: https://docs.opencv.org/3.4/d0/d0f/tutorial_js_object_detection.html