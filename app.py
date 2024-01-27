import streamlit as st
view = [100,150,40]
st.write(' # You view')
st.bar_chart(view)

import pandas as pd  
sview = pd.Series(view)
sview
