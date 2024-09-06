import rasterio
from rasterio.transform import from_origin
import numpy as np

def read_header(hdr_file):
    # Try different encodings to read the header file
    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'gbk']
    for encoding in encodings:
        try:
            with open(hdr_file, 'r', encoding=encoding) as hdr:
                header_lines = hdr.readlines()
            return header_lines
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Could not decode {hdr_file} with tried encodings")

def convert_envi_to_tiff(hdr_file, bil_file, output_tiff):
    # Read the header file to get metadata
    header_lines = read_header(hdr_file)
    
    metadata = {}
    for line in header_lines:
        if '=' in line:
            key, value = line.strip().split('=')
            metadata[key.strip().lower()] = value.strip()  # Ensure keys are in lowercase for consistency

    # Debug print statements for metadata
    print("Metadata extracted from header:")
    for key, value in metadata.items():
        print(f"{key}: {value}")

    # Extract relevant metadata with fallback mechanisms
    try:
        width = int(metadata.get('samples', 0))
        height = int(metadata.get('lines', 0))
        bands = int(metadata.get('bands', 1))
        data_type = metadata.get('data type', '0')
    except ValueError as e:
        print(f"Error parsing metadata values: {e}")
        width, height, bands, data_type = 0, 0, 1, '0'

    # Check if width, height, and bands are valid
    if width <= 0 or height <= 0 or bands <= 0:
        print(f"Invalid dimensions extracted: width={width}, height={height}, bands={bands}.")
        return  # Exit if dimensions are invalid

    # Data type mapping (ENVI data types to numpy dtypes)
    data_type_map = {
        '1': 'int16',
        '2': 'int32',
        '3': 'float32',
        '4': 'float64',
        '12': 'uint16'
    }

    dtype = data_type_map.get(data_type, 'uint8')

    # Read the binary raster data
    try:
        with open(bil_file, 'rb') as bil:
            data = np.fromfile(bil, dtype=dtype).reshape((bands, height, width))
    except ValueError as e:
        print(f"Error reshaping data: {e}. Check if the dimensions and dtype are correct.")
        return  # Exit if reshaping fails

    # Extract map info (assuming 'map info' key exists)
    map_info = metadata.get('map info', '0').split(',')
    if len(map_info) < 7:
        print(f"Invalid map info metadata: {map_info}.")
        return  # Exit if map info is invalid
    else:
        try:
            x_start = float(map_info[3])
            y_start = float(map_info[4])
            pixel_width = float(map_info[5])
            pixel_height = float(map_info[6])
        except ValueError as e:
            print(f"Error parsing map info values: {e}.")
            return  # Exit if parsing map info fails

    transform = from_origin(x_start, y_start, pixel_width, -pixel_height)  # Note: pixel_height is negative

    # Check for identity matrix
    if transform == from_origin(0.0, 0.0, 1.0, -1.0):
        print("Warning: Transform is identity or flipped identity matrix. Georeferencing may be incorrect.")

    # Write to TIFF
    with rasterio.open(
        output_tiff, 'w',
        driver='GTiff',
        height=height,
        width=width,
        count=bands,
        dtype=dtype,
        crs='EPSG:4326',  # You may need to update the CRS based on your data
        transform=transform
    ) as dst:
        for i in range(bands):
            dst.write(data[i, :, :], i + 1)

# Example usage
hdr_file = 'HWSD_RASTER/hwsd.hdr'
bil_file = 'HWSD_RASTER/hwsd.bil'
output_tiff = 'OUTPUT/output_file.tif'

convert_envi_to_tiff(hdr_file, bil_file, output_tiff)
