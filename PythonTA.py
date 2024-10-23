import streamlit as st
import math

# Box information
boxes = {
    1: {
        "name": "Small Box",
        "dimensions": (30, 20, 15),
        "max_weight": 5,
        "price_per_kg": 50,
        "base_price": 100
    },
    2: {
        "name": "Medium Box",
        "dimensions": (40, 30, 20),
        "max_weight": 10,
        "price_per_kg": 40,
        "base_price": 150
    },
    3: {
        "name": "Large Box",
        "dimensions": (60, 40, 30),
        "max_weight": 20,
        "price_per_kg": 30,
        "base_price": 200
    },
    4: {
        "name": "Extra Large Box",
        "dimensions": (80, 60, 50),
        "max_weight": 30,
        "price_per_kg": 25,
        "base_price": 300
    },
}

province_coords = {
    "Bangkok": (13.756331, 100.501762),
    "Chiang Mai": (18.787747, 98.993128),
    "Chonburi": (13.361143, 100.984673),
    
}

# Function to calculate price and weight
def calculate_price_and_weight(box_info, weight, delivery_type):
    if weight > box_info["max_weight"]:
        return None, "Weight exceeds the box limit"
    extra_charge = 40 if delivery_type == "express" else 0
    total_price = weight * box_info["price_per_kg"] + box_info["base_price"] + extra_charge
    return total_price, weight

# Function to add delivery time
def add_delivery_time(start_time, delivery_time):
    start_hour, start_minute = map(int, start_time.split(':'))
    delivery_hour, delivery_minute = map(int, delivery_time.split(':'))
    total_minutes = (start_hour * 60 + start_minute) + (delivery_hour * 60 + delivery_minute)
    new_hour = (total_minutes // 60) % 24
    new_minute = total_minutes % 60
    return f"{new_hour:02d}:{new_minute:02d}"

# Haversine formula to calculate distance
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

# Streamlit app
st.title("Logistic Calculator")

# User inputs: weight
weight = st.number_input("Please enter the package weight (kg):", min_value=0.0, step=0.1)

# User inputs: delivery type
delivery_type = st.radio("Select Delivery Type:", ("standard", "express"))

# Calculate box and price
if weight > 0:
    suitable_boxes = [box_id for box_id, box_info in boxes.items() if weight <= box_info["max_weight"]]
    
    if suitable_boxes:
        selected_box_id = suitable_boxes[0]
        selected_box = boxes[selected_box_id]
        
        total_price, _ = calculate_price_and_weight(selected_box, weight, delivery_type)
        st.write(f"Selected Box: {selected_box['name']} (Size: {selected_box['dimensions'][0]}x{selected_box['dimensions'][1]}x{selected_box['dimensions'][2]} cm)")
        st.write(f"Total Price: {total_price:.2f} Baht")
    else:
        st.error("No suitable box for this weight.")

# User inputs: start time and province
start_time = st.text_input("Enter the delivery start time (HH:MM):", value="08:00")
selected_province = st.selectbox("Select Destination Province:", list(province_coords.keys()))

# Calculate delivery time
if st.button("Calculate Delivery Time"):
    if selected_box_id:
        delivery_time = "6:00" if delivery_type == "standard" else "4:00"
        estimated_arrival = add_delivery_time(start_time, delivery_time)
        st.write(f"Estimated Arrival Time in {selected_province}: {estimated_arrival} ({delivery_type.capitalize()} Delivery)")

# Confirm delivery
if st.button("Confirm Delivery"):
    if weight and selected_province and start_time:
        distance = haversine_distance(province_coords["Bangkok"][0], province_coords["Bangkok"][1],
                                      province_coords[selected_province][0], province_coords[selected_province][1])
        st.success(f"Delivery confirmed!\nPackage: {selected_box['name']}\nWeight: {weight} kg\nDistance: {distance:.2f} km\nProvince: {selected_province}\nStart Time: {start_time}")
    else:
        st.error("Please complete all fields.")



