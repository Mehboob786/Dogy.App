from fastapi import FastAPI, HTTPException, Request
import requests
from dotenv import load_dotenv
import os
from DogyExercise import GetExercises
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware



# Load environment variables from .env file
load_dotenv()

app = FastAPI()



origins = [
    "*",
    "https://dogy-app.vercel.app/"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def main():
    return {"message": "Hello World"}





base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
api_key = os.getenv("GOOGLE_Maps_API_KEY")

@app.get("/")
async def my_first_get_api():
    return {"message": "First FastAPI example"}

# @app.get("/nearby-places-names/")
# async def get_nearby_placesNames(latitude: float, longitude: float, radius: int = 500, place_type: str = 'park'):
#     # Use the API key from the environment variable
   
#     if not api_key:
#         raise HTTPException(status_code=500, detail="API key not found")
    
    
#     params = {
#         "location": f"{latitude},{longitude}",
#         "radius": radius,
#         "type": place_type,
#         "key": api_key
#     }
    
#     try:
#         response = requests.get(base_url, params=params)
#         if response.status_code == 200:
#             results = response.json()['results']
#             nearby_places = [place['name'] for place in results[:5]] # Get the first 5 places
#             return {"nearby_places": nearby_places}
#         else:
#             return HTTPException(status_code=400, detail="Error fetching data from Google Places API")
#     except Exception as e:
#         return HTTPException(status_code=500, detail=str(e))

class DogySensitivityModel(BaseModel):
    car: bool
    noise: bool
    none: bool 


class DogData(BaseModel):
    DogeSize: str
    DogyEnergyLevel: str
    DogySensitivity: DogySensitivityModel
    DogyAge: str
    Latitude: float  # Added for location
    Longitude: float  # Added for location



#async def get_exercise(data: DogData):
    # Extract properties directly from the data model instance
  #  doge_size = data.DogeSize
  #  dogy_energy_level = data.DogyEnergyLevel
  #  dogy_sensitivity = data.DogySensitivity
  #  dogy_age = data.DogyAge
    
    # Assuming GetExercises is a function that you have defined elsewhere



@app.post("/dog-profile/")
async def get_exercise_places(data: DogData):
    # Extracted directly from the data model instance, including location
    doge_size = data.DogeSize
    dogy_energy_level = data.DogyEnergyLevel
    dogy_sensitivity = data.DogySensitivity 
    dogy_age =  data.DogyAge
    latitude =  data.Latitude
    longitude =data.Longitude
    
    exercises = GetExercises(doge_size, dogy_energy_level, dogy_sensitivity, dogy_age)
    places = get_nearby_places(latitude, longitude)
    print("places")
    print (places)
    return {"exercises": exercises, "places": places}

@app.post("/get_nearby_places/")
def get_nearby_places(latitude: float, longitude: float):
    types = ["park", "gym", "pet_store"]
    places = []

    for location_type in types:
        places_results = get_places(latitude, longitude, location_type)
        print(places_results)
        for place in places_results[:1]:  # Limit to 1 place per type for diversity
            places.append({
                "name": place.get("name"),
                "type": location_type,
                "latitude": place["geometry"]["location"]["lat"],
                "longitude": place["geometry"]["location"]["lng"]
            })

    return places
 
def get_places(latitude: float, longitude: float, location_type: str):
    params = {
        "location": f"{latitude},{longitude}",
        "radius": "100000",
        "type": location_type,
        "key": api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        places_data = response.json()
        # Check if there's an error_message key in the response
        print(places_data)
        if 'error_message' in places_data:
            error_message = places_data['error_message']
            raise HTTPException(status_code=400, detail=error_message)
        return places_data.get('results', [])
    else:
        # If the response status code is not 200, raise an HTTPException with the status code and a generic message
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from Google Places API.")
    

