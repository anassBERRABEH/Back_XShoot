from ultralytics import YOLO
import cv2
import easyocr
import os
import json

model_detect_path = './best.pt'
model_detect = YOLO(model_detect_path)


def one_image(image):   # bibs
    output = []

    # bibs prediction
    bibs = []
    res = model_detect.predict(image)
    for box in res[0].boxes:
        bibs.append(box.xyxy)

    # num identification
    image = cv2.imread(image)
    reader = easyocr.Reader(['en'])
    for bib in bibs:
        x1, y1, x2, y2 = [int(i) for i in bib.numpy().tolist()[0]]
        results = reader.readtext(image[y1:y2, x1:x2])
        for (bbox, text, prob) in results:
            # print(f"Detected text: {text} (Probability: {prob})")
            for i in results:
                try:
                    output.append(int(i[1]))
                except:
                    pass
    return output


def save_to_json(data, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def process_folder(folder_path):
    all_bibs = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            image_path = os.path.join(folder_path, filename)
            bib_numbers = one_image(image_path)
            print(bib_numbers, "****************************")
            for bib_number in bib_numbers:
                if bib_number not in all_bibs:
                    all_bibs[bib_number] = set()
                all_bibs[bib_number].add(image_path)

    print(all_bibs)
    for k, v in all_bibs.items():
        all_bibs[k] = list(v)
    output_file = folder_path + '/bib_images.json'
    save_to_json(all_bibs, output_file)
