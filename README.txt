MEMBER 4 - UPDATED EDA SUBMISSION

Contents:
1. eda_analysis.py - complete EDA source code
2. EDA_Analysis.ipynb - Jupyter Notebook that runs the Python source file
3. Dataset/ - cleaned CSV required to run the project
4. EDA_Output/Charts/ - generated charts (including Advanced_Charts)
5. EDA_Output/Reports/ - generated CSV and business insight reports

HOW TO RUN:
1. Extract the ZIP file.
2. Open the extracted Member4_EDA_Updated folder in VS Code or Jupyter.
3. Install required packages if needed:
   pip install pandas matplotlib seaborn jupyter
4. Run eda_analysis.py in VS Code, OR open EDA_Analysis.ipynb in Jupyter and run all cells.

The script searches for the CSV in the Dataset folder beside the script.
Order_Date is parsed explicitly using DD-MM-YYYY format.
City-wise analysis uses the dataset's Shipping_City column.
2026 is a partial year in the available data; compare yearly totals with this limitation in mind.
