### Import package
import streamlit as st
import numpy as np
import pandas as pd

### Functions
def position_sizing(risk_per_trade, stop_loss_percent):
  """Position size % = (Risk per trade %) / (stop loss %) * 100 """
  pass

def Stop_loss_percent(entry, sl):
  sl_percent = ((entry-sl)/entry) * 100
  return sl_percent


### MAIN
def main():
    """Main function to run the Streamlit app."""

    st.set_page_config(layout="wide")  # Set wide layout as default

    st.title("Risk Management Analysis")

    # Input section (using columns for better layout)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        capital = st.number_input("Capital (INR)")

    with col2:
        entry_price = st.number_input("Entry Price")

    with col3:
        sl_price = st.number_input("Stop Loss Price")

    with col4:
        quantity = st.number_input("Quantity")

    slp = Stop_loss_percent(entry_price, sl_price)
    # Placeholder for analysis results (to be implemented later)
    st.subheader("Analysis Results")
    st.write("Stop loss in percent", slp)

if __name__ == "__main__":
    main()
