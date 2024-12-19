import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards


import streamlit as st

wch_colour_box = (0,204,102)
wch_colour_font = (0,0,0)
fontsize = 18
valign = "left"
iconname = "fas fa-asterisk"
sline = "Observations"
lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
i = 123

htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                              {wch_colour_box[1]}, 
                                              {wch_colour_box[2]}, 0.75); 
                        color: rgb({wch_colour_font[0]}, 
                                   {wch_colour_font[1]}, 
                                   {wch_colour_font[2]}, 0.75); 
                        font-size: {fontsize}px; 
                        border-radius: 7px; 
                        padding-left: 12px; 
                        padding-top: 18px; 
                        padding-bottom: 18px; 
                        line-height:25px;'>
                        <i class='{iconname} fa-xs'></i> {i}
                        </style><BR><span style='font-size: 14px; 
                        margin-top: 0;'>{sline}</style></span></p>"""

st.markdown(lnk + htmlstr, unsafe_allow_html=True)
