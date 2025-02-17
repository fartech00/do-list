import streamlit as st
import requests
import geocoder

# List of all major cities in South Korea
cities = {
    "Seoul": (37.5665, 126.9780),
    "Busan": (35.1796, 129.0756),
    "Incheon": (37.4563, 126.7052),
    "Daegu": (35.8714, 128.6014),
    "Daejeon": (36.3504, 127.3845),
    "Gwangju": (35.1595, 126.8526),
    "Suwon": (37.2636, 127.0286),
    "Ulsan": (35.5384, 129.3114),
    "Changwon": (35.2270, 128.6811),
    "Goyang": (37.6584, 126.8320),
    "Jeonju": (35.8242, 127.1480),
    "Seongnam": (37.4200, 127.1260),
    "Cheongju": (36.6424, 127.4890),
    "Jeju": (33.4996, 126.5312),
}

# Function to get user's approximate location
def get_location():
    g = geocoder.ip("me")  
    if g.ok:
        return g.latlng  
    return None

# Function to get prayer times from API
def get_prayer_times(lat, lon):
    url = f"http://api.aladhan.com/v1/timings?latitude={lat}&longitude={lon}&method=2"
    response = requests.get(url)
    data = response.json()
    
    if "data" in data:
        return data["data"]["timings"]
    return None

# Sample user comments
comments = [
    "Great app! Very useful.",
    "Prayer times are accurate, thank you!",
    "Can you add a reminder feature?",
    "Would love to see weather info as well!"
]

# Streamlit UI
def main():
    st.title("🌅 Daily Sunset, Sunrise & Prayer Times")

    # Sidebar for city selection
    st.sidebar.header("📍 Select a City in South Korea")
    selected_city = st.sidebar.selectbox("Choose a city:", list(cities.keys()))

    # Auto-detect location or use selected city
    location = get_location()
    
    if location:
        auto_lat, auto_lon = location
        st.sidebar.write(f"🔍 Auto-detected Location: {auto_lat:.2f}, {auto_lon:.2f}")
    
    # Use selected city coordinates
    lat, lon = cities[selected_city]
    st.write(f"📍 Showing prayer times for **{selected_city}** ({lat}, {lon})")

    # Get prayer times
    prayer_times = get_prayer_times(lat, lon)
    
    if prayer_times:
        st.subheader("🕌 Today's Prayer Times")
        for prayer, time in prayer_times.items():
            st.write(f"**{prayer.capitalize()}**: {time}")
    else:
        st.error("Could not fetch prayer times. Try again later.")

    # Show comments section
    if st.button("Show Comments 💬"):
        st.subheader("User Comments")
        for comment in comments:
            st.write(f"- {comment}")

if __name__ == "__main__":
    main()
