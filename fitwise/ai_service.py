from google import genai
import os
from dotenv import load_dotenv
load_dotenv()

api_key=os.getenv("api_key")

client = genai.Client(api_key=api_key)

def get_diet_plan(response_data):

   monthly_total= response_data["monthly_calories"]

   meal_type_summary = response_data["monthly_meal_type_calories"]

   meal_type_summary_text= ""

   for di in meal_type_summary:

      meal_type_summary_text += f". {di.get('meal_type')} : {di.get('total')} calorie \n"
   
   prompt = f"""
         Act as an expert nutritionist specializing in healthy eating and affordable Kerala cuisine.

         Here is the user's food intake summary:
         - Total Calories: {monthly_total:,}
         - Food Items and Categories: {meal_type_summary_text}

         Based on this data, generate a practical personalized diet plan:

         1. *Food Analysis:* Analyze the user's eating habits and calorie intake based on the available food logs.

         2. *Diet Plan:* Suggest a balanced 7-day meal plan with breakfast, lunch, dinner, and snacks using affordable Kerala foods. Include food names, portion sizes, and estimated calories.

         3. *Healthy Alternatives:* Recommend healthier alternatives to improve the user's eating habits while maintaining nutritional balance.

         4. *Actionable Tips:* Provide 3-4 practical tips for healthy eating, portion control, and affordable food choices.
         """
# Step 4: Call Gemini 2.5 Flash
   response = client.models.generate_content(
            model = "gemini-3.5-flash",
            contents=prompt
   )

   return response.text


