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
    "Amnat Charoen": (15.858743, 104.625777),
    "Ang Thong": (14.589605, 100.455017),
    "Bueng Kan": (18.360912, 103.651171),
    "Buriram": (14.993001, 103.102919),
    "Chachoengsao": (13.688348, 101.071243),
    "Chai Nat": (15.185382, 100.125216),
    "Chaiyaphum": (15.806817, 102.031502),
    "Chanthaburi": (12.611456, 102.103832),
    "Chiang Mai": (18.787747, 98.993128),
    "Chiang Rai": (19.910479, 99.840576),
    "Chonburi": (13.361143, 100.984673),
    "Chumphon": (10.493049, 99.180019),
    "Kalasin": (16.432836, 103.506091),
    "Kamphaeng Phet": (16.483407, 99.522151),
    "Kanchanaburi": (14.020854, 99.532811),
    "Khon Kaen": (16.441935, 102.835992),
    "Krabi": (8.086300, 98.906283),
    "Lampang": (18.288840, 99.490806),
    "Lamphun": (18.574188, 99.008728),
    "Loei": (17.490533, 101.727119),
    "Lopburi": (14.799507, 100.653377),
    "Mae Hong Son": (19.301672, 97.969646),
    "Maha Sarakham": (16.184520, 103.300878),
    "Mukdahan": (16.545311, 104.723052),
    "Nakhon Nayok": (14.204893, 101.214394),
    "Nakhon Pathom": (13.819920, 100.062167),
    "Nakhon Phanom": (17.392039, 104.769405),
    "Nakhon Ratchasima": (14.979900, 102.097769),
    "Nakhon Sawan": (15.704987, 100.137116),
    "Nakhon Si Thammarat": (8.432267, 99.963120),
    "Nan": (18.783768, 100.778175),
    "Narathiwat": (6.426481, 101.823547),
    "Nong Bua Lamphu": (17.204850, 102.440628),
    "Nong Khai": (17.878280, 102.744387),
    "Nonthaburi": (13.859108, 100.514352),
    "Pathum Thani": (14.020920, 100.525766),
    "Pattani": (6.869742, 101.250482),
    "Phang Nga": (8.451090, 98.529288),
    "Phatthalung": (7.617828, 100.074559),
    "Phayao": (19.168548, 99.901813),
    "Phetchabun": (16.418291, 101.160565),
    "Phetchaburi": (13.113152, 99.940368),
    "Phichit": (16.440630, 100.348959),
    "Phitsanulok": (16.821510, 100.265369),
    "Phrae": (18.145669, 100.141816),
    "Phuket": (7.880447, 98.392540),
    "Prachinburi": (14.047995, 101.365007),
    "Prachuap Khiri Khan": (11.803130, 99.800682),
    "Ranong": (9.952870, 98.608464),
    "Ratchaburi": (13.527732, 99.811188),
    "Rayong": (12.681197, 101.278939),
    "Roi Et": (16.054411, 103.653131),
    "Sa Kaeo": (13.824038, 102.064583),
    "Sakon Nakhon": (17.155417, 104.147732),
    "Samut Prakan": (13.599096, 100.599831),
    "Samut Sakhon": (13.547066, 100.274399),
    "Samut Songkhram": (13.409371, 100.002410),
    "Saraburi": (14.527712, 100.910204),
    "Satun": (6.623800, 100.065280),
    "Sing Buri": (14.887292, 100.402172),
    "Sisaket": (15.118485, 104.322663),
    "Songkhla": (7.189343, 100.595171),
    "Sukhothai": (17.007926, 99.822759),
    "Suphan Buri": (14.474159, 100.117765),
    "Surat Thani": (9.138240, 99.321748),
    "Surin": (14.881866, 103.493629),
    "Tak": (16.871311, 99.124159),
    "Trang": (7.558756, 99.611686),
    "Trat": (12.242981, 102.517473),
    "Ubon Ratchathani": (15.244435, 104.857052),
    "Udon Thani": (17.364696, 102.815578),
    "Uthai Thani": (15.378702, 100.026981),
    "Uttaradit": (17.627542, 100.099294),
    "Yala": (6.541147, 101.280672),
    "Yasothon": (15.792196, 104.145090)
    # Add more provinces if needed...
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

