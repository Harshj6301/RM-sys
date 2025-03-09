import streamlit as st
import numpy as np
import pandas as pd

### Functions
def position_sizing(risk_per_trade, stop_loss_percent, capital, entry_price):
    """Position size % = (Risk per trade %) / (stop loss %) * 100 """
    if stop_loss_percent == 0:
        return 0, 0, 0  # Handle division by zero
    position_size_percent = (risk_per_trade / stop_loss_percent) * 100
    position_size_capital = (capital * risk_per_trade / 100) / (stop_loss_percent / 100) if stop_loss_percent != 0 else 0
    position_size_quantity = position_size_capital / entry_price if entry_price != 0 else 0
    return position_size_percent, position_size_capital, position_size_quantity

def stop_loss_percent(entry, sl):
    try:
        if entry == 0:
            return 0  # Handle division by zero
        sl_percent = ((entry - sl) / entry) * 100
        return sl_percent
    except:
        return None  # Return None in case of errors

### MAIN
def main():
    """Main function to run the Streamlit app."""

    st.set_page_config(layout="wide")  # Set wide layout as default

    st.title("PT - RM_sys - CC")

    # Input section (using columns for better layout)
    capital = st.number_input('Capital in INR', min_value=0.0, value=10000.0)
    col1, col2, col3 = st.columns(3)

    with col1:
        entry_price = st.number_input("Entry Price", min_value=0.0, value=100.0, step=0.05)

    with col2:
        sl_price = st.number_input("Stop Loss Price", min_value=0.0, value=95.0, step=0.05)

    with col3:
        rpt = st.number_input("Risk per Trade (%)", min_value=0.0, value=1.0, step=0.05)

    # calculation:
    slp = stop_loss_percent(entry_price, sl_price)

    if slp is not None: # only calculate position size if stop loss percent is a valid number.
        psp, psc, psq = position_sizing(rpt, slp, capital, entry_price)

        # Placeholder for analysis results (to be implemented later)
        st.subheader("Analysis Results")
        st.divider()
        st.write(f"Stop loss in Percent: {slp:.2f}%")
        st.write(f"Position Size in Percent: {psp:.2f}%")
        st.write(f"Position Size in Capital: {psc:.2f}")
        st.write(f"Position Size in Quantity: {psq:.2f}")
        st.divider()
    else:
        st.write("Please check entry price and stop loss price.")

if __name__ == "__main__":
    main()
