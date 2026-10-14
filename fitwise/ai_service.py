from google import genai

api_key="AQ.Ab8RN6I3UQF_UNmkLylTwj553RjGyN0IhVbEkrd2qqT3MmsuMQ"

def get_diet_plan(response_data):

    monthly_total= response_data["monthly_calories"]

    meal_type_summary = response_data["monthly_meal_type_calories"]

    meal_type_summary_text= ""

    for di in meal_type_summary:

       meal_type_summary_text += f". {di.get('meal_type')} : {di.get('total')} calorie \n"

    print(meal_type_summary_text)