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

def calculate_rr_ratio(entry_price, stop_loss_price, target_price):
    """Calculates the Risk:Reward (R:R) ratio."""
    if entry_price is None or stop_loss_price is None or target_price is None:
        return None  # Return None if any input is missing

    risk = abs(entry_price - stop_loss_price)
    reward = abs(target_price - entry_price)

    if risk == 0:
        return float('inf') if reward > 0 else 0 # handle risk = 0

    rr_ratio = reward / risk
    return rr_ratio

### MAIN
def main():
    """Main function to run the Streamlit app."""

    st.set_page_config(layout="wide")  # Set wide layout as default

    st.title("PT - RM_sys - CC")

    # Input section (using columns for better layout)
    capital = st.number_input('Capital in INR', min_value=0.0, value=10000.0, step=100.00)
    col1, col2, col3 = st.columns(3)

    with col1:
        entry_price = st.number_input("Entry Price", min_value=0.0, value=100.0, step=0.05)

    with col2:
        sl_price = st.number_input("Stop Loss Price", min_value=0.0, value=95.0, step=0.05)

    with col3:
        tgt_est = st.number_input("Estimated target", min_value=0.0, value=200.0, step=0.5)
        
    rpt = st.slider("Risk per Trade (%)", min_value=0.0, max_value=30.0, value=1.0, step=0.05)

    # calculation:
    slp = stop_loss_percent(entry_price, sl_price)

    if slp is not None: # only calculate position size if stop loss percent is a valid number.
        try:
            psp, psc, psq = position_sizing(rpt, slp, capital, entry_price)
            rr_ratio = calculate_rr_ratio(entry_price, sl_price, tgt_est)
            lot_size = st.number_input("Lot Size in Quantity", min_value=0, value=75, step=5)
            no_of_lots = st.number_input("Number of Lots", min_value=1, value=1, step=1)
            total_size = lot_size * no_of_lots 
            buy_size = total_size * entry_price 
            
            # Placeholder for analysis results (to be implemented later)
            col1, col2 = st.columns(2)
    
            with col1:
                st.subheader("Optimal Position Sizing", divider='red')
                st.write(f"Stop loss in Percent: {slp:.2f}%")
                st.write(f"Position Size in Percent: {psp:.2f}%")
                st.write(f"Position Size in Capital: {psc:.2f}")
                st.write(f"Position Size in Quantity: {psq:.2f}")
    
            with col2:
                st.subheader("Per trade analysis", divider='red')
                scol1, scol2 = st.columns(2)
                with scol1:
                    st.write(f"Total Quantity: {total_size}")
                    st.write(f"Total buy size: {buy_size}")
                    st.write(f"Total SL: {buy_size - (total_size * sl_price)}")
                with scol2:
                    st.write(f"Profit range: {(tgt_est * total_size) - (buy_size)}")
                    st.write(f"R:R ratio: {rr_ratio:.2f}")
            
            # Create DataFrame
            data = {
                "Entry Price": [entry_price],
                "Stop Loss Price": [sl_price],
                "Target Price": [tgt_est],
                "Lot Size": [lot_size],
                "Total Size": [total_size],
                "Buy Size": [buy_size],
                "Stop Loss Amount": [buy_size - (total_size * sl_price)],
                "Profit Range": [(tgt_est * total_size) - (buy_size)],
                "R:R Ratio": [rr_ratio]
                }
            df = pd.DataFrame(data)
            st.bar_chart(df, x=['Buy Size', 'Profit Range', 'R:R Ratio'], stack=False, horizontal=True)
        except:
            pass
    else:
        st.write("Please check entry price and stop loss price.")

    

if __name__ == "__main__":
    main()
