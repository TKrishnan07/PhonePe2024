import streamlit as st
from streamlit_option_menu import option_menu

# CSS for custom styling
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://cdn.dribbble.com/users/1902890/screenshots/15619502/media/4110e14facc720955ac1ad0ae1589477.gif");
        background-position: center;
        background-size: cover;
    }

    .title {
        color: #FFFFFF;
        font-size: 36px;
        font-weight: bold;
    }

    /* Sidebar hover effects */
    .css-1d391kg a:hover {
        background-color: #5A189A !important;  /* Darker purple on hover */
        color: #FFD700 !important;  /* Gold text on hover */
    }

    /* Hover effect for the title */
    .title:hover {
        color: #FFD700;  /* Change to gold color on hover */
    }

    /* Tab headers color */
    .stTabs [data-baseweb="tab"] {
        color: #FFFFFF !important;  /* Set tab text color to white */
    }

    /* Radio button labels and selected option color */
    .stRadio label {
        color: #FFFFFF !important;  /* Set radio button labels to white */
    }
    .stRadio div[role='radiogroup'] > label {
        color: #FFFFFF !important;  /* Ensure all radio button labels are white */
    }
    .stRadio div[role='radiogroup'] > label div[aria-checked="true"] > div:first-child {
        background-color: #FFFFFF !important;  /* Set the radio button selection dot to white */
    }
    .stRadio div[role='radiogroup'] > label div[aria-checked="true"] > div:first-child:hover {
        background-color: #FFFFFF !important;  /* Maintain white color on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the title with hover effect
st.markdown('<h1 class="title">PhonePe Data Visualization and Exploration</h1>', unsafe_allow_html=True)

# Sidebar with option menu
with st.sidebar:
    select = option_menu("Main Menu", ["Home", "Data Exploration", "Top Charts"])

if select == "Home":
    pass

elif select == "Data Exploration":
    Tab1, Tab2, Tab3 = st.tabs(["Aggregated Data", "Map Data", "Top Data"])

    with Tab1:
        Data_Analysis1 = st.radio("Select one Aggregated Data", ["Aggregated Insurance Data", "Aggregated Transaction Data", "Aggregated User Data"])

        if Data_Analysis1 == "Aggregated Insurance Data":
            pass
        elif Data_Analysis1 == "Aggregated Transaction Data":
            pass
        elif Data_Analysis1 == "Aggregated User Data":
            pass

    with Tab2:
        Data_Analysis2 = st.radio("Select one Map Data", ["Map Insurance Data", "Map Transaction Data", "Map User Data"])

        if Data_Analysis2 == "Map Insurance Data":
            pass
        elif Data_Analysis2 == "Map Transaction Data":
            pass
        elif Data_Analysis2 == "Map User Data":
            pass

    with Tab3:
        Data_Analysis3 = st.radio("Select one Top Data", ["Top Insurance Data", "Top Transaction Data", "Top User Data"])

        if Data_Analysis3 == "Top Insurance Data":
            pass
        elif Data_Analysis3 == "Top Transaction Data":
            pass
        elif Data_Analysis3 == "Top User Data":
            pass

