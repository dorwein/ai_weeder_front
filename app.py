import streamlit as st
from PIL import Image
import numpy as np
import requests


# Dictionaries
plant_info = {
    'Black-grass': 'Black-Grass (Alopecurus myosuroides) is a notorious weed, especially problematic in cereal crops like wheat and barley.' ,
    'Charlock':'Charlock (Sinapis arvensis), also known as wild mustard, is considered a weed, often found in crop fields.',
    "Cleavers":'Cleavers (Galium aparine), also known as stickyweed, is a common weed that clings to other plants and crops.',
    "Common Chickweed":'Common Chickweed (Stellaria media) is a widespread weed that thrives in disturbed soils, gardens, and cities.',
    "Common wheat":'Common wheat (Triticum aestivum) is a major cereal crop, the base of many delicious baked goods.',
    "Fat Hen":'Fat Hen (Chenopodium album) is an annual weed, common in farmlands, gardens, and disturbed soils, known for competing with crops.',
    "Loose Silky-bent":'Loose Silky-bent (Apera spica-venti) is considered a weed, especially in grain crops where it can affect yields.',
    "Maize":'Maize (Zea mays), or better known as corn, is a cultivated crop and irreplaceable for popcorn.',
    "Scentless Mayweed":'Scentless Mayweed (Tripleurospermum inodorum) is a common agricultural weed that competes with crops for nutrients and space.',
    "Shepherds Purse":'Shepherds Purse (Capsella bursa-pastoris) is a common weed, particularly found in cultivated soils and gardens.',
    "Small-flowered Cranesbill":'Small-flowered Cranesbill (Geranium pusillum) is a weed that can be invasive, often found in disturbed soils and gardens.',
    "Sugar beet":'Sugar beet (Beta vulgaris) is an important root crop, cultivated for sugar production and responsible for about 20% of the worlds sugar production'
}

weeds_dict = {'Black-grass': 'weed' ,
 'Charlock':'weed',
 "Cleavers":'weed',
 "Common Chickweed":'weed',
 "Common wheat":'not weed',
 "Fat Hen":'weed',
 "Loose Silky-bent":'weed',
 "Maize":'not weed',
 "Scentless Mayweed":'weed',
 "Shepherds Purse":'weed',
 "Small-flowered Cranesbill":'weed',
 "Sugar beet":'not weed' }




# Center-aligned style for headers and titles
header_style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bungee&display=swap');
h1 {
    font-size: 100px;
    font-family: 'Bungee', sans-serif;
}
.centered-header {
    text-align: center;
}
.centered-header-green {
    text-align: center;
    color: #5ba334;
}
.centered-header-orange {
    text-align: center;
    color: #bf4824;
}
.stButton>button {
    width: 100%;
    font-size: 20px;
    background-color: #5ba334;
    color: white;
}
.stButton>button:hover {
    background-color: white;
    color: #5ba334;
    border: 2px solid #5ba334;
}
</style>
"""



st.markdown(header_style, unsafe_allow_html=True)

# Title of the app (centered)
st.markdown('<h1 class="centered-header-green">AI Weeder</h1>', unsafe_allow_html=True)

st.markdown('''
This model is designed for implementation on an agricultural robot to accurately identify and remove
weeds. This user interface allows you to interact with the model by uploading an image of a plants seedling
and getting a prediction of the seedling's type using a pre-trained model via an API.
''')
st.markdown('''
The model was trained on the following common crops and weeds species in Danish agriculture: Black-grass, Charlock,
Cleavers, Common Chickweed, Fat Hen, Loose Silky-bent, Scentless Mayweed, Sheperd‘s Purse, Small-flowered Cranesbill Common wheat, Maize, Sugar beet
''')

st.markdown('<h5 class="centered-header">Select a seedling image...</h5>', unsafe_allow_html=True)
# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# State variable to control the visibility of the camera input
if 'show_camera' not in st.session_state:
    st.session_state.show_camera = False

# Button to toggle camera input
if st.button('Use Camera'):
    st.session_state.show_camera = True

# Display camera input only when the button is pressed
camera_photo = st.camera_input("Take a photo...") if st.session_state.show_camera else None
if st.button('↑ Hide ↑') if st.session_state.show_camera else None:
    st.session_state.show_camera = False

if uploaded_file is not None or camera_photo is not None:
    # Determine which image to use
    if uploaded_file is not None:
        image = uploaded_file
        image_caption = "Uploaded Image"
    else:
        image = camera_photo
        image_caption = "Captured Image"

    # Display the selected image
    st.image(image, caption=image_caption, use_column_width=True)
    st.write("")

    if st.markdown('<div style="text-align: center;">', unsafe_allow_html=True):
        if st.button('Predict'):
            img_bytes = image.read() if uploaded_file else camera_photo.getvalue()

            # Make API request
            api_url = 'https://aiweeder-1080691208206.europe-west1.run.app/upload_image'
            # Send the image to the API
            response = requests.post(api_url, files={'img': img_bytes})

            if response.status_code == 200:
                result = response.json()

                predicted_classes = result.get('types')
                probabilities = result.get('probabilities')
                predicted_types = result.get('weed_or_not')
                weed_prediction = result.get('weed_prediction')

                if weed_prediction.get('type') == 'crop':
                    seedling_type = weed_prediction.get('type').capitalize() + '🌱'
                    st.markdown(
                        """
                        <div style='text-align: center;'>
                        <h4 class='centered-header' style='display: inline;'>This seedling is a: </h4>
                        <h1 class='centered-header-green' style='display: inline;'>{}</h1>
                        </div>
                        """.format(seedling_type),
                        unsafe_allow_html=True
                    )

                    st.markdown(f"<h4 class='centered-header'>(Probability: {(weed_prediction.get('probability'))*100:.0f}%)</h4><br>", unsafe_allow_html=True)

                    st.markdown(
                        """
                        <div style='text-align: center;'>
                        <h5 class='centered-header' style='display: inline;'>Of type: </h5>
                        <h4 class='centered-header-green' style='display: inline;'>{}</h4>
                        </div>
                        """.format(predicted_classes.get('first_feature').capitalize()),
                        unsafe_allow_html=True
                    )
                    st.markdown(f"<h5 class='centered-header'>(Probability: {probabilities.get('first_feature')*100:.0f}%)</h5>", unsafe_allow_html=True)
                else:
                    seedling_type = weed_prediction.get('type').capitalize() + '🚫'
                    st.markdown(
                        """
                        <div style='text-align: center;'>
                        <h4 class='centered-header' style='display: inline;'>This seedling is a: </h4>
                        <h1 class='centered-header-orange' style='display: inline;'>{}</h1>
                        </div>
                        """.format(seedling_type),
                        unsafe_allow_html=True
                    )

                    st.markdown(f"<h5 class='centered-header'>(Probability: {weed_prediction.get('probability')*100:.0f}%)</h5><br>", unsafe_allow_html=True)

                    st.markdown(
                        """
                        <div style='text-align: center;'>
                        <h5 class='centered-header' style='display: inline;'>Of type: </h5>
                        <h4 class='centered-header-orange' style='display: inline;'>{}</h4>
                        </div>
                        """.format(predicted_classes.get('first_feature').capitalize()),
                        unsafe_allow_html=True
                    )
                    st.markdown(f"<h6 class='centered-header'>(Probability: {probabilities.get('first_feature')*100:.0f}%)</h6>", unsafe_allow_html=True)

                st.markdown(f"<h6 class='centered-header'>{plant_info.get(predicted_classes.get('first_feature'))}</h6>", unsafe_allow_html=True)

            else:
                st.write("Error: Unable to get a prediction from the API.")
