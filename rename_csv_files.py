import os

directory = "Bank CSV test"

for filename in os.listdir(directory):
    if filename.endswith(".csv") and len(filename) == 14:

        if filename.endswith(".csv") and len(filename.split("-")) == 3:
            # Split the filename to extract month, day, and the year part without '.csv'
            parts = filename.split("-")
            year = parts[2].split(".")[0]  # Remove '.csv'
            month = parts[0]
            day = parts[1]

            # Construct the new filename with year at the front
            new_filename = f"{year}-{month}-{day}.csv"

        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, new_filename)

        os.rename(old_file, new_file)
        print(f"Renamed '{filename}' to '{new_filename}'")

print("Renaming completed.")
