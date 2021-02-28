import streamlit as st
import io
import requests
from PIL import Image
from PIL import ImageDraw


st.title('へたれの顔認証')

subscription_key = 'ebc501a7a3664e5a8e146c5cdadf3371'
assert subscription_key

face_api_url = 'https://20210228hetare.cognitiveservices.azure.com/face/v1.0/detect'

uploaded_file = st.file_uploader("Chuse an image...", type='jpg')
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue() #バイナリ取得
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes': 'age,gender,headpose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }
    res = requests.post(face_api_url, params=params, headers=headers, data=binary_img)

    results = res.json()
    for result in results:
        rect = result['faceRectangle']
        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'], rect['top']), (rect['left']+rect['width'],
                                         rect['top']+rect['height'])], fill=None, outline='green', width=5)
                    
    st.image(img, caption='uploded Image.', use_column_width=True)
