import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from datetime import date

load_dotenv()

# Configuration for both local and Streamlit Cloud
genai.configure(api_key=os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY"))

def generate_response(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

def main():
    st.title("🌍 Personalized Travel Itinerary Generator")

    with st.expander("📝 Tell Us About Your Trip"):
        # Destination and Dates
        destination = st.text_input("Destination")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=date.today(), min_value=date.today())
        with col2:
            end_date = st.date_input("End Date", 
                                   min_value=start_date,
                                   value=start_date)
        
        # Calculate duration
        duration = (end_date - start_date).days + 1
        
        # Trip Details
        budget = st.selectbox("Budget Level", [
            "Low Budget", "Low To Moderate", 
            "Moderate", "Moderate To High", "Luxury"
        ])
        number_of_people = st.number_input("Number of People", min_value=1, max_value=30, value=1)
        purpose = st.text_input("Trip Purpose (e.g. Friends Getaway, Solo Adventure, Couples Retreat)", value="General Trip")
        activities = st.text_input("Activities You Want to Try (e.g., Scuba Diving, Hiking, Museum Hopping)")
        dietary = st.text_input("Dietary Preferences (e.g., Vegan, Gluten-Free)")
        allergies = st.text_input("Food Allergies (e.g., Peanuts, Shellfish)")
        mobility = st.selectbox("Walking Tolerance", ["Low", "Moderate", "High"])
        accommodation = st.text_input("Accommodation Preferences (e.g., Hotels, AirBnb, Resort, Hostels, Cabin, etc.)")
        specific_features = st.text_input("Specific Features In Accomdation (e.g., Pool, Gym, Kitchen, etc.)")
        place_of_accomodation = st.text_input("Place Of Accomodation (e.g. Central Location, Near A Specific Location, Surrounded by Nature, etc., etc.)")

    if st.button("✨ Generate My Perfect Itinerary") and destination:
        # Format dates
        start_fmt = start_date.strftime("%b %d")
        end_fmt = end_date.strftime("%b %d")
        
        # Build prompt
        base_prompt = f"""
        Create a {duration}-day itinerary for {destination} ({start_fmt} to {end_fmt}) with:
        - Budget: {budget}
        - Number of People: {number_of_people}
        - Travel Purpose: {purpose}
        - Desired Activities: {activities if activities else 'General Exploration'}
        - Dietary Needs: {dietary if dietary else 'No restrictions'}
        - Food Allergies: {allergies if allergies else 'None'}
        - Mobility Level: {mobility}
        - Accommodation: {accommodation if accommodation else 'Not specified'}
        - Specific Features: {specific_features if specific_features else 'Not specified'}
        - Place Of Accomodation: {place_of_accomodation if place_of_accomodation else 'Not Specified'}
        
        Include for each day:
        Morning, Afternoon, and Evening activities
        2-3 dining options with dietary accommodations
        Transportation options between locations
        Cost estimates for each activity mentioned above
        Local insider tips and hidden gems
        """

        refined_prompt = f"""
        {base_prompt}
        Structure this itinerary:
        1. Group nearby attractions to minimize travel time
        2. Balance popular spots with unique local experiences
        3. Include time buffers for meals and transit and meals should follow dietary restrictions
        4. Add safety tips and cultural notes
        5. Format with clear daily headings and emojis
        6. Give me answer only in english
        7. Provide a summary at the end with total cost and time spent on each activity
        """

        with st.spinner("🧭 Planning your adventure..."):
            itinerary = generate_response(refined_prompt)
        
        st.subheader(f"🗓️ Your {duration}-Day {destination} Itinerary")
        st.markdown(itinerary)
        
        st.success("✅ Trip planning complete! Bon voyage!")

if __name__ == "__main__":
    main()