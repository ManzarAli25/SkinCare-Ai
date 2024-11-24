import os
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


def gemini_chat(messages):
    gemini = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro", temperature=0, max_tokens=None
    )
    return gemini(messages)

def get_recommendations(answers, results, severity_scale):
    prompt = f"""You are a skincare and wellness expert.
    Based on the following user-provided information, analyze their skin type, lifestyle, and dietary habits.
    Provide personalized dietary and lifesty le recommendations to help improve their skin health and address their specific skin concerns.
    ADITIIONAL INFORMATION:"""+json.dumps(answers,indent = 4)+"""
    ACNE SEVERIY :"""+ json.dumps(results,indent = 4)+"""
    HOW TO INTERPET THE RESULTS:"""+json.dumps(severity_scale) + """

    ### Task:
    1. **Analyze** the information provided to identify potential causes of the user's skin concerns (e.g., diet, hydration, sleep, allergies, or other habits).
    2. **Provide Specific Recommendations** for:
    - Diet (e.g., foods to include and avoid)
    - Lifestyle habits (e.g., sleep improvements, hydration, stress management)
    - Skincare routine adjustments, if applicable.
    3. Use simple and actionable advice tailored to the user's input.
    4. Ensure your tone is supportive and educational.
    """
    gemini = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
    response = gemini.invoke(prompt)
    return response.content
