from fastapi import FastAPI
import uvicorn
from selenium import webdriver
import requests
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Define the root route
@app.get("/")
async def root():
    return {"message": "jie small pp"}

@app.get("/properties") 
async def properties():
    return {"message": "jie small pp"}

@app.get("/properties/{state}/{city}")
async def get_properties(state: str, city: str):
    try:
        # Initialize WebDriver
        driver = webdriver.Firefox()
        driver.get(f"https://www.trulia.com/{state}/{city}/")  # Adjust URL based on state and city
        print(state)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit() if 'driver' in locals() else None
    





# Ensure the app runs only when this script is executed directly
if __name__ == "__main__":
    # uvicorn main:app --reload
    uvicorn.run(app, host="127.0.0.1", port=8000)
