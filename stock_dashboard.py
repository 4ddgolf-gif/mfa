import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Streamlit app title
st.title('Stock Dashboard')

# User input for stock symbols
stocks_input = st.text_input('Enter stock symbols separated by commas (e.g., AAPL, GOOGL, MSFT)')

# Button to refresh data
if st.button('Refresh Data'):
    pass  # This forces a rerun when clicked, updating the data

if stocks_input:
    stock_list = [s.strip().upper() for s in stocks_input.split(',')]
    
    for stock in stock_list:
        try:
            ticker = yf.Ticker(stock)
            info = ticker.info
            
            # Display stock header
            st.subheader(stock)
            
            # Columns for metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                current_price = info.get('currentPrice', 'N/A')
                st.metric('Current Price', f"${current_price:.2f}" if current_price != 'N/A' else 'N/A')
            
            with col2:
                day_low = info.get('dayLow', 'N/A')
                day_high = info.get('dayHigh', 'N/A')
                day_range = f"{day_low:.2f} - {day_high:.2f}" if day_low != 'N/A' and day_high != 'N/A' else 'N/A'
                st.metric("Day's Range", day_range)
            
            with col3:
                week_low = info.get('fiftyTwoWeekLow', 'N/A')
                week_high = info.get('fiftyTwoWeekHigh', 'N/A')
                week_range = f"{week_low:.2f} - {week_high:.2f}" if week_low != 'N/A' and week_high != 'N/A' else 'N/A'
                st.metric('52-Week Range', week_range)
            
            # Fetch historical data for chart (1 year)
            hist = ticker.history(period='1y')
            if not hist.empty:
                fig = go.Figure(data=[go.Candlestick(x=hist.index,
                                                    open=hist['Open'],
                                                    high=hist['High'],
                                                    low=hist['Low'],
                                                    close=hist['Close'],
                                                    name=stock)])
                fig.update_layout(title=f'{stock} 1-Year Candlestick Chart',
                                  xaxis_title='Date',
                                  yaxis_title='Price',
                                  xaxis_rangeslider_visible=True)
                st.plotly_chart(fig)
            else:
                st.write('No historical data available for chart.')
        
        except Exception as e:
            st.error(f"Error fetching data for {stock}: {str(e)}")
else:
    st.write('Please enter stock symbols to view the dashboard.')
