"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import os
from dotenv import load_dotenv
from fastapi import HTTPException
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()


api_key = os.getenv("GoogleGeminiAPIKey")



genai.configure(api_key=api_key)

def GetExercisestest(DogeSize,DogyEnergyLevel,DogySensitivity,DogyAge):
                

                genai.configure(api_key=api_key)

            # Set up the model
                generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
            }

                safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            ]

                model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                        generation_config=generation_config,
                                        safety_settings=safety_settings)

                prompt_parts = [
            f"input: Given the following characteristics of a dog:\n- Size: {DogeSize}\n- Energy Level: {DogyEnergyLevel}\n- Sensitivity: {DogySensitivity}\n- Age: {DogyAge}\n\nProvide a detailed exercise summary tailored for this dog. The summary should include recommendations on the type, duration, and intensity of exercise appropriate for the dog's size, energy level, sensitivity, and age. Consider the dog's physical and emotional well-being, ensuring the suggested activities promote health without causing undue stress or exhaustion.",
            f"output: Detailed Summary of Exercises for Dogy",
            f"input: dog:\n- Size: {DogeSize}\n- Energy Level: {DogyEnergyLevel}\n- Sensitivity: {DogySensitivity}\n- Age: {DogyAge}",
            f"output: ",
            ]

                response = model.generate_content(prompt_parts)
                return response.text

def GetExercises(DogeSize, DogyEnergyLevel, DogySensitivity, DogyAge):
    try:
        # Assuming genai is a properly imported library and api_key is defined somewhere
        genai.configure(api_key=api_key)

        # Set up the model
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)

        prompt_parts = [
            f"input: Given the following characteristics of a dog:\n- Size: {DogeSize}\n- Energy Level: {DogyEnergyLevel}\n- Sensitivity: {DogySensitivity}\n- Age: {DogyAge}\n\nProvide a detailed exercise summary tailored for this dog. The summary should include recommendations on the type, duration, and intensity of exercise appropriate for the dog's size, energy level, sensitivity, and age. Consider the dog's physical and emotional well-being, ensuring the suggested activities promote health without causing undue stress or exhaustion.",
            "output: Detailed Summary of Exercises for Dogy",
            f"input: dog:\n- Size: {DogeSize}\n- Energy Level: {DogyEnergyLevel}\n- Sensitivity: {DogySensitivity}\n- Age: {DogyAge}",
            "output: ",
        ]

        response = model.generate_content(prompt_parts)
        return response.text

    except HTTPException as e:
        # Here, instead of just logging or returning the error, we throw it
        raise HTTPException(f"Failed to generate exercises due to an error: {e}")
