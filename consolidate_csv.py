import pandas as pd
from pathlib import Path
import re


def consolidate_csv_by_year(folder_path):
    # Create a Path object for the folder
    folder = Path(folder_path)

    # Dictionary to hold filenames grouped by year
    files_by_year = {}

    # Regular expression to extract the year from filenames
    year_regex = re.compile(r'^(\d{4})-\d{2}-\d{2}\.csv$')

    # Group files by year
    for file in folder.glob('*.csv'):
        match = year_regex.match(file.name)
        if match:
            year = match.group(1)
            if year not in files_by_year:
                files_by_year[year] = []
            files_by_year[year].append(file)

    # For each year, consolidate files
    for year, files in files_by_year.items():
        # Sort files by month to ensure the data is appended in order
        files.sort()
        # Initialize an empty DataFrame to append data
        year_df = pd.DataFrame()
        for file in files:
            month_df = pd.read_csv(file)
            year_df = pd.concat([year_df, month_df], ignore_index=True)

        # Save the consolidated DataFrame to a new CSV file
        output_filename = folder / f"{year}.csv"
        year_df.to_csv(output_filename, index=False)
        print(f"Consolidated CSV for {year} saved to {output_filename}")


# Example usage
folder_path = "Bank CSV test 2"  # Update this to the path of your folder containing the CSV files
consolidate_csv_by_year(folder_path)
