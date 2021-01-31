from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras import models

import pickle
from scipy.spatial.distance import cosine

model = models.load_model('vgg_feature_extraction_model.h5')
all_images_features = pickle.load(open('vgg16_features.pkl','rb+'))
all_images_names = pickle.load(open('all_images_names.pkl', 'rb+'))


def get_input_image_features(image_path):
  # load an image from file
  input_image = load_img(image_path, target_size=(224, 224))
  # convert the image pixels to a numpy array
  input_image = img_to_array(input_image)
  # reshape data for the model
  input_image = input_image.reshape((1, input_image.shape[0], input_image.shape[1], input_image.shape[2]))
  # prepare the image for the VGG model
  input_image = preprocess_input(input_image)
  # get extracted features
  input_image_features = model.predict(input_image)

  return input_image_features

def calculate_cosine_distance_with_all_DB_images(input_image_features, all_images_features):
  all_cosine_distance = []
  for idx,f in enumerate(all_images_features):
    cos_distance = cosine(input_image_features, f)
    cos_distance = round(cos_distance, 4)
    all_cosine_distance.append([cos_distance, idx])
    all_cosine_distance = sorted(all_cosine_distance)
  return all_cosine_distance

if __name__ == "__main__":
    path = "/content/drive/MyDrive/Sample_Images/Dog10.jpeg"
    input_image_features = get_input_image_features(path)
    all_cosine_distance = calculate_cosine_distance_with_all_DB_images(input_image_features,all_images_features)