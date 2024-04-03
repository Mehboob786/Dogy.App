## Dog Nutrition and Exercise Guide API
# Introduction
This FastAPI application is designed to assist dog owners by providing detailed nutrition information for dog food, personalized exercise recommendations based on the dog's profile, and locations for nearby dog-friendly exercise areas. It leverages the Google Places API for fetching location data and includes features for analyzing dog food nutrition through uploaded images.

# Setup
# Prerequisites
Python 3.8+
An API key for Google Maps API
Installation
Clone the repository


```
git clone https://github.com/Mehboob786/Dogy.App-BackEnd.git

```
Set up a virtual environment

```
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

```
# Install dependencies from requirements.txt
First, ensure you have a requirements.txt file in your project directory listing all necessary packages. Then, install the dependencies:

```
pip install -r requirements.txt

```

# Add any other dependencies here
Setting up Environment Variables
Create a .env file in your project's root directory. This file should include your Google Maps API key and any other environment variables your application needs. For example:

```
GOOGLE_Maps_API_KEY=your_google_maps_api_key
GoogleGeminiAPIKey=your_google_Gemini_api_key
OPENAI_API_KEY=your_OpenAI_api_key

```
# Any other API keys or sensitive information
This file will not be tracked by Git if you include .env in your .gitignore file, which is a best practice for security.

Running the Application
To run the application, use Uvicorn with the following command:


```
uvicorn main:app --reload

```
The API will then be accessible at http://127.0.0.1:8000.

# API Endpoints

GET /: Displays a welcome message.

Dog Profile and Exercise Recommendations

POST /dog-profile/: Accepts a dog's profile and returns exercise recommendations and nearby exercise locations.
Nutrition Analysis

POST /get-nutrition/: Analyzes uploaded images of dog food packaging to provide nutrition details.

# Development Notes

Customize the get_places and get_nearby_places functions based on your requirements for finding dog-friendly exercise locations.
The get_nutrition endpoint may require integrating with an external service or implementing a solution for nutrition analysis.

# Contributing
Contributions are welcome! Please contribute by reporting bugs, suggesting enhancements, or submitting pull requests.