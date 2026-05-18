import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Perceptron
import os

model = None
scaler = None

def assess_quality_logic(co2, pm25, humidity, occupancy, vent_status):
    """Hàm chấm điểm dựa trên đúng 5 thông số UI truyền vào"""
    score = 0
    # 1. Điểm CO2
    if co2 < 1000: score += 1
    elif co2 < 1500: score += 2
    else: score += 3

    # 2. Điểm PM2.5
    if pm25 < 25: score += 1
    elif pm25 < 50: score += 2
    else: score += 3

    # 3. Điểm Độ ẩm
    if 40 <= humidity <= 60: score += 1
    elif 30 <= humidity < 40 or 60 < humidity <= 75: score += 2
    else: score += 3

    # 4. Điểm Số người
    if occupancy < 15: score += 1
    elif occupancy < 30: score += 2
    else: score += 3

    # 5. Điểm Thông gió
    if vent_status == 0: score += 2  # Phạt điểm nếu đóng cửa
    else: score += 0

    # Tổng kết
    if score <= 6: return "Good"
    elif score <= 10: return "Average"
    else: return "Hazardous"

def init_brain():
    global model, scaler
    csv_path = 'IoT_Indoor_Air_Quality_Dataset.csv'
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Không tìm thấy file {csv_path}. Hãy để file dữ liệu cùng thư mục code.")

    df = pd.read_csv(csv_path).dropna()

    # Xử lý cột Thông gió thành số (0 và 1)
    df['Vent_Encoded'] = df.iloc[:, 11].astype(str).str.strip().str.lower().map({'open': 1, 'closed': 0}).fillna(0)

    # Lấy 5 cột Inputs
    X = pd.DataFrame({
        'CO2': df.iloc[:, 3],
        'PM2.5': df.iloc[:, 4],
        'Humidity': df.iloc[:, 2],
        'Occupancy': df.iloc[:, 10],
        'Ventilation': df['Vent_Encoded']
    })

    # Chạy hàm tạo nhãn cho toàn bộ dữ liệu
    y = df.apply(lambda r: assess_quality_logic(r.iloc[3], r.iloc[4], r.iloc[2], r.iloc[10], df['Vent_Encoded'][r.name]), axis=1)

    # Chuẩn hóa dữ liệu
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Dùng đúng mạng Perceptron theo yêu cầu thầy
    model = Perceptron(max_iter=1000, random_state=42)
    model.fit(X_scaled, y)

def predict_air_status(user_data):
    """Hàm này đã được đổi tên để khớp với lệnh gọi trong file main.py"""
    global model, scaler
    
    # user_data = [co2_val, pm25_val, hum_val, occ_val, vent_val]
    input_df = pd.DataFrame([user_data], columns=['CO2', 'PM2.5', 'Humidity', 'Occupancy', 'Ventilation'])
    
    input_scaled = scaler.transform(input_df)
    return model.predict(input_scaled)[0]