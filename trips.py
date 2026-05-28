import csv
import os
from datetime import datetime, timedelta

# 1. CẤU HÌNH THÔNG SỐ CHẠY XE
ROUTE_ID = "R_26"          # Khớp với route_id trong file routes.txt
SERVICE_ID = "SV_DAILY"    # Khớp với service_id trong file calendar.txt

START_TIME = "05:00"       # Giờ mở bến
END_TIME = "22:30"         # Giờ đóng bến
FREQUENCY_MINUTES = 10     # Tần suất: 10 phút/chuyến

OUTPUT_FILE = "./HaNoi_Bus_GTFS/trips.txt"

# Hàm sinh danh sách các mốc thời gian xuất phát cách nhau 10 phút
def generate_departure_times(start_str, end_str, freq_mins):
    times = []
    current_time = datetime.strptime(start_str, "%H:%M")
    end_time = datetime.strptime(end_str, "%H:%M")
    
    while current_time <= end_time:
        times.append(current_time.strftime("%H%M")) # Trả về định dạng HHMM (ví dụ: 0500)
        current_time += timedelta(minutes=freq_mins)
    return times

# Sinh ra các mốc thời gian xuất bến
departure_slots = generate_departure_times(START_TIME, END_TIME, FREQUENCY_MINUTES)

# 2. KHỞI TẠO HOẶC ĐỌC FILE CŨ ĐỂ CHỐNG TRÙNG
existing_trips = set()
file_exists = os.path.exists(OUTPUT_FILE) and os.path.getsize(OUTPUT_FILE) > 0

if file_exists:
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if row:
                existing_trips.add(row[2]) # row[2] chính là cột trip_id
    print(f"[*] Phát hiện file trips.txt cũ đang có {len(existing_trips)} chuyến.")
else:
    print("[*] Sẽ tạo mới file trips.txt hoàn toàn.")

# 3. TIẾN HÀNH SINH CHUYẾN TỰ ĐỘNG VÀ GHI VÀO FILE
count_added = 0
count_skipped = 0

with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    
    # Viết tiêu đề chuẩn GTFS nếu file mới tinh
    if not file_exists:
        writer.writerow(["route_id", "service_id", "trip_id", "direction_id"])
        
    # Lặp qua cả 2 chiều: 0 (Chiều đi), 1 (Chiều về)
    for direction in ["0", "1"]:
        for time_slot in departure_slots:
            # Tạo mã trip_id duy nhất dựa trên Tuyến, Chiều và Giờ xuất bến
            trip_id = f"TRIP_{ROUTE_ID}_DIR{direction}_{time_slot}"
            
            # Logic chống trùng
            if trip_id in existing_trips:
                count_skipped += 1
                continue
                
            writer.writerow([ROUTE_ID, SERVICE_ID, trip_id, direction])
            existing_trips.add(trip_id)
            count_added += 1

print("--- KẾT QUẢ SINH CHUYẾN XE ---")
print(f"[+] Đã tự động sinh mới: {count_added} chuyến xe (cho cả chiều đi và về).")
print(f"[!] Bỏ qua do trùng lặp: {count_skipped} chuyến.")
print(f"[ SUCCESS ] Tổng số chuyến xe hiện có trong file: {len(existing_trips)}")