import requests
import json
import time
import matplotlib.pyplot as plt

## USER INPUTS BELOW ##
api_key = "[ENTER ALPHAVANTAGE KEY]" 
master_stock = "[STOCK TICKER]"
# Populate with tickers for comparative analysis
comparison_tickers = [""]
# Populate with PEG ratios (decimal) for comparison tickers
comparison_ticker_peg = []
# PE Ratio of Index (S&P500 used as example)
index_pe = 23.46
# EPS Growth of Index
index_eps_growth = 8.69
# Expected dividend growth rate (expressed as decimal: 5% -> 0.05)
g = 0.00
# Current annual dividend (expressed as percent)
current_dividend = 0.0
# Market Cap (In Dollars)
E = 0
# Debt Value (In Dollars)
D = 0
# Cost of Equity (expressed as decimal: 5% -> 0.05)
cost_of_equity = 0.00
# Interest Expense (annually, In Dollars)
interest_expense = 0
# US Corporate Tax Rate (expressed as decimal: 5% -> 0.05), 21% in 2023
tax_rate = 0.21

#####################################################################
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

comparison_ticker_pe = []
comparison_ticker_peg = []


index_peg = index_pe / index_eps_growth

for ticker in comparison_tickers:
    temp_peg = get_peg_ratio(ticker, api_key)
    comparison_ticker_peg.append(temp_peg)
    print(f"{ticker}: successful, PEG: {temp_peg}")
    # Prevent API Blocking
    time.sleep(8)
comparative_avg_peg = sum(comparison_ticker_peg) / len (comparison_ticker_peg)

for ticker in comparison_tickers:
    temp_pe = get_pe_ratio(ticker, api_key)
    comparison_ticker_pe.append(temp_pe)
    print(f"{ticker}: successful, PE: {temp_pe}")
    # Prevent API Blocking
    time.sleep(8)
comparative_avg_pe = sum(comparison_ticker_pe) / len (comparison_ticker_pe)

print(f"Comparative ticker PE Ratios: {comparison_ticker_pe}")
print(f"Comparative ticker PEG Ratios: {comparison_ticker_peg}")

# Manually setting comparative ticker PEG ratios
comparative_avg_peg = sum(comparison_ticker_peg) / len (comparison_ticker_peg)

# Display Results
print(f"Comparative Sector PE: {round(comparative_avg_pe, 3)}")
print(f"Index Average PE: {round(index_pe, 3)}")

print(f"Comparative Sector PEG: {round(comparative_avg_peg, 3)}")
print(f"Index Average PEG: {round(index_peg, 3)}")

# Note: comparative sector PE/PEG stored from earlier calculations
ms_pe = get_pe_ratio(master_stock, api_key)
ms_peg = 2.44

# Display Results
print(f"Comparative Sector PE: {round(comparative_avg_pe, 2)}")
print(f"Morgan Stanley Average PE: {ms_pe}")

print(f"Comparative Sector PEG: {round(comparative_avg_peg, 2)}")
print(f"Morgan Stanley Average PEG: {ms_peg}")


cost_of_debt = interest_expense / D
r = (E / (E + D) * cost_of_equity) + (D / (E + D) * cost_of_debt * (1 - tax_rate))

# Calculating DDM
div = current_dividend * (g + 1)
ddm_estimate = div / (r - g)

print(f"The DDM model Prices {master_stock} stock at: {round(ddm_estimate, 2)}")

# Styling
plt.style.use('seaborn-v0_8-dark')
plt.figure(figsize=(8,8))
plt.axis([0, 70, 0, 3.5])

# Plot comparative Stock (PE, PEG) in black
plt.plot(comparison_ticker_pe, comparison_ticker_peg, 'o', color = 'black', label = 'Comparative Stocks')

# Plot Master Stock (PE, PEG) in green
plt.plot(ms_pe, ms_peg, 'o', color = 'green', label = "Master Stock")

# Plot S&P500 Index PE vertical line and PEG horizontal line
plt.axvline(x = index_pe, color = 'red', label = 'S&P 500 PE Ratio')
plt.axhline(y = index_peg, color = 'red', label = 'S&P 500 PEG Ratio')

# Title and Axis Labels
plt.title("Master Stock vs Comparative Sector vs S&P500 PE/PEG Ratios")
plt.xlabel("PE Ratio")
plt.ylabel("PEG Ratio")

# Create Legend
plt.legend(loc="lower right")

# Display Graph
plt.show
