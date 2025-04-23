import os

# Website
WEBSITE_SERVER = "http://localhost:5173"

# Backend
BACKEND_PORT = 5000
CSV_FILEPATH = "./files/extracted_data.csv"
PREPROCESSED_FILEPATH = "./files/prepocessed_data.csv"

# constants
DEPTH_INCREMENT = 0.3
DECIMAL_POINTS = 3

def set_env(cut_direction):
    os.environ["DIR1"] = cut_direction
    if cut_direction == "X":
        os.environ["DIR2"] = "Y"
    else :
        os.environ["DIR2"] = "X"
        
