### Import package
import streamlit as st
import numpy as np
import pandas as pd

### Functions
def position_sizing(risk_per_trade, stop_loss_percent):
  """Position size % = (Risk per trade %) / (stop loss %) * 100 """
  position_size_percent = (risk_per_trade/slp) * 100
  position_size_capital = capital/position_size_percent
  position_size_quantity = position_size_capital/entry_price
  return position_size_percent, position_size_capital, position_size_quantity

def Stop_loss_percent(entry, sl):
  try:
    sl_percent = ((entry-sl)/entry) * 100
  except as e:
    print('Recheck', e)
    pass
  return sl_percent


### MAIN
def main():
    """Main function to run the Streamlit app."""

    st.set_page_config(layout="wide")  # Set wide layout as default

    st.title("PT - RM_sys")

    # Input section (using columns for better layout)

    capital = st.number_input('Capital in INR')
    col1, col2, col3, col4 = st.columns(4)

    with col1:
      entry_price = st.number_input("Entry Price")
      
    with col2:
      sl_price = st.number_input("Stop Loss Price") 

    with col3:
      rpt = st.number_input("Risk per Trade (%)")

    with col4:
      quantity = st.number_input("Quantity")

    # calculation:
    slp = Stop_loss_percent(entry_price, sl_price)
    psp,psc,psq = position_sizing(rpt, slp)
    
    # Placeholder for analysis results (to be implemented later)
    st.subheader("Analysis Results")
    col1,col2 = st.columns(2)

    with col1:
      st.write("Stop loss in Percent", slp)

    with col2:
      st.write(f"Position Size in Percent: {psp}\nPostion size in Capital: {psc}\nPosition size in Quantity: {psq}"

if __name__ == "__main__":
    main()
