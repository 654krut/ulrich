import requests

# Define the URL of the M3U playlist
m3u_url = "http://line.protv.cc/get.php?username=9338741459&password=79615db6da37&type=m3u_plus&output=ts"  # Replace with your M3U URL


# Download the M3U file
response = requests.get(m3u_url)

# Check if the response is successful
if response.status_code == 200 and response.headers['Content-Type'].startswith('application/octet-stream'):
    m3u_content = response.text

    # Define a dictionary mapping filenames to search strings
    file_conditions = {
        "ita.m3u": 'tvg-name="IT',  # File 1: Contains "tvg-name=\"IT\""
        "pol.m3u": 'tvg-name="PL',  # File 2: Contains "tvg-name=\"PL\""
    }

    # Create a dictionary to hold the filtered lines for each file
    filtered_files = {filename: [] for filename in file_conditions}

    # Process the M3U content
    lines = m3u_content.splitlines()

    # Keep the first line (if it's a #EXTM3U line) for each file
    if lines:
        for filtered_list in filtered_files.values():
            filtered_list.append(lines[0])

    # Iterate through the lines and apply filters
    i = 1
    while i < len(lines):
        for filename, search_string in file_conditions.items():
            if search_string in lines[i]:  # Check if the line contains the search string
                filtered_files[filename].append(lines[i])  # Save the current line
                if i + 1 < len(lines):  # Ensure the next line exists
                    filtered_files[filename].append(lines[i + 1])  # Save the following line (the URL)
                break  # Stop further checks once a condition is matched for this line
        i += 2  # Skip to the next relevant line (since we add two lines at a time)

    # Save the filtered content to each corresponding M3U file
    for filename, filtered_lines in filtered_files.items():
        with open(filename, "w") as f:
            f.write("\n".join(filtered_lines))

    print("Filtered M3U files created successfully!")

else:
    print(f"Error: Unable to fetch M3U file. Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
    print(response.text[:500])  # Print the first 500 characters of the response for debugging
