import pandas as pd
from geopy.geocoders import Nominatim
import folium
from folium.plugins import MarkerCluster

def get_address_data():
    names = []
    addresses = []
    phone_numbers = []
    print("Enter the names, addresses, and phone numbers (type 'done' when finished):")
    while True:
        name = input("Enter name: ")
        if name.lower() == 'done':
            break
        address = input("Enter address: ")
        if address.lower() == 'done':
            break
        phone_number = input("Enter phone number: ")
        if phone_number.lower() == 'done':
            break
        names.append(name)
        addresses.append(address)
        phone_numbers.append(phone_number)
    return pd.DataFrame({'Name': names, 'Address': addresses, 'Phone': phone_numbers})

def geocode_addresses(df):
    geolocator = Nominatim(user_agent="address_mapper")
    lats = []
    longs = []
    for address in df['Address']:
        location = geolocator.geocode(address)
        if location:
            lats.append(location.latitude)
            longs.append(location.longitude)
        else:
            lats.append(None)
            longs.append(None)
    df['Latitude'] = lats
    df['Longitude'] = longs
    return df

def create_map_with_markers(df):
    map_center = [df['Latitude'].mean(), df['Longitude'].mean()]
    folium_map = folium.Map(location=map_center, zoom_start=10)

    marker_cluster = MarkerCluster().add_to(folium_map)

    for _, row in df.iterrows():
        if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
            popup_text = f"<b>{row['Name']}</b><br>{row['Address']}<br>Phone: {row['Phone']}"
            folium.Marker(
                location=(row['Latitude'], row['Longitude']),
                popup=popup_text
            ).add_to(marker_cluster)
    
    return folium_map

if __name__ == "__main__":
    try:
        existing_data = pd.read_csv('addresses.csv')
    except FileNotFoundError:
        existing_data = pd.DataFrame(columns=['Name', 'Address', 'Phone'])

    new_data = get_address_data()
    combined_data = pd.concat([existing_data, new_data], ignore_index=True)
    combined_data = geocode_addresses(combined_data)

    map_with_markers = create_map_with_markers(combined_data)
    map_with_markers.save("address_mapper.html")  # Changed map file name

    combined_data.to_csv('addresses.csv', index=False)
