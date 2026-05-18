import customtkinter as ctk
import threading
import os
from tkinter import messagebox
import logic_module
import requests
from PIL import Image # Thư viện để chèn ảnh

# --- CẤU HÌNH MÀU SẮC THƯƠNG HIỆU SKQ ANALYTICS - CORPORATE LIGHT MODE ---
SKQ_BG = "#F4F7FC"            # Nền chính (Xám cực nhạt)
SKQ_PANEL_LIGHT = "#FFFFFF"   # Nền Panel (Trắng)
SKQ_NAVY = "#091C3E"         # Xanh Navy đậm đặc trưng (Dùng cho Header)
SKQ_PANEL = "#122A59"        
SKQ_BLUE = "#33B5FF"         # Xanh Sky Blue dạ quang (Dùng cho điểm nhấn)
SKQ_BLUE_HOVER = "#2797D6"   
SKQ_BTN_DARK = "#0A1833"     # Nút phụ tối màu (Navy đậm)
SKQ_BTN_DARK_HOVER = "#122A59"
SKQ_TEXT_BLACK = "#1A1A1A"   # Văn bản chính trên nền trắng
SKQ_TEXT_GREY = "#666666"    # Văn bản phụ
SKQ_TEXT_WHITE = "#FFFFFF"

# --- CẤU HÌNH FONT CHỮ (Đảm bảo máy đã cài font Montserrat) ---
FONT_MAIN = ("Montserrat", 13)
FONT_LABEL = ("Montserrat", 13, "bold")
FONT_V = ("Montserrat", 15)
FONT_TITLE = ("Montserrat", 20, "bold")
FONT_BIG = ("Montserrat", 72, "bold")

ctk.set_appearance_mode("Light") # Chuyển sang chế độ sáng

class AirClassifyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SKQ Analytics - AI Room Environment Classifier")
        self.geometry("1150x750")
        self.configure(fg_color=SKQ_BG) 
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Load trước các Asset Hình ảnh
        self.load_images()
        self.show_loading()

    def load_images(self):
        """Tải hình ảnh thương hiệu vào bộ nhớ"""
        try:
            # Logo màu chính
            self.img_logo_color = ctk.CTkImage(light_image=Image.open("Logo nền màu.png"),
                                               dark_image=Image.open("Logo nền màu.png"),
                                               size=(180, 180))
            
            # Logo trắng (dùng cho Header Navy)
            self.img_logo_white = ctk.CTkImage(light_image=Image.open("Logo nền trắng.png"),
                                               dark_image=Image.open("Logo nền trắng.png"),
                                               size=(100, 100))
            
            # Logo trắng icon (dùng cho nút GPS)
            self.img_icon_white = ctk.CTkImage(light_image=Image.open("Logo nền trắng.png"),
                                               dark_image=Image.open("Logo nền trắng.png"),
                                               size=(25, 25))

            # Hình ảnh minh họa Mockup nền trắng (Hình nền đt trắng.png)
            self.img_mockup_white = ctk.CTkImage(light_image=Image.open("Giao diện người dùng 2.png"),
                                                 dark_image=Image.open("Giao diện người dùng 2.png"),
                                                 size=(280, 400))
        except Exception as e:
            print("Lưu ý: Không tìm thấy file ảnh gốc. App sẽ chạy không có ảnh.", e)
            self.img_logo_color = None
            self.img_logo_white = None
            self.img_icon_white = None
            self.img_mockup_white = None

    def show_loading(self):
        # Màn hình chờ vẫn giữ Navy cho sang trọng khi giới thiệu thương hiệu
        self.loading_win = ctk.CTkToplevel(self)
        self.loading_win.title("Khởi động hệ thống")
        self.loading_win.geometry("450x300")
        self.loading_win.configure(fg_color=SKQ_NAVY)
        self.loading_win.attributes("-topmost", True)
        self.loading_win.grab_set()
        
        # Chèn Logo vào màn hình chờ
        if self.img_logo_color:
            ctk.CTkLabel(self.loading_win, text="", image=self.img_logo_color).pack(pady=(20, 10))

        ctk.CTkLabel(self.loading_win, text="⏳ ĐANG KHỞI ĐỘNG HỆ THỐNG...\n\nSKQ Analytics đang huấn luyện mạng Perceptron...", 
                     font=FONT_LABEL, text_color=SKQ_BLUE).pack(pady=10)
        
        threading.Thread(target=self.train_async, daemon=True).start()

    def train_async(self):
        try:
            logic_module.init_brain()
            self.after(0, self.build_layout)
            self.after(500, self.loading_win.destroy) # Đợi nửa giây cho mượt
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Lỗi hệ thống", str(e)))

    def build_layout(self):
        # --- PANEL TRÁI (Nền Trắng) ---
        self.left_frame = ctk.CTkScrollableFrame(self, width=420, corner_radius=15, fg_color=SKQ_PANEL_LIGHT)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        # Chèn Logo màu nhỏ gọn ở góc trái trên cùng
        if self.img_logo_color:
            self.small_logo = ctk.CTkImage(Image.open("Logo nền màu.png"), size=(100, 100))
            ctk.CTkLabel(self.left_frame, text="", image=self.small_logo).pack(pady=(15, 0))

        ctk.CTkLabel(self.left_frame, text="THÔNG SỐ & BỐI CẢNH", font=FONT_TITLE, text_color=SKQ_BLUE).pack(pady=(5, 25))

        self.entry_co2 = self.create_labeled_entry("☁️ Nồng độ CO2 (ppm):", "VD: 415.0")
        self.entry_pm25 = self.create_labeled_entry("💨 Bụi mịn PM2.5 (µg/m³):", "VD: 28.4")
        self.entry_hum = self.create_labeled_entry("💧 Độ ẩm không khí (%):", "VD: 62.5")
        self.entry_occ = self.create_labeled_entry("👥 Số người trong phòng:", "VD: 12")

        ctk.CTkLabel(self.left_frame, text="🌬️ Trạng thái thông gió:", font=FONT_LABEL, text_color=SKQ_TEXT_BLACK).pack(anchor="w", padx=30, pady=(10, 2))
        self.combo_vent = ctk.CTkComboBox(self.left_frame, values=["Open", "Closed"], font=FONT_V, height=45, 
                                          fg_color=SKQ_PANEL_LIGHT, border_color="#E0E0E0", button_color=SKQ_BLUE,
                                          text_color=SKQ_TEXT_BLACK,
                                          command=self.reset_button)
        self.combo_vent.pack(fill="x", padx=30, pady=(0, 20))
        self.combo_vent.set("Open")

        # Nút lấy dữ liệu: Nền Navy, tích hợp Logo trắng nhỏ
        if self.img_icon_white:
            self.btn_gps = ctk.CTkButton(self.left_frame, text=" LẤY DỮ LIỆU TỪ TRẠM VỆ TINH", 
                                         font=("Montserrat", 13, "bold"), fg_color=SKQ_BTN_DARK, hover_color=SKQ_BTN_DARK_HOVER,
                                         height=45, corner_radius=8, image=self.img_icon_white, compound="left", command=self.autofill_from_station)
        else:
            self.btn_gps = ctk.CTkButton(self.left_frame, text="📍 LẤY DỮ LIỆU TỪ TRẠM VỆ TINH", 
                                         font=("Montserrat", 13, "bold"), fg_color=SKQ_BTN_DARK, hover_color=SKQ_BTN_DARK_HOVER,
                                         height=45, corner_radius=8, command=self.autofill_from_station)
        self.btn_gps.pack(fill="x", padx=40, pady=(15, 0))

        # Nút Phân tích chính
        self.btn_main = ctk.CTkButton(self.left_frame, text="🚀 CHẠY PHÂN TÍCH AI", 
                                      font=("Montserrat", 16, "bold"), height=60, corner_radius=12,
                                      fg_color=SKQ_BLUE, hover_color=SKQ_BLUE_HOVER, text_color=SKQ_NAVY,
                                      command=self.start_classification)
        self.btn_main.pack(fill="x", padx=30, pady=25)

    def create_labeled_entry(self, label_text, placeholder):
        container = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        container.pack(fill="x", padx=30, pady=5)
        ctk.CTkLabel(container, text=label_text, font=FONT_LABEL, text_color=SKQ_TEXT_BLACK).pack(anchor="w")
        
        ent = ctk.CTkEntry(container, placeholder_text=placeholder, font=FONT_V, height=40,
                           fg_color=SKQ_PANEL_LIGHT, border_color="#E0E0E0", text_color=SKQ_TEXT_BLACK,
                           placeholder_text_color=SKQ_TEXT_GREY)
        ent.pack(fill="x", pady=(2, 10))
        ent.bind("<KeyRelease>", self.reset_button)
        return ent

    def reset_button(self, event=None):
        self.btn_main.configure(state="normal", text="🚀 CHẠY PHÂN TÍCH AI", fg_color=SKQ_BLUE, text_color=SKQ_NAVY)

    def start_classification(self):
        try:
            co2 = float(self.entry_co2.get())
            pm25 = float(self.entry_pm25.get())
            hum = float(self.entry_hum.get())
            occ = int(self.entry_occ.get())
            vent = 1 if self.combo_vent.get() == "Open" else 0
            
            self.btn_main.configure(state="disabled", text="⌛ HỆ THỐNG ĐANG QUYẾT ĐỊNH...", fg_color=SKQ_BTN_DARK, text_color=SKQ_TEXT_WHITE)
            threading.Thread(target=self.run_ai, args=([co2, pm25, hum, occ, vent],), daemon=True).start()
        except ValueError:
            messagebox.showerror("Lỗi dữ liệu", "Vui lòng nhập đầy đủ các thông số dạng số học!")

    def run_ai(self, user_inputs):
        try:
            result = logic_module.predict_air_status(user_inputs)
            self.after(0, self.display_result, result)
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Lỗi Logic", str(e)))
            self.after(0, self.reset_button)

    def build_right_panel(self, color_status, text_status, is_initial=False):
        if hasattr(self, 'right_frame'):
            self.right_frame.destroy()

        self.right_frame = ctk.CTkFrame(self, corner_radius=20, fg_color=SKQ_PANEL_LIGHT)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)
        
        # --- HEADER PANEL PHẢI: Xanh Navy đậm, chứa Logo trắng ---
        self.header_frame = ctk.CTkFrame(self.right_frame, height=100, fg_color=SKQ_NAVY, corner_radius=15)
        self.header_frame.pack(fill="x", padx=10, pady=10)
        
        if self.img_logo_white:
            ctk.CTkLabel(self.header_frame, text="", image=self.img_logo_white).pack(pady=10)

        # Body Frame chứa nội dung (Trắng)
        self.body_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.body_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.body_frame.grid_columnconfigure(0, weight=1)

        # Nếu là trạng thái mới khởi chạy (READY), hiển thị ảnh Mockup TRẮNG
        if is_initial and self.img_mockup_white:
            ctk.CTkLabel(self.body_frame, text="HỆ THỐNG SẴN SÀNG", font=FONT_TITLE, text_color=SKQ_TEXT_BLACK).pack(pady=(40, 20))
            ctk.CTkLabel(self.body_frame, text="", image=self.img_mockup_white).pack(pady=10)
            ctk.CTkLabel(self.body_frame, text="Sẵn sàng tiếp nhận dữ liệu từ cảm biến hoặc vệ tinh", font=("Montserrat", 13, "italic"), text_color=SKQ_TEXT_GREY).pack(pady=20)
            return

        # Nếu là trạng thái đã có kết quả
        ctk.CTkLabel(self.body_frame, text="BÁO CÁO CHẤT LƯỢNG MÔI TRƯỜNG", font=FONT_TITLE, text_color=SKQ_TEXT_GREY).pack(pady=(100, 10))

        # Khung chứa kết quả lớn (Vẫn Navy để nổi kết quả sáng)
        result_box = ctk.CTkFrame(self.body_frame, fg_color="#0A1833", corner_radius=20)
        result_box.pack(pady=20, padx=80, fill="x")
        
        self.lbl_big_result = ctk.CTkLabel(result_box, text=text_status, font=FONT_BIG, text_color=color_status)
        self.lbl_big_result.pack(pady=50)
        
        ctk.CTkLabel(self.body_frame, text="Sustainable Key Quality - Protected by Perceptron AI", font=("Montserrat", 12, "italic"), text_color=SKQ_TEXT_GREY).pack(pady=(40, 0))

    def display_result(self, status):
        color = "#2EE08D" if status == "Good" else "#FBBF24" if status == "Average" else "#FF5252"
        self.build_right_panel(color, status.upper())
        self.reset_button()

    def autofill_from_station(self):
        REAL_STATIONS = {
            "📍 Cơ sở B UEH Nguyễn Tri Phương (Q.10)": (10.7610, 106.6683),
            "📍 CFVG - UEH Cơ sở C (Q.10)":(10.7735, 106.6774),
            "📍 Ngã tư Hàng Xanh (Bình Thạnh)": (10.8016, 106.7116),
            "📍 Khu công nghệ cao (TP. Thủ Đức)": (10.8521, 106.7987),
            "📍 Phố đi bộ Nguyễn Huệ (Q.1)": (10.7743, 106.7031)
        }

        # Popup cũng dùng tông màu sáng, Header Navy
        popup = ctk.CTkToplevel(self)
        popup.title("Truy xuất dữ liệu Vệ Tinh")
        popup.geometry("500x220")
        popup.configure(fg_color=SKQ_BG)
        popup.attributes("-topmost", True)
        popup.grab_set()

        ctk.CTkLabel(popup, text="📡 CHỌN TRẠM ĐO ĐỂ TẢI DỮ LIỆU", font=FONT_LABEL, text_color=SKQ_BLUE).pack(pady=20)

        combo_station = ctk.CTkComboBox(popup, values=list(REAL_STATIONS.keys()), width=420, font=("Montserrat", 12),
                                        fg_color=SKQ_PANEL_LIGHT, border_color="#E0E0E0", button_color=SKQ_BLUE, text_color=SKQ_TEXT_BLACK)
        combo_station.pack(pady=5)

        def fetch_live_data():
            selected = combo_station.get()
            lat, lon = REAL_STATIONS[selected]

            try:
                aq_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=pm2_5"
                live_pm25 = requests.get(aq_url).json()['current']['pm2_5']

                w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=relative_humidity_2m"
                live_hum = requests.get(w_url).json()['current']['relative_humidity_2m']

                self.entry_pm25.delete(0, 'end'); self.entry_pm25.insert(0, str(live_pm25))
                self.entry_hum.delete(0, 'end'); self.entry_hum.insert(0, str(live_hum))
                self.entry_co2.delete(0, 'end'); self.entry_co2.insert(0, "415.0") 
                self.combo_vent.set("Open") 

                popup.destroy()
                messagebox.showinfo("SKQ Analytics", f"✅ Đã tải cấu hình vệ tinh:\n\n{selected}\n\n💨 PM2.5: {live_pm25} µg/m³\n💧 Độ ẩm: {live_hum}%")

            except Exception as e:
                messagebox.showerror("Lỗi kết nối", f"Mất tín hiệu vệ tinh: {e}")
                popup.destroy()

        # Nút nhấn dùng Navy và tích hợp logo icon trắng nhỏ
        if self.img_icon_white:
            ctk.CTkButton(popup, text=" KẾT NỐI VÀ TẢI XUỐNG", font=("Montserrat", 13, "bold"), height=40,
                          fg_color=SKQ_BTN_DARK, hover_color=SKQ_BTN_DARK_HOVER, image=self.img_icon_white, compound="left",
                          command=fetch_live_data).pack(pady=20)
        else:
            ctk.CTkButton(popup, text="⬇️ KẾT NỐI VÀ TẢI XUỐNG", font=("Montserrat", 13, "bold"), height=40,
                          fg_color=SKQ_BTN_DARK, hover_color=SKQ_BTN_DARK_HOVER,
                          command=fetch_live_data).pack(pady=20)

if __name__ == "__main__":
    app = AirClassifyApp()
    # Khởi chạy màn hình bên phải với cờ is_initial=True để hiện mockup TRẮNG
    app.build_right_panel(SKQ_TEXT_GREY, "READY", is_initial=True)  # <-- Sửa chỗ này nè
    app.mainloop()