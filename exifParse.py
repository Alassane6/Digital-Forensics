import exifread
import sys

def parsewexif(file_path):
    try:
        with open(file_path, "rb") as image: 
            exif_tags = exifread.process_file(image)        
            lat_ref = exif_tags.get('GPS GPSLatitudeRef', None)
            lat = exif_tags.get('GPS GPSLatitude')
            lon_ref = exif_tags.get('GPS GPSLongitudeRef', None)
            lon = exif_tags.get('GPS GPSLongitude')

            def convert_to_float(value):
                return float(value.num) / float(value.den) if hasattr(value, 'num') and hasattr(value, 'den') else float(value)

            if lat and lat_ref and lon and lon_ref:
                lat_deg = lat.values[0]
                lat_min = convert_to_float(lat.values[1])
                lat_sec = convert_to_float(lat.values[2]) / 60.0  # Convert to decimal minutes
                lon_deg = lon.values[0]
                lon_min = convert_to_float(lon.values[1])
                lon_sec = convert_to_float(lon.values[2]) / 60.0  # Convert to decimal minutes
                
                # Convert longitude to negative if reference is 'W'
                if lon_ref.values == 'W':
                    lon_deg = -lon_deg   
                latitude = f"{lat_deg} degrees, {lat_min:.1f} minutes, {convert_to_float(lat.values[2]):.1f} seconds" 
                longitude = f"{lon_deg} degrees, {lon_min:.1f} minutes, {convert_to_float(lon.values[2]):.1f} seconds"
            else:
                latitude, longitude = "N/A", "N/A"    

            print(f"Source File: {file_path}")
            print(f"Make: {exif_tags.get('Image Make')}")
            print(f"Model: {exif_tags.get('Image Model')}")
            print(f"Original Date/Time: {exif_tags.get('EXIF DateTimeDigitized')}")       
            print(f"Latitude: {latitude}")
            print(f"Longitude: {longitude}")

    except IOError:
        print("Error! - File Not Found!")
    except Exception as e:
        print(f"Error processing EXIF data: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error! - No Image File Specified!")
    else:
        parsewexif(sys.argv[1])
