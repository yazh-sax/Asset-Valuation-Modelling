import requests
import json
import time
import matplotlib.pyplot as plt

api_key = "[ENTER ALPHAVANTAGE KEY]" 
master_stock = "[STOCK TICKER]"

# Helper functions to Make & Process API Calls for Commonly Used Data

def get_value(ticker, key, api_function, json_key_0, json_key_1=None):
    request_url = f"https://www.alphavantage.co/query?function={api_function}&symbol={ticker}&apikey={key}"
    r = requests.get(request_url)
    data = r.json()
    if (json_key_1 != None):
        return (data[json_key_0][json_key_1])
    else:
        return (data[json_key_0])

def get_price(ticker, key):
    return float(get_value(ticker, key, "GlOBAL_QUOTE", "Global Quote", "05. price"))

def get_pe_ratio(ticker, key):
    return float(get_value(ticker, key, "OVERVIEW", "PERatio"))

def get_peg_ratio(ticker, key):
    return float(get_value(ticker, key, "OVERVIEW", "PEGRatio"))

def get_dividend(ticker, key):
    return(float(get_value(ticker, key, "OVERVIEW", "DividendPerShare")))

financial_tickers = ["SPGI", "JPM", "V", "MA", "BAC", "WFC", "MS", "GS", "BLK", "AXP"]
financial_ticker_pe = []
financial_ticker_peg = []

index_pe = 23.46
index_eps_growth = 8.69
index_peg = index_pe / index_eps_growth

for ticker in financial_tickers:
    temp_peg = get_peg_ratio(ticker, api_key)
    financial_ticker_peg.append(temp_peg)
    print(f"{ticker}: successful, PEG: {temp_peg}")
    # Prevent API Blocking
    time.sleep(8)
financial_avg_peg = sum(financial_ticker_peg) / len (financial_ticker_peg)

for ticker in financial_tickers:
    temp_pe = get_pe_ratio(ticker, api_key)
    financial_ticker_pe.append(temp_pe)
    print(f"{ticker}: successful, PE: {temp_pe}")
    # Prevent API Blocking
    time.sleep(8)
financial_avg_pe = sum(financial_ticker_pe) / len (financial_ticker_pe)

print(f"Financial ticker PE Ratios: {financial_ticker_pe}")
print(f"Financial ticker PEG Ratios: {financial_ticker_peg}")

# Manually setting financial ticker PEG ratios
financial_ticker_peg = [2.47, 1.92, 1.82, 1.86, 1.22, 0.87, 2.44, 1.35, 1.98, 1.02]
financial_avg_peg = sum(financial_ticker_peg) / len (financial_ticker_peg)

# Display Results
print(f"Financial Sector PE: {round(financial_avg_pe, 3)}")
print(f"Index Average PE: {round(index_pe, 3)}")

print(f"Financial Sector PEG: {round(financial_avg_peg, 3)}")
print(f"Index Average PEG: {round(index_peg, 3)}")

# Note: Financial sector PE/PEG stored from earlier calculations
ms_pe = get_pe_ratio(master_stock, api_key)
ms_peg = 2.44

# Display Results
print(f"Financial Sector PE: {round(financial_avg_pe, 2)}")
print(f"Morgan Stanley Average PE: {ms_pe}")

print(f"Financial Sector PEG: {round(financial_avg_peg, 2)}")
print(f"Morgan Stanley Average PEG: {ms_peg}")

# Calculating g, r & div
g = 0.04
div = 3.4 * (g + 1)

# Calculating r/capital equity cost (in millions of dollars)
E = 147586
D = 244692
cost_of_equity = 0.1184
cost_of_debt = 12268 / D
tax_rate = 0.21

r = (E / (E + D) * cost_of_equity) + (D / (E + D) * cost_of_debt * (1 - tax_rate))

# Calculating DDM
ddm_estimate = div / (r - g)

print(f"The DDM model Prices Morgan Stanley stock at: {round(ddm_estimate, 2)}")

# Styling
plt.style.use('seaborn-v0_8-dark')
plt.figure(figsize=(8,8))
plt.axis([0, 70, 0, 3.5])

# Plot Financial Stock (PE, PEG) in black
plt.plot(financial_ticker_pe, financial_ticker_peg, 'o', color = 'black', label = 'Financial Stocks')

# Plot Morgan Stanley (PE, PEG) in green
plt.plot(ms_pe, ms_peg, 'o', color = 'green', label = "Morgan Stanley")

# Plot S&P500 Index PE vertical line and PEG horizontal line
plt.axvline(x = index_pe, color = 'red', label = 'S&P 500 PE Ratio')
plt.axhline(y = index_peg, color = 'red', label = 'S&P 500 PEG Ratio')

# Title and Axis Labels
plt.title("Morgan Stanley vs Financial Sector vs S&P500 PE/PEG Ratios")
plt.xlabel("PE Ratio")
plt.ylabel("PEG Ratio")

# Create Legend
plt.legend(loc="lower right")

# Display Graph
plt.show
