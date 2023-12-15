

import streamlit as st
from PIL import Image, ImageFilter
import io
from huggingface_hub import hf_hub_download
from PIL import Image
from transformers import DetrFeatureExtractor
from transformers import TableTransformerForObjectDetection
import matplotlib.pyplot as plt
import torch
# colors for visualization
COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
          [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]

def plot_results(model,pil_img, scores, labels, boxes):
  plt.figure(figsize=(16,10))
  plt.imshow(pil_img)
  ax = plt.gca()
  colors = COLORS * 100
  for score, label, (xmin, ymin, xmax, ymax),c  in zip(scores.tolist(), labels.tolist(), boxes.tolist(), colors):
      ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                 fill=False, color=c, linewidth=3))
      text = f'{model.config.id2label[label]}: {score:0.2f}'
      ax.text(xmin, ymin, text, fontsize=15,
              bbox=dict(facecolor='yellow', alpha=0.5))

  plt.axis('off')
  plt.show()
  img_buffer = io.BytesIO()
  plt.savefig(img_buffer, format="png")
  img_buffer.seek(0)
  img = Image.open(img_buffer)
  plt.close()
  return img

def table_detection(image,encoding,feature_extractor):
  model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-detection")

  with torch.no_grad():
    outputs = model(**encoding)

  width, height = image.size
  #Extracting Table info from Model output
  results = feature_extractor.post_process_object_detection(outputs, threshold=0.7, target_sizes=[(height, width)])[0]

  processed_image= plot_results(model,image, results['scores'], results['labels'], results['boxes'])
  return processed_image

def table_structure_detection(image,encoding,feature_extractor):
  model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-structure-recognition")

  with torch.no_grad():
    outputs = model(**encoding)

  target_sizes = [image.size[::-1]]
  #Extracting Table info from Model output
  results = feature_extractor.post_process_object_detection(outputs, threshold=0.6, target_sizes=target_sizes)[0]

  processed_image= plot_results(model,image, results['scores'], results['labels'], results['boxes'])
  return processed_image

def process_image(uploaded_file):
    #Converting Image Bytes to PIL image
    image_bytes = uploaded_file.read()
    image_pil = Image.open(io.BytesIO(image_bytes))
    image = image_pil.convert("RGB")
    width, height = image.size
    image.resize((int(width*0.5), int(height*0.5)))

    #Extracting features from the image
    feature_extractor = DetrFeatureExtractor()
    encoding = feature_extractor(image, return_tensors="pt")
    encoding.keys()

    processed_image= table_detection(image,encoding,feature_extractor)
    process_image2=table_structure_detection(image,encoding,feature_extractor)
    return [processed_image,process_image2]

def main():
    st.title("Table Detection using Table Transformers")

    # Upload image through Streamlit
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Display the original image
        st.image(uploaded_file, caption="Original Image", use_column_width=True)

        # Process the image
        l1 = process_image(uploaded_file)
        #
        # Display the processed image
        st.image(l1[0], caption="Table Detected Image", use_column_width=True)
        st.image(l1[1], caption="Table Structure Detected Image", use_column_width=True)

if __name__ == "__main__":
    main()
