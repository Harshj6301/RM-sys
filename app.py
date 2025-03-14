import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

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

def calculate_roi(initial_investment, final_value):
    """
    Calculates the Return on Investment (ROI).

    Args:
        initial_investment: The initial amount of money invested.
        final_value: The final value of the investment.

    Returns:
        The ROI as a percentage. Returns None if initial_investment is 0.
    """
    if initial_investment == 0:
        return None  # Avoid division by zero
    roi = ((final_value - initial_investment) / initial_investment) * 100
    return roi
    
### MAIN
def main():
    """Main function to run the Streamlit app."""

    st.set_page_config(layout="wide")  # Set wide layout as default

    st.title("PT - RM_sys - CC")

    # Input section (using columns for better layout)
    capital = st.number_input('**Capital in INR**', min_value=0.0, value=10000.0, step=100.00)
    col1, col2, col3 = st.columns(3)

    with col1:
        entry_price = st.number_input("**Entry Price**", min_value=0.0, value=100.0, step=0.5)

    with col2:
        sl_price = st.number_input("**Stop Loss Price**", min_value=0.0, value=95.0, step=0.5)

    with col3:
        tgt_est = st.number_input("**Estimated target**", min_value=0.0, value=200.0, step=0.5)
        
    rpt = st.slider("**Risk per Trade (%)**", min_value=0.0, max_value=30.0, value=1.0, step=0.05)

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
            total_sl = (buy_size - (total_size * sl_price))
            profit_range = ((tgt_est * total_size) - (buy_size))
            # Placeholder for analysis results (to be implemented later)
            col1, col2 = st.columns(2)
    
            with col1:
                st.subheader("Optimal Position Sizing", divider='red')
                if slp >= 7.0:
                    st.markdown(f"Stop loss in Percent: :red[**{slp:.2f}%**]")
                elif slp >= 3.0:
                    st.markdown(f"Stop loss in Percent: :orange[**{slp:.2f}%**]")
                else:
                    st.markdown(f"Stop loss in Percent: :green[**{slp:.2f}%**]")
                st.markdown(f"Position Size in Percent: :orange[**{psp:.2f}%**]")
                st.markdown(f"Position Size in Capital: :green[**{psc:.2f}**]")
                st.markdown(f"Position Size in Quantity: :orange[**{psq:.2f}**]")
    
            with col2:
                st.subheader("Per trade analysis", divider='red')
                scol1, scol2 = st.columns(2)
                with scol1:
                    st.markdown(f"Total Quantity: :orange[**{total_size}**]")
                    st.markdown(f"Total buy size: :green[**{buy_size}**]")
                    st.markdown(f"Total SL: :red[**{total_sl:.2f}**]")
                with scol2:
                    st.markdown(f"Profit range: :green[**{profit_range}**]")
                    if rr_ratio <= 3.00:
                        st.markdown(f"R:R ratio: :red[**{rr_ratio:.2f}**]")
                    else:
                        st.markdown(f"R:R ratio: :green[**{rr_ratio:.2f}**]")
                    st.markdown(f"ROI: :green[**{calculate_roi(buy_size, (tgt_est * total_size)):.2f}%**]")
            
            # Create DataFrame
            data = {
                "Entry Price": [entry_price],
                "Stop Loss Price": [sl_price],
                "Target Price": [tgt_est],
                "Lot Size": [lot_size],
                "Number of Lots": [no_of_lots],
                "Total Size": [total_size],
                "Buy Size": [buy_size],
                "Stop Loss Amount": [total_sl],
                "Profit Range": [profit_range],
                "R:R Ratio": [rr_ratio]
                }
            df = pd.DataFrame(data)
            st.subheader('Graphs', divider='red')
            
            col1, col2 = st.columns(2)
            with col1:
                labels = ['Buy Size', 'Stop Loss Amount', 'Profit Range']
                values = [buy_size, total_sl, profit_range]

                fig_pie = px.pie(values=values, names=labels, title='Trade Composition',color_discrete_sequence=['darkorange','orange', 'yellow'])
                st.plotly_chart(fig_pie, theme="streamlit", use_container_width=True)
            with col2:
               # st.bar_chart(df[['Entry Price', 'Stop Loss Price', 'Target Price']], x_label='Trade levels', stack=False, horizontal=True)
                fig_bar = px.bar(df, x=tgt_est+100.0, y=['Entry Price', 'Stop Loss Price', 'Target Price'], title='Trade Levels', color_discrete_sequence=px.colors.sequential.Oranges, orientation='h')
                st.plotly_chart(fig_bar, theme='streamlit', use_container_width=True)

        
        except:
            pass
    else:
        st.write("Please check entry price and stop loss price.")

    

if __name__ == "__main__":
    main()
