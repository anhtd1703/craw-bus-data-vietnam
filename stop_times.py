import csv
import os
from datetime import datetime, timedelta

# 1. CẤU HÌNH THAM SỐ
TRIPS_FILE = "./HaNoi_Bus_GTFS/trips.txt"
STOPS_FILE = "./HaNoi_Bus_GTFS/stops.txt"
OUTPUT_FILE = "./HaNoi_Bus_GTFS/stop_times.txt"
TIME_BETWEEN_STOPS_MINUTES = 2  # Khoảng thời gian trung bình giữa 2 trạm (2 phút)

print("[*] Đang đọc cấu trúc danh sách trạm dừng từ stops.txt...")

# 2. ĐỌC DANH SÁCH TRẠM VÀ PHÂN CHIA THEO CHIỀU (GIẢ ĐỊNH THEO THỨ TỰ TRONG FILE)
# Chiều đi (0): Từ trạm đầu đến trạm cuối trong file stops.txt
# Chiều về (1): Đảo ngược lại danh sách trạm của chiều đi
stops_direction_0 = []

with open(STOPS_FILE, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader, None)
    for row in reader:
        if row:
            stops_direction_0.append(row[0])  # row[0] là stop_id

stops_direction_1 = list(reversed(stops_direction_0))

print(f"[+] Chiều đi (Direction 0) có: {len(stops_direction_0)} trạm.")
print(f"[+] Chiều về (Direction 1) có: {len(stops_direction_1)} trạm.")

# 3. ĐỌC DANH SÁCH CHUYẾN XE (TRIPS) ĐÃ SINH Ở BƯỚC TRƯỚC
trips_list = []
with open(TRIPS_FILE, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader, None)
    for row in reader:
        if row:
            # Lưu lại: route_id, service_id, trip_id, direction_id
            trips_list.append(row)

# 4. KHỞI TẠO HOẶC KIỂM TRA FILE STOP_TIMES.TXT CŨ ĐỂ TRÁNH TRÙNG
existing_stop_times = set()
file_exists = os.path.exists(OUTPUT_FILE) and os.path.getsize(OUTPUT_FILE) > 0

if file_exists:
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if row:
                # Khóa chống trùng kết hợp giữa trip_id và stop_sequence
                existing_stop_times.add((row[0], row[4])) 
    print(f"[*] Phát hiện file stop_times.txt cũ đang có dữ liệu.")
else:
    print("[*] Sẽ tạo mới file stop_times.txt hoàn toàn.")

# 5. TIẾN HÀNH TÍNH TOÁN VÀ GHI DỮ LIỆU CHÍNH XÁC
count_rows = 0
count_skipped = 0

with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    
    if not file_exists:
        writer.writerow(["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence"])
        
    for trip in trips_list:
        route_id, service_id, trip_id, direction_id = trip
        
        # Chọn danh sách trạm tương ứng với chiều của chuyến xe đó
        current_stops = stops_direction_0 if direction_id == "0" else stops_direction_1
        
        # Lấy giờ xuất bến từ phần đuôi của trip_id (Ví dụ: TRIP_R01_DIR0_0500 -> lấy 0500)
        start_time_str = trip_id.split("_")[-1] 
        start_time = datetime.strptime(start_time_str, "%H%M")
        
        # Duyệt qua từng trạm trong hành trình của chuyến xe
        for index, stop_id in enumerate(current_stops):
            stop_sequence = str(index + 1)
            
            # Logic kiểm tra trùng dòng
            if (trip_id, stop_sequence) in existing_stop_times:
                count_skipped += 1
                continue
            
            # Tính toán thời gian tịnh tiến bằng cách cộng dồn phút
            minutes_to_add = index * TIME_BETWEEN_STOPS_MINUTES
            stop_time = start_time + timedelta(minutes=minutes_to_add)
            time_formatted = stop_time.strftime("%H:%M:%S") # Chuẩn GTFS bắt buộc có cả giây HH:MM:SS
            
            # Ghi vào file (Thời gian đến và đi trùng nhau nghĩa là xe dừng đón trả khách chớp nhoáng)
            writer.writerow([trip_id, time_formatted, time_formatted, stop_id, stop_sequence])
            count_rows += 1

print("--- KẾT QUẢ SINH LỊCH TRÌNH CHI TIẾT ---")
print(f"[+] Đã ghi thêm thành công: {count_rows} dòng thời gian dừng trạm.")
print(f"[!] Bỏ qua do trùng lặp: {count_skipped} dòng.")
print(f"[ SUCCESS ] File '{OUTPUT_FILE}' đã hoàn thành đạt chuẩn!")