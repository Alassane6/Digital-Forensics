EXIF Metadata Parser (exif_parser.py)

This Python script extracts and displays key EXIF metadata from an image file, including camera make and model, date/time the image was taken, and GPS coordinates (if available).
📸 Features

    Parses EXIF metadata from JPEG or TIFF image files.

    Extracts and prints:

        Camera make and model

        Date and time of original capture

        GPS latitude and longitude (in degrees, minutes, and seconds)

🛠️ Requirements

    Python 3.6+

    pip

    exifread

You can install the required library using pip:

pip install exifread

🚀 Usage

Run the script from the command line and provide an image file path as an argument:

python exif_parser.py path/to/image.jpg (file1 or file2)

Sample Output

Source File: path/to/image.jpg
Make: Canon
Model: Canon EOS REBEL T6
Original Date/Time: 2021:07:20 14:52:11
Latitude: 37 degrees, 48.9 minutes, 22.0 seconds
Longitude: -122 degrees, 25.3 minutes, 15.0 seconds

📂 File Structure

exif_parser.py  # Main script to extract and display EXIF metadata

⚠️ Notes

    Only images with embedded GPS data will return latitude and longitude values.

    If EXIF data is missing or corrupted, appropriate error messages will be displayed.

    GPS coordinates are partially converted to human-readable format, but not to decimal degrees (this can be added if needed).

🧪 Example Image for Testing

To test the script effectively, use an image file taken with GPS-enabled devices like smartphones or DSLR cameras with GPS support.






Chrome History Analyzer

This Python script extracts and summarizes useful forensic information from a Google Chrome History SQLite database, including file downloads and search terms.
🔍 Features

    Analyzes Chrome's History SQLite file

    Extracts and reports:

        Number of downloads and largest file

        Number of unique search terms

        Most recent search term with timestamp

🛠️ Requirements

    Python 3.6+

    Standard library only (no external packages needed)

📦 How to Use

    Locate Chrome's History database file:

        On Windows: C:\Users\<username>\AppData\Local\Google\Chrome\User Data\Default\History

        On macOS: ~/Library/Application Support/Google/Chrome/Default/History

        On Linux: ~/.config/google-chrome/Default/History

    Run the script from the command line:

    python chrome_history_parser.py /path/to/History

