import shutil
from fastapi import FastAPI, HTTPException, BackgroundTasks
from dotenv import load_dotenv
import os
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import BaseModel
import nutrition_api
import assistant
import shutil
import requests
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



@app.post("/get-nutrition/")
async def get_nutrition(files: list[UploadFile] = File(...), user_message: Optional[str] = None):
    image_paths = []
    for file in files:
        # Save temporary image file
        try:
            temp_file_path = f"temp_{file.filename}"
            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            image_paths.append(temp_file_path)
        finally:
            file.file.close()

    if not image_paths:
        raise HTTPException(status_code=400, detail="No images provided")

    try:
        response = nutrition_api.get_nutritional_details(image_paths,user_message=user_message)
        # Clean up: remove temporary files after processing
        for path in image_paths:
            os.remove(path)
        return JSONResponse(content=response)
    except Exception as e:
        # Clean up: remove temporary files in case of an error
        for path in image_paths:
            os.remove(path)
        raise HTTPException(status_code=500, detail=str(e))
class AssistantRequest(BaseModel):
    name: str
    instructions: str
    model: str
    file_ids: List[str]

class MessageRequest(BaseModel):
    thread_id: str
    assistant_id: str
    user_message: str
