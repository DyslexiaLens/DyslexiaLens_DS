Preparing Dataset
Load Dataset

drive.mount('/content/drive')
zip_path='/content/drive/MyDrive/KebunQ/grape.zip'

Mounted at /content/drive

! unzip "/content/drive/MyDrive/KebunQ/grape.zip" -d .

grape_data = "/content/grape"
grape_classes = os.listdir(grape_data)

print("Grape Classes:")
for classes in grape_classes:
  if os.path.isdir(os.path.join(grape_data, classes)):
    print(classes)
     
Grape Classes:
Leaf Blight
Healthy
Esca (Black Measles)
Black Rot

Preview Image Dataset

for item in grape_classes:
  print("")
  print(item)
  class_dir = os.path.join(grape_data, item)
  class_images = os.listdir(class_dir)

  # Total images in each classes
  num_images = len(class_images)
  print("Total Images:", num_images)

  # Resolution/size of each first image in class
  img_path = os.path.join(class_dir, class_images[0])
  img = mpimg.imread(img_path)
  image_shape = img.shape
  print("Resolution of First Image:", image_shape)

  # Showing some images
  plt.figure(figsize=(10, 5))
  for i, img_path in enumerate(class_images[:5]):
    sp = plt.subplot(1, 5, i+1)
    img = mpimg.imread(os.path.join(class_dir, img_path))
    plt.axis('off')
    plt.imshow(img)
  plt.show()

Preprocessing Dataset
resized_dir = "/content/drive/MyDrive/KebunQ/resized"
os.makedirs(resized_dir, exist_ok=True)

def normalize_image(images):
  normalized_image = images.astype(np.float32) / 255.0
  return normalized_image

for item in grape_classes:
  class_dir = os.path.join(grape_data, item)
  class_image = os.listdir(class_dir)

  for i, img_path in enumerate(class_image):
    img = Image.open(os.path.join(class_dir, img_path))
    resized_img = img.resize((224, 224))
    normalized_img = normalize_image(np.array(resized_img))

    save_path = os.path.join(resized_dir, item, img_path)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    Image.fromarray((normalized_img * 255).astype(np.uint8)).save(save_path)


resized_dir = "/content/drive/MyDrive/KebunQ/resized"
grape_classes = os.listdir(resized_dir)

for grape_class in grape_classes:
  class_dir = os.path.join(resized_dir, grape_class)
  if os.path.isdir(class_dir):
    file_list = os.listdir(class_dir)
    for i, file_name in enumerate(file_list):
      file_path = os.path.join(class_dir, file_name)
      new_file_name = f"{grape_class}_{i+1}.jpg"
      new_file_path = os.path.join(class_dir, new_file_name)
      os.rename(file_path, new_file_path)

datafinal_dir = "/content/drive/MyDrive/KebunQ/datafinal"

num_images_per_class = min(len(os.listdir(resized_dir+"/Esca (Black Measles)")),
                           len(os.listdir(resized_dir+"/Healthy")),
                           len(os.listdir(resized_dir+"/Leaf Blight")),
                           len(os.listdir(resized_dir+"/Black Rot")))

os.makedirs(datafinal_dir+"/Esca (Black Measles)", exist_ok=True)
os.makedirs(datafinal_dir+"/Healthy", exist_ok=True)
os.makedirs(datafinal_dir+"/Leaf Blight", exist_ok=True)
os.makedirs(datafinal_dir+"/Black Rot", exist_ok=True)

selected_images = os.listdir(resized_dir+"/Esca (Black Measles)")[:num_images_per_class]
for image in selected_images:
    shutil.copy(os.path.join(resized_dir+"/Esca (Black Measles)", image), datafinal_dir+"/Esca (Black Measles)")

selected_images = os.listdir(resized_dir+"/Healthy")[:num_images_per_class]
for image in selected_images:
    shutil.copy(os.path.join(resized_dir+"/Healthy", image), datafinal_dir+"/Healthy")

selected_images = os.listdir(resized_dir+"/Leaf Blight")[:num_images_per_class]
for image in selected_images:
    shutil.copy(os.path.join(resized_dir+"/Leaf Blight", image), datafinal_dir+"/Leaf Blight")

selected_images = os.listdir(resized_dir+"/Black Rot")[:num_images_per_class]
for image in selected_images:
    shutil.copy(os.path.join(resized_dir+"/Black Rot", image), datafinal_dir+"/Black Rot")

datafinal_dir = "/content/drive/MyDrive/KebunQ/datafinal"

for item in grape_classes:
  print("")
  print(item)
  class_dir = os.path.join(datafinal_dir, item)
  class_images = os.listdir(class_dir)

  # Total images in each classes
  num_images = len(class_images)
  print("Total Images:", num_images)

  # Resolution/size of each first image in class
  img_path = os.path.join(class_dir, class_images[0])
  img = mpimg.imread(img_path)
  image_shape = img.shape
  print("Resolution of Arfter Resized:", image_shape)

  # Showing some images
  plt.figure(figsize=(10, 5))
  for i, img_path in enumerate(class_images[:5]):
    sp = plt.subplot(1, 5, i+1)
    img = mpimg.imread(os.path.join(class_dir, img_path))
    plt.axis('off')
    plt.imshow(img)
  plt.show()

