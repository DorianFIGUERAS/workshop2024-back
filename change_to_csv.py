import pandas as pd

def convert_xlsx_to_csv(xlsx_file, csv_file):
    # Read the Excel file
    df = pd.read_excel(xlsx_file)
    
    # Write the DataFrame to a CSV file
    df.to_csv(csv_file, index=False, sep=' ', encoding='utf-8')

if __name__ == "__main__":
    xlsx_file = 'D:/Dorian FIGUERAS/Downloads/data_breastcancer.xlsx'  # Replace with your input file path
    csv_file = 'D:/Dorian FIGUERAS/Downloads/data_breastcancer.csv'   # Replace with your desired output file path
    convert_xlsx_to_csv(xlsx_file, csv_file)