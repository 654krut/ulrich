import requests

# Define the URL of the M3U playlist
m3u_url = "http://line.protv.cc/get.php?username=9338741459&password=79615db6da37&type=m3u_plus&output=ts"  # Replace with your M3U URL

# Download the M3U file
response = requests.get(m3u_url)
m3u_content = response.text


# Filter the content (save lines starting with "pippo" and the next line)
filtered_lines = []
lines = m3u_content.splitlines()

filtered_lines.append(lines[0])
i = 1
while i < len(lines):
    if lines[i].find('tvg-name="IT')>-1:  # Check if the line contains tvg-name=IT
        filtered_lines.append(lines[i])  # Save the current line
        if i + 1 < len(lines):  # Ensure the next line exists
            filtered_lines.append(lines[i + 1])  # Save the following line
        i += 1  # Skip the next line, since it's already added
    i += 1

# Save the filtered content to a new M3U file
with open("ita.m3u", "w") as f:
    f.write("\n".join(filtered_lines))
