

## Step 1.

To get started, one might like to collect the indices (or tickers, symbols) of interest, the indices that will be the basis of the analysis.
- Navigate to `.config/exchanges.py` and decide what exchanges or indices to focus on (also, see Note below)
- Run the script `.src/data_acquisition/get_symbols.py` with the desired option included (which can be checked by running with the --help argument)


Note:
    If the index of interest is not present, create a new Exchange instance and 
    fill in the details (perhaps there is a wiki url from which to dowload the relevant data, etc.)

