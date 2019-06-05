from azure.cognitiveservices.vision.computervision import ComputerVisionClient

from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes

from msrest.authentication import CognitiveServicesCredentials

import os
import sys
import time

#   The Quickstarts in this file are for the Computer Vision API for Microsoft
#   Cognitive Services. In this file are Quickstarts for the following tasks:
#     - Describing images
#     - Categorizing images
#     - Tagging images
#     - Detecting faces
#     - Detecting adult or racy content
#     - Detecting the color scheme
#     - Detecting domain-specific content (celebrities/landmarks)
#     - Detecting image types (clip art/line drawing)
#     - Detecting objects
#     - Detecting brands
#     - Recognizing printed and handwritten text with the batch read API
#     - Recognizing printed text with OCR


#   Configure the Computer Vision client by:
#     1. Reading the Computer Vision API key and the Azure region from environment
#        variables (COMPUTERVISION_API_KEY and COMPUTERVISION_REGION), which must
#        be set prior to running this code. After setting the	environment variables,
#        restart your command shell or your IDE.
#     2. Constructing the endpoint URL from the base URL and the Azure region.
#     3. Setting up the authorization on the client with the subscription key.
#     4. Getting the context.
if 'COMPUTERVISION_API_KEY' in os.environ:
    computervision_api_key = os.environ['COMPUTERVISION_API_KEY']
else:
    print("\nPlease set the COMPUTERVISION_API_KEY environment variable.\n**Note that you might need to restart your shell or IDE.**")
    sys.exit()

if 'COMPUTERVISION_REGION' in os.environ:
    computervision_region = os.environ['COMPUTERVISION_REGION']
else:
    print("\nPlease set the COMPUTERVISION_REGION environment variable.\n**Note that you might need to restart your shell or IDE.**")
    sys.exit()

endpoint_url = "https://" + computervision_region + ".api.cognitive.microsoft.com"

computervision_client = ComputerVisionClient(endpoint_url, CognitiveServicesCredentials(computervision_api_key))
#	END - Configure the Computer Vision client

#   Get a local image for analysis
local_image_path = "resources\\faces.jpg"
print("\n\nLocal image path:\n" + os.getcwd() + local_image_path)
#   END - Get a local image for analysis

# Describe a local image by:
#   1. Opening the binary file for reading.
#   2. Defining what to extract from the image by initializing an array of VisualFeatureTypes.
#   3. Calling the Computer Vision service's analyze_image_in_stream with the:
#      - image
#      - features to extract
#   4. Displaying the image captions and their confidence values.
local_image = open(local_image_path, "rb")
description = computervision_client.describe_image_in_stream(local_image)

print("\nCaptions from local image: ")
if (len(description.captions) == 0):
    print("No captions detected.")
else:
    for caption in description.captions:
        print("'{}' with confidence {:.2f}%".format(caption.text, caption.confidence * 100))
#  END - Describe a local image

#   Get a remote image for analysis
remote_image_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/landmark.jpg"
print("\n\nRemote image URL:\n" + remote_image_url)
#   END - Get a remote image for analysis

# Describe a remote image by:
#   1. Defining what to extract from the image by initializing an array of VisualFeatureTypes.
#   2. Calling the Computer Vision service's analyze_image with the:
#      - image URL
#      - features to extract
#   3. Displaying the image captions and their confidence values.
description = computervision_client.describe_image(remote_image_url)

print("\nCaptions from remote image: ")
if (len(description.captions) == 0):
    print("No captions detected.")
else:
    for caption in description.captions:
        print("'{}' with confidence {:.2f}%".format(caption.text, caption.confidence * 100))
#   END - Describe a remote image


# Categorize a local image by:
#   1. Opening the binary file for reading.
#   2. Defining what to extract from the image by initializing an array of VisualFeatureTypes.
#   3. Calling the Computer Vision service's analyze_image_in_stream with the:
#      - image
#      - features to extract
#   4. Displaying the image categories and their confidence values.
local_image = open(local_image_path, "rb")
local_image_features = ["categories"]
local_image_analysis = computervision_client.analyze_image_in_stream(local_image, local_image_features)

print("\nCategories from local image: ")
if (len(local_image_analysis.categories) == 0):
    print("No categories detected.")
else:
    for category in local_image_analysis.categories:
        print("'{}' with confidence {:.2f}%".format(category.name, category.score * 100))
#   END - Categorize a local image

# Categorize a remote image by:
#   1. Calling the Computer Vision service's analyze_image with the:
#      - image URL
#      - features to extract
#   2. Displaying the image categories and their confidence values.
remote_image_features = ["categories"]
remote_image_analysis = computervision_client.analyze_image(remote_image_url, remote_image_features)

print("\nCategories from remote image: ")
if (len(remote_image_analysis.categories) == 0):
    print("No categories detected.")
else:
    for category in remote_image_analysis.categories:
        print("'{}' with confidence {:.2f}%".format(category.name, category.score * 100))
#   END - Categorize a remote image

# Tag a local image by:
#   1. Opening the binary file for reading.
#   2. Defining what to extract from the image by initializing an array of analyze_image_in_stream.
#   3. Calling the Computer Vision service's tag_image_in_stream with the:
#      - image
#      - features to extract
#   4. Displaying the image captions and their confidence values.
local_image = open(local_image_path, "rb")
local_image_analysis = computervision_client.tag_image_in_stream(local_image)

print("\nTags in the local image: ")
if (len(local_image_analysis.tags) == 0):
    print("No tags detected.")
else:
    for tag in local_image_analysis.tags:
        print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))
#   END - Tag a local image

# Tag a remote image by:
#   1. Calling the Computer Vision service's analyze_image with the:
#      - image URL
#      - features to extract
#   2. Displaying the image captions and their confidence values.
remote_image_analysis = computervision_client.tag_image(remote_image_url)

print("\nTags in the remote image: ")
if (len(remote_image_analysis.tags) == 0):
    print("No tags detected.")
else:
    for tag in remote_image_analysis.tags:
        print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))
#   END - Tag a remote image

# Detect faces in a local image by:
#   1. Opening the binary file for reading.
#   2. Defining what to extract from the image by initializing an array of VisualFeatureTypes.
#   3. Calling the Computer Vision service's analyze_image_in_stream with the:
#      - image
#      - features to extract
#   4. Displaying the image captions and their confidence values.
local_image = open(local_image_path, "rb")
local_image_features = ["faces"]
local_image_analysis = computervision_client.analyze_image_in_stream(local_image, local_image_features)

print("\nFaces in the local image: ")
if (len(local_image_analysis.faces) == 0):
    print("No faces detected.")
else:
    for face in local_image_analysis.faces:
        print("'{}' of age {} at location {}, {}, {}, {}".format(face.gender, face.age, \
        face.face_rectangle.left, face.face_rectangle.top, \
        face.face_rectangle.left + face.face_rectangle.width, \
        face.face_rectangle.top + face.face_rectangle.height))
#   END - Detect faces in a local image

# Detect faces in a remote image by:
#   1. Calling the Computer Vision service's analyze_image with the:
#      - image URL
#      - features to extract
#   2. Displaying the image captions and their confidence values.
remote_image_features = ["faces"]
remote_image_analysis = computervision_client.analyze_image(remote_image_url, remote_image_features)

print("\nFaces in the remote image: ")
if (len(remote_image_analysis.faces) == 0):
    print("No faces detected.")
else:
    for face in remote_image_analysis.faces:
        print("'{}' of age {} at location {}, {}, {}, {}".format(face.gender, face.age, \
        face.face_rectangle.left, face.face_rectangle.top, \
        face.face_rectangle.left + face.face_rectangle.width, \
        face.face_rectangle.top + face.face_rectangle.height))
#   END - Detect faces in a remote image

# Detect adult or racy content in a local image by:
#   1. Opening the binary file for reading.
#   2. Defining what to extract from the image by initializing an array of VisualFeatureTypes.
#   3. Calling the Computer Vision service's analyze_image_in_stream with the:
#      - image
#      - features to extract
#   4. Displaying the image captions and their confidence values.
local_image = open(local_image_path, "rb")
local_image_features = ["adult"]
local_image_analysis = computervision_client.analyze_image_in_stream(local_image, local_image_features)

print("\nAnalyzing local image for adult or racy content ... ")
print("Is adult content: {} with confidence {:.2f}%".format(local_image_analysis.adult.is_adult_content, local_image_analysis.adult.adult_score * 100))
print("Has racy content: {} with confidence {:.2f}%".format(local_image_analysis.adult.is_racy_content, local_image_analysis.adult.racy_score * 100))


# print("Is adult content: " + str(local_image_analysis.adult.is_adult_content) + " with confidence " + str(local_image_analysis.adult.adult_score))
# print("Has racy content: " + str(local_image_analysis.adult.is_racy_content) + " with confidence " + str(local_image_analysis.adult.racy_score))
#   END - Detect adult or racy content in a local image

# Detect adult or racy content in a remote image by:
#   1. Calling the Computer Vision service's analyze_image with the:
#      - image URL
#      - features to extract
#   2. Displaying the image captions and their confidence values.
remote_image_features = ["adult"]
remote_image_analysis = computervision_client.analyze_image(remote_image_url, remote_image_features)

print("\nAnalyzing remote image for adult or racy content ... ")
print("Is adult content: {} with confidence {:.2f}%".format(remote_image_analysis.adult.is_adult_content, local_image_analysis.adult.adult_score * 100))
print("Has racy content: {} with confidence {:.2f}%".format(remote_image_analysis.adult.is_racy_content, local_image_analysis.adult.racy_score * 100))
#   END - Detect adult or racy content in a remote image

# Detect the color scheme of a local image by:
#   1. Opening the binary file for reading.
#   2. Calling the Computer Vision service's analyze_image_in_stream with the:
#      - image
#      - features to extract
#   3. Displaying color scheme of the local image.
local_image = open(local_image_path, "rb")
local_image_features = ["color"]
local_image_analysis = computervision_client.analyze_image_in_stream(local_image, local_image_features)

print("\nColor scheme of the local image: ");
print("Is black and white: ".format(local_image_analysis.color.is_bw_img))
print("Accent color: 0x{}".format(local_image_analysis.color.accent_color))
print("Dominant background color: {}".format(local_image_analysis.color.dominant_color_background))
print("Dominant foreground color: {}".format(local_image_analysis.color.dominant_color_foreground))
print("Dominant colors: {}".format(local_image_analysis.color.dominant_colors))
#   END - Detect the color scheme in a local image

# Detect the color scheme of a remote image by:
#   1. Calling the Computer Vision service's analyze_image with the:
#      - image
#      - features to extract
#   2. Displaying color scheme of the local image.
remote_image_features = ["color"]
remote_image_analysis = computervision_client.analyze_image(remote_image_url, remote_image_features)

print("\nColor scheme of the remote image: ");
print("Is black and white: ".format(remote_image_analysis.color.is_bw_img))
print("Accent color: 0x{}".format(remote_image_analysis.color.accent_color))
print("Dominant background color: {}".format(remote_image_analysis.color.dominant_color_background))
print("Dominant foreground color: {}".format(remote_image_analysis.color.dominant_color_foreground))
print("Dominant colors: {}".format(remote_image_analysis.color.dominant_colors))
#   END - Detect the color scheme in a remote image

#   Detect domain-specific content (celebrities/landmarks) in a local image by:
#   1. Opening the binary file for reading.
#   2. Calling the Computer Vision service's analyze_image_by_domain_in_stream with the:
#      - domain-specific content to search for
#      - image
#   3. Displaying any domain-specific content (celebrities/landmarks).
local_image = open(local_image_path, "rb")
celebs = computervision_client.analyze_image_by_domain_in_stream("celebrities", local_image)

print("\nCelebrities in the local image:")
for celeb in celebs.result["celebrities"]:
    print(celeb["name"])

local_image = open(local_image_path, "rb")
landmarks = computervision_client.analyze_image_by_domain_in_stream("landmarks", local_image)

print("\nLandmarks in the local image:")
for landmark in landmarks.result["landmarks"]:
    print(landmark["name"])
#   END Detect domain-specific content (celebrities/landmarks) in a local image

#   Detect domain-specific content (celebrities/landmarks) in a remote image by:
#   1. Calling the Computer Vision service's analyze_image_by_domain with the:
#      - domain-specific content to search for
#      - image
#   2. Displaying any domain-specific content (celebrities/landmarks).
celebs = computervision_client.analyze_image_by_domain("celebrities", remote_image_url)

print("\nCelebrities in the remote image:")
for celeb in celebs.result["celebrities"]:
    print(celeb["name"])

landmarks = computervision_client.analyze_image_by_domain("landmarks", remote_image_url)

print("\nLandmarks in the remote image:")
for landmark in landmarks.result["landmarks"]:
    print(landmark["name"])
#   END Detect domain-specific content (celebrities/landmarks) in a remote image

#   Detect image types (clip art/line drawing) of a local image by:
#   1. Opening the binary file for reading.
#   2. Calling the Computer Vision service's analyze_image_in_stream with the:
#      - image
#      - features to extract
#   3. Displaying the image type.
local_image = open(local_image_path, "rb")
local_image_features = VisualFeatureTypes.image_type
local_image_analysis = computervision_client.analyze_image_in_stream(local_image, local_image_features)

print("\nImage type of local image:")
if local_image_analysis.image_type.clip_art_type == 0:
    print("Image is not clip art.")
elif local_image_analysis.image_type.line_drawing_type == 1:
    print("Image is ambiguously clip art.")
elif local_image_analysis.image_type.line_drawing_type == 2:
    print("Image is normal clip art.")
else:
    print("Image good clip art.")

if local_image_analysis.image_type.line_drawing_type == 0:
    print("Image is not a line drawing.")
else:
    print("Image is a line drawing")
#   END - Detect image types (clip art/line drawing) of a local image

#   Detect image types (clip art/line drawing) of a remote image by:
#   1. Calling the Computer Vision service's analyze_image with the:
#      - image
#      - features to extract
#   2. Displaying the image type.
remote_image_features = VisualFeatureTypes.image_type
remote_image_analysis = computervision_client.analyze_image(remote_image_url, remote_image_features)

print("\nImage type of remote image:")
if remote_image_analysis.image_type.clip_art_type == 0:
    print("Image is not clip art.")
elif remote_image_analysis.image_type.line_drawing_type == 1:
    print("Image is ambiguously clip art.")
elif remote_image_analysis.image_type.line_drawing_type == 2:
    print("Image is normal clip art.")
else:
    print("Image good clip art.")

if remote_image_analysis.image_type.line_drawing_type == 0:
    print("Image is not a line drawing.")
else:
    print("Image is a line drawing")
#   END - Detect image types (clip art/line drawing) of a remote image

#   Detect objects in a local image by:
#   1. Opening the binary file for reading.
#   2. Calling the Computer Vision service's detect_objects_in_stream with the:
#      - image
#   3. Displaying the location of the objects.
local_image = open(local_image_path, "rb")
local_image_analysis = computervision_client.detect_objects_in_stream(local_image)

print("\nDetecting objects in local image:")
if len(local_image_analysis.objects) == 0:
    print("No objects detected.")
else:
    for object in local_image_analysis.objects:
        print("object at location {}, {}, {}, {}".format( \
        object.rectangle.x, object.rectangle.x + object.rectangle.w, \
        object.rectangle.y, object.rectangle.y + object.rectangle.h))
#   END - Detect objects in a local image

#   Detect objects in a remote image by:
#   1. Opening the binary file for reading.
#   2. Calling the Computer Vision service's detect_objects with the:
#      - image
#      - features to extract
#   3. Displaying the location of the objects.
remote_image_analysis = computervision_client.detect_objects(remote_image_url)

print("\nDetecting objects in remote image:")
if len(remote_image_analysis.objects) == 0:
    print("No objects detected.")
else:
    for object in remote_image_analysis.objects:
        print("object at location {}, {}, {}, {}".format( \
        object.rectangle.x, object.rectangle.x + object.rectangle.w, \
        object.rectangle.y, object.rectangle.y + object.rectangle.h))
#   END - Detect objects in a remote image

#   Detect brands in a local image by:
#   1. Opening the binary file for reading.
#   2. Calling the Computer Vision service's analyze_image_in_stream with the:
#      - image
#      - features to extract
#   3. Displaying brands detected in the image and their locations.
local_image_path = "resources\\gray-shirt-logo.jpg"
local_image = open(local_image_path, "rb")
local_image_features = ["brands"]
local_image_analysis = computervision_client.analyze_image_in_stream(local_image, local_image_features)

print("\nDetecting brands in local image: ")
if len(local_image_analysis.brands) == 0:
    print("No brands detected.")
else:
    for brand in local_image_analysis.brands:
        print("'{}' brand detected with confidence {:.1f}% at location {}, {}, {}, {}".format( \
        brand.name, brand.confidence * 100, brand.rectangle.x, brand.rectangle.x + brand.rectangle.w, \
        brand.rectangle.y, brand.rectangle.y + brand.rectangle.h))
#   END - Detect brands in a local image

#   Detect brands in a remote image by:
#   1. Calling the Computer Vision service's analyze_image_in_stream with the:
#      - image
#      - features to extract
#   3. Displaying brands detected in the image and their locations.
remote_image_url = "https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/images/gray-shirt-logo.jpg"
remote_image_features = ["brands"]
remote_image_analysis = computervision_client.analyze_image(remote_image_url, remote_image_features)

print("\nDetecting brands in remote image: ")
if len(remote_image_analysis.brands) == 0:
    print("No brands detected.")
else:
    for brand in remote_image_analysis.brands:
        print("'{}' brand detected with confidence {:.1f}% at location {}, {}, {}, {}".format( \
        brand.name, brand.confidence * 100, brand.rectangle.x, brand.rectangle.x + brand.rectangle.w, \
        brand.rectangle.y, brand.rectangle.y + brand.rectangle.h))
#   END - Detect brands in a remote image

# Recognize text with the Read API in a local image by:
#   1. Specifying whether the text to recognize is handwritten or printed.
#   2. Calling the Computer Vision service's batch_read_file_in_stream with the:
#      - context
#      - image
#      - text recognition mode
#   3. Extracting the Operation-Location URL value from the batch_read_file_in_stream
#      response
#   4. Waiting for the operation to complete.
#   5. Displaying the results.
local_image_path = "resources\\handwritten_text.jpg"
local_image = open(local_image_path, "rb")
text_recognition_mode = "handwritten"
num_chars_in_operation_id = 36

client_response = computervision_client.batch_read_file_in_stream(local_image, text_recognition_mode, raw=True)
operation_location = client_response.headers["Operation-Location"]
id_location = len(operation_location) - num_chars_in_operation_id
operation_id = operation_location[id_location:]

print("\nRecognizing text in a local image with the batch Read API ... \n")

while True:
    result = computervision_client.get_read_operation_result(operation_id)
    if result.status not in ['NotStarted', 'Running']:
        break
    time.sleep(1)

if result.status == TextOperationStatusCodes.succeeded:
    for text_result in result.recognition_results:
        for line in text_result.lines:
            print(line.text)
            print(line.bounding_box)
            print()
#   END - Recognizing printed and handwritten text with the batch read API in a local image

# Recognize text with the Read API in a remote image by:
#   1. Specifying whether the text to recognize is handwritten or printed.
#   2. Calling the Computer Vision service's batch_read_file_in_stream with the:
#      - context
#      - image
#      - text recognition mode
#   3. Extracting the Operation-Location URL value from the batch_read_file_in_stream
#      response
#   4. Waiting for the operation to complete.
#   5. Displaying the results.
remote_image_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/printed_text.jpg"
text_recognition_mode = "printed"
num_chars_in_operation_id = 36

client_response = computervision_client.batch_read_file(remote_image_url, text_recognition_mode, raw=True)
operation_location = client_response.headers["Operation-Location"]
id_location = len(operation_location) - num_chars_in_operation_id
operation_id = operation_location[id_location:]

print("\nRecognizing text in a remote image with the batch Read API ... \n")

while True:
    result = computervision_client.get_read_operation_result(operation_id)
    if result.status not in ['NotStarted', 'Running']:
        break
    time.sleep(1)

if result.status == TextOperationStatusCodes.succeeded:
    for text_result in result.recognition_results:
        for line in text_result.lines:
            print(line.text)
            print(line.bounding_box)
            print()
#   END - Recognizing printed and handwritten text with the batch read API in a remote image

# Recognize printed text with OCR in a local image by:
local_image_path = "resources\\printed_text.jpg"
#   END - Recognize printed text with OCR in a local image


# Recognize text with OCR in a remote image by:
remote_image_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/printed_text.jpg"

#   END - Recognize printed text with OCR in a remote image
