import logging
import tkinter as tk
from tkinter import filedialog

import cv2
import numpy as np
from PIL import Image, ImageTk
from matplotlib import pyplot as plt

from src.LoadLoggingConfig import load_logging_config
from src.app.EventDetection import EventDetection
from src.db.DatabaseManager import DatabaseManager


class EventDetectionUI :
    def __init__(self, root) :
        self.detected_objects_buttons_dict = {}
        try :
            # Load logging configuration
            load_logging_config()
            # Get the logger for the 'staging' logger
            self.logger = logging.getLogger('staging')

            # Set the root window for the UI
            self.root = root
            # Set the title and make the window non-resizable
            self.root.title("Object Detection Application")
            self.root.resizable(False, False)

            # Create instances of EventDetection and DatabaseManager
            self.backend = EventDetection()
            self.db_manager = DatabaseManager()

            # Initialize variables for image path and image
            self.image_path = ""
            self.image = None

            # Create a canvas for displaying images
            self.canvas = tk.Canvas(root, width=500, height=500)
            self.canvas.pack()

            # Create a button to select an image and bind it to the select_image method
            self.select_button = tk.Button(root, text="Select Image", command=self.select_image)
            self.select_button.pack()

            # Create a label to display information and bind it to a StringVar
            self.label_text = tk.StringVar()
            self.label = tk.Label(root, textvariable=self.label_text)
            self.label.pack()

            # Initialize a list to store buttons for detected objects
            self.detected_objects_buttons = []  # List to store buttons
        except Exception as e :
            # Log an error if any exception occurs during UI initialization
            self.logger.error("An error occurred during UI initialization: %s", str(e))

    def select_image(self) :
        """
            This method allows the user to select an image using a file dialog.
            It reads the selected image using OpenCV and displays it on the canvas.

            :return:

        """
        try :
            # Open a file dialog to select an image
            self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])

            if self.image_path :
                # Log the selected image path
                self.logger.info("Selected image path: " + self.image_path)
                # Load the selected image using OpenCV
                self.image = cv2.imread(self.image_path)

                if self.image is not None :
                    # Log the successful image loading
                    self.logger.info("Image loaded successfully.")
                    # Display the loaded image
                    self.display_image()

                    self.detect_objects()
                    # self.select_button.pack_forget()
                else :
                    # If image loading fails, raise a RuntimeError and log the error
                    raise RuntimeError("Failed to load image.")
                    return
        except Exception as e :
            # Log an error if any exception occurs during image selection
            self.logger.error("An error occurred during image selection: %s", str(e))

    def detect_objects(self) :
        """
            This method detects objects in the selected image using the backend.
            It updates the UI with the detected objects and their labels.

            :return:

        """
        try :
            # Check if both the image and its path are available
            if self.image is not None and self.image_path :
                # Detect objects in the selected image
                detected_objects = self.backend.detect_objects(self.image_path)

                # Log the selected image path and detected objects
                self.logger.info("Image path: " + self.image_path)
                self.logger.info("Detected objects: " + str(detected_objects))

                # Update the label to show detecting status
                self.label_text.set("Detected Objects: Detecting...")

                # Create a list to store unique detected object labels
                unique_detected_objects = []
                for obj_label, coords, confidence in detected_objects :
                    unique_detected_objects.append((obj_label, confidence))

                # Insert detected objects into the database
                self.db_manager.insert_detected_objects(detected_objects)
                self.db_manager.close_connection()
                self.display_image()

                if not detected_objects :
                    # No objects detected
                    self.label_text.set("Detected Objects: No objects detected")
                    raise RuntimeError("No objects detected")
                    return

                # Clear existing buttons
                for button in self.detected_objects_buttons :
                    button.destroy()
                self.detected_objects_buttons.clear()

                # Update the detected objects with buttons
                for obj_label, confidence in unique_detected_objects :
                    button = tk.Button(self.root, text=f"Generate histogram for object: {obj_label} ({confidence * 100:.2f}%)",
                                       command=lambda label=obj_label : self.display_selected_object(label))
                    button.pack()
                    self.detected_objects_buttons.append(button)
                    self.detected_objects_buttons_dict[obj_label] = button

                # Update the label to show the list of detected objects
                self.label_text.set(
                    "Detected Objects: {0}".format(
                        ", ".join([f"{obj} ({conf * 100:.2f}%)" for obj, conf in unique_detected_objects]))
                )
        except Exception as e :
            # Log an error if any exception occurs during object detection
            self.logger.error("An error occurred during object detection: %s", str(e))

    def display_selected_object(self, obj_label) :
        """
            This method displays a selected object along with its label on the canvas.
            It resizes the image, adjusts object coordinates, draws a bounding box, and displays the label.

            :param obj_label:
            :return:
        """
        try :
            # Check if the button for the selected object exists
            if obj_label not in self.detected_objects_buttons_dict :
                self.label_text.set("Selected object button does not exist.")
                raise RuntimeError("Selected object button does not exist.")
                return

            # Check if both the image and its path are available
            if self.image is not None and self.image_path :
                button = self.detected_objects_buttons_dict.get(obj_label)
                if button :

                    # Detect objects in the selected image
                    detected_objects = self.backend.detect_objects(self.image_path)

                    selected_img = self.image.copy()
                    # Resize the image for displaying the label
                    selected_img = cv2.resize(selected_img, (500, 500))

                    # Iterate through detected objects and their coordinates
                    for obj_label_detected, coords, confidence in detected_objects :

                        # Check if the detected object matches the requested label
                        if obj_label_detected == obj_label :
                            x, y, w, h = coords
                            h, w, x, y = self.adjust_object_coordinates(h, w, x, y)

                            # Draw a bounding box around the object and display the label and confidence
                            cv2.rectangle(selected_img, (x, y), (x + w, y + h), (255, 255, 0), 2)
                            label_position = (x, y + h + 20)  # Adjust label position
                            label_text = f"{obj_label} ({confidence * 100:.2f}%)"
                            cv2.putText(selected_img, label_text, label_position, cv2.FONT_HERSHEY_TRIPLEX, 0.5,
                                        (0, 0, 0), 2)

                    # Convert the OpenCV image to PIL format
                    img_pil = Image.fromarray(np.uint8(selected_img))
                    img_tk = ImageTk.PhotoImage(image=img_pil)

                    # Display the modified image on the canvas
                    self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
                    self.canvas.image = img_tk

                    selected_object_data = []

                    for item in detected_objects :
                        if item[0] == obj_label :
                            selected_object_data.append(item)
                    if selected_object_data :
                        self.generate_histogram(selected_object_data)

        except Exception as e :
            # Log an error if any exception occurs during displaying the selected object
            self.logger.error("An error occurred in display_selected_object: %s", str(e))

    def display_image(self) :
        try :
            # Convert and resize the image for display
            img = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (500, 500))
            detected_objects = self.backend.detect_objects(self.image_path)

            # Loop through detected objects and their coordinates
            for obj_label, coords, confidence in detected_objects :  # Added 'confidence'
                x, y, w, h = coords

                h, w, x, y = self.adjust_object_coordinates(h, w, x, y)

                # Draw a bounding box and display the label with confidence on the image
                label_text = f"{obj_label} ({confidence * 100:.2f}%)"  # Adding confidence to the label
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
                label_position = (x, y + h + 20)
                cv2.putText(img, label_text, label_position, cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 0), 2)

            # Convert the OpenCV image to PIL format
            img_pil = Image.fromarray(np.uint8(img))
            img_tk = ImageTk.PhotoImage(image=img_pil)

            # Display the modified image on the canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.canvas.image = img_tk

            # Check if the image is not loaded
            if self.image is None :
                raise RuntimeError("Image not loaded!")

        except Exception as e :
            # Log an error if any exception occurs during image display
            self.logger.error("An error occurred during image display: %s", str(e))

    def update_detected_objects(self, detected_objects) :
        """
            This method updates the displayed list of detected objects on the GUI.

            :param detected_objects:  list of detected objects
            :return:
        """
        try :
            # Update the label text with the list of detected objects
            self.label_text.set("Detected Objects: " + ", ".join(detected_objects))
            # Update the GUI to reflect the changes
            self.root.update()
        except Exception as e :
            # Log an error if an exception occurs during updating detected objects
            self.logger.error("An error occurred during updating detected objects: %s", str(e))

    def adjust_object_coordinates(self, h, w, x, y) :
        # Adjust object coordinates for the resized image
        x = int(x * 500 / self.image.shape[1])
        y = int(y * 500 / self.image.shape[0])
        w = int(w * 500 / self.image.shape[1])
        h = int(h * 500 / self.image.shape[0])
        return h, w, x, y

    def generate_histogram(self, detected_objects) :
        """
            Plot a histogram for the combined color channels of the detected object.
            Plot histograms for the color channels of the detected object.
        """
        try :
            selected_object_data = detected_objects[-1]  # Get data for the last detected object
            if selected_object_data :
                selected_img = cv2.imread(self.image_path)
                x, y, w, h = selected_object_data[1]  # Get coordinates of the detected object

                # Extract the region of interest (ROI) from the image
                roi = selected_img[y :y + h, x :x + w]

                # Calculate histograms for the color channels (red, green, blue)
                colors = ('b', 'g', 'r')
                plt.figure(figsize=(10, 6))
                for i, color in enumerate(colors) :
                    hist = cv2.calcHist([roi], [i], None, [256], [0, 256])
                    plt.plot(hist, color=color, label=f'Channel {color.upper()}')
                plt.title('Color Channels Histogram')
                plt.xlabel('Pixel Value')
                plt.ylabel('Frequency')
                plt.legend()
                plt.grid(True)
                plt.show()

        except Exception as e :
            # Handle and log any errors that might occur during histogram generation
            self.logger.error("An error occurred during generating histogram: %s", str(e))