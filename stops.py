import csv
import json
import os

# 1. DỮ LIỆU JSON MỚI BẠN MUỐN NẠP THÊM (Ví dụ minh họa trạm mới và trạm cũ trùng)
raw_json = """
[
    {
        "AddressNo": "",
        "Code": "A2",
        "Lat": "21.023183333333",
        "Lng": "105.86088333333",
        "Name": "(A) Trần Khánh Dư 2",
        "Routes": "02",
        "Search": "",
        "Status": "",
        "StopID": "1001629",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "1318",
        "Lat": "21.018573760986",
        "Lng": "105.86055755615",
        "Name": "Đối diện Bệnh Viện Trung ương Quân đội 108 - Trần Hưng Đạo",
        "Routes": "02,03A,03B,35A,42,43,45,49",
        "Search": "",
        "Status": "",
        "StopID": "1001277",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "2686",
        "Lat": "21.020618438721",
        "Lng": "105.85832214356",
        "Name": "9 Trần Thánh Tông",
        "Routes": "02,18,23,45,49",
        "Search": "",
        "Status": "",
        "StopID": "1002686",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "2792",
        "Lat": "21.023115158081",
        "Lng": "105.85687255859",
        "Name": "Hè cạnh vườn hoa 19-8",
        "Routes": "02",
        "Search": "",
        "Status": "",
        "StopID": "1002792",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "2685",
        "Lat": "21.024074554443",
        "Lng": "105.85358428955",
        "Name": "22B Hai Bà Trưng",
        "Routes": "02,34,40A,40B",
        "Search": "",
        "Status": "",
        "StopID": "1002685",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "448",
        "Lat": "21.025009155273",
        "Lng": "105.85040283203",
        "Name": "48 Hai Bà Trưng - Viện Kiểm Nghiệm thuốc Trung ương",
        "Routes": "02,34,36,40A,40B",
        "Search": "",
        "Status": "",
        "StopID": "100412",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "1365",
        "Lat": "21.026546478271",
        "Lng": "105.8496170044",
        "Name": "6-8 Tràng Thi (Qua ngã 4 Tràng Thi - Lý Quốc Sư)",
        "Routes": "02,09,45",
        "Search": "",
        "Status": "",
        "StopID": "1001324",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "1366",
        "Lat": "21.027383333333",
        "Lng": "105.84665",
        "Name": "Bệnh viện Việt Đức - 40 Tràng Thi",
        "Routes": "02,09,45",
        "Search": "",
        "Status": "",
        "StopID": "1001325",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "186",
        "Lat": "21.029407501221",
        "Lng": "105.84239196777",
        "Name": "12A Điện Biên Phủ",
        "Routes": "02,09,32,34,45",
        "Search": "",
        "Status": "",
        "StopID": "100180",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "1337",
        "Lat": "21.031084060669",
        "Lng": "105.83909606934",
        "Name": "Công viên Lê nin - Đối diện 34 Trần Phú",
        "Routes": "02,23,32,34",
        "Search": "",
        "Status": "",
        "StopID": "1001296",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "127",
        "Lat": "21.031055450439",
        "Lng": "105.8360824585",
        "Name": "Bệnh viện Xanhpon - 12 Chu Văn An",
        "Routes": "02,23,41",
        "Search": "",
        "Status": "",
        "StopID": "100124",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "1287",
        "Lat": "21.027200698852",
        "Lng": "105.83382415772",
        "Name": "92-94 Tôn Đức Thắng",
        "Routes": "02,25,41",
        "Search": "",
        "Status": "",
        "StopID": "1001246",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "1288",
        "Lat": "21.024799346924",
        "Lng": "105.83274078369",
        "Name": "160 Tôn Đức Thắng ",
        "Routes": "02,25,41,49",
        "Search": "",
        "Status": "",
        "StopID": "1001247",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "1289",
        "Lat": "21.020021438599",
        "Lng": "105.83049011231",
        "Name": "276 Tôn Đức Thắng ",
        "Routes": "02,25,41,49",
        "Search": "",
        "Status": "",
        "StopID": "1001248",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "826",
        "Lat": "21.015804290771",
        "Lng": "105.82822418213",
        "Name": "142-144 Nguyễn Lương Bằng",
        "Routes": "01,02,09",
        "Search": "",
        "Status": "",
        "StopID": "100788",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "1207",
        "Lat": "21.011096954346",
        "Lng": "105.82527923584",
        "Name": "Gò Đống Đa - Tây Sơn",
        "Routes": "01,02,09",
        "Search": "",
        "Status": "",
        "StopID": "1001166",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "1208",
        "Lat": "21.007072448731",
        "Lng": "105.82315826416",
        "Name": "290 Tây Sơn",
        "Routes": "01,02,09,18,21A,21B,44,51,84",
        "Search": "",
        "Status": "",
        "StopID": "1001167",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "1473",
        "Lat": "20.99994468689",
        "Lng": "105.81532287598",
        "Name": "94 Nguyễn Trãi",
        "Routes": "01,02,19,21A,21B,27,44",
        "Search": "",
        "Status": "",
        "StopID": "1001431",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "840",
        "Lat": "20.995897293091",
        "Lng": "105.80921936035",
        "Name": "332 Nguyễn Trãi",
        "Routes": "01,02,05,19,21A,21B,27,29,44,44,60B",
        "Search": "",
        "Status": "",
        "StopID": "100802",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "841",
        "Lat": "20.993455886841",
        "Lng": "105.80562591553",
        "Name": "386 Nguyễn Trãi - Cục Sở hữu trí tuệ",
        "Routes": "01,02,05,19,21A,21B,27,29,60A",
        "Search": "",
        "Status": "",
        "StopID": "100803",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "842",
        "Lat": "20.990411758423",
        "Lng": "105.80131530762",
        "Name": "Hè trước Bách hóa Thanh Xuân - đường Nguyễn Trãi",
        "Routes": "01,02,19,21A,21B,27,33,39,78",
        "Search": "",
        "Status": "",
        "StopID": "100804",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "843",
        "Lat": "20.988107681274",
        "Lng": "105.7981338501",
        "Name": "204-206 Nguyễn Trãi ( Gần ngã 3 Nguyễn Trãi - Lương Thế Vinh )",
        "Routes": "01,02,19,21A,21B,27,33,39,78",
        "Search": "",
        "Status": "",
        "StopID": "100805",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "844",
        "Lat": "20.985960006714",
        "Lng": "105.79509735107",
        "Name": "Công ty CP Công trình GT 873 - Nguyễn Trãi",
        "Routes": "01,02,19,21A,21B,27,33,39,78",
        "Search": "",
        "Status": "",
        "StopID": "100806",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "1339",
        "Lat": "20.983469009399",
        "Lng": "105.79164886475",
        "Name": "Cửa hàng bán xe ôtô Hoà Bình - Trần Phú (Hà Đông)",
        "Routes": "01,02,19,21A,21B,27,33,39,78",
        "Search": "",
        "Status": "",
        "StopID": "1001298",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "1340",
        "Lat": "20.980421066284",
        "Lng": "105.78789520264",
        "Name": "Học viện công nghệ bưu chính viễn thông - Trần Phú (Hà Đông)",
        "Routes": "01,02,19,21A,21B,22B,27,33,39,78,85",
        "Search": "",
        "Status": "",
        "StopID": "1001299",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "1341",
        "Lat": "20.979379653931",
        "Lng": "105.7865524292",
        "Name": "Công ty Điện lực TP cơ sở 2 - 100 Trần Phú (Hà Đông)",
        "Routes": "01,02,19,21A,21B,27,33,78,85",
        "Search": "",
        "Status": "",
        "StopID": "1001300",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "1342",
        "Lat": "20.975483333333",
        "Lng": "105.78155",
        "Name": "Khách sạn Sông Nhuệ (148 Trần Phú- Hà Đông)",
        "Routes": "01,02,19,21A,21B,22B,27,33,78",
        "Search": "",
        "Status": "",
        "StopID": "1001301",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "1474",
        "Lat": "20.972476959229",
        "Lng": "105.77758789062",
        "Name": "8 Quang Trung - Siêu thị Hiway",
        "Routes": "01,02,21A,21B,27,33,57,77,78,89",
        "Search": "",
        "Status": "",
        "StopID": "1001432",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "1472",
        "Lat": "20.969570159912",
        "Lng": "105.77397155762",
        "Name": "Chi cục quản lý thị trường Hà Nội - 78 Quang Trung (Hà Đông)",
        "Routes": "01,02,21A,21B,27,33,57,77,78,89",
        "Search": "",
        "Status": "",
        "StopID": "1001430",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "961",
        "Lat": "20.96759223938",
        "Lng": "105.77127075195",
        "Name": "Nhà thi đấu Hà Đông - 182 Quang Trung (Hà Đông)",
        "Routes": "01,02,21A,21B,27,33,57,77,78,89",
        "Search": "",
        "Status": "",
        "StopID": "100923",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "962",
        "Lat": "20.964807510376",
        "Lng": "105.76773834228",
        "Name": "268 Quang Trung - Hà Đông",
        "Routes": "01,02,21A,21B,27,33,37,57,62,77,78,89",
        "Search": "",
        "Status": "",
        "StopID": "100924",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "963",
        "Lat": "20.96201133728",
        "Lng": "105.76430511475",
        "Name": "Đối diện KĐT Văn Phú - 418 Quang Trung (Hà Đông)",
        "Routes": "01,02,21A,21B,27,33,37,57,62,77,78,89",
        "Search": "",
        "Status": "",
        "StopID": "100925",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "1980",
        "Lat": "20.960437774658",
        "Lng": "105.76222991943",
        "Name": "530 - 532 Quang Trung (Hà Đông)",
        "Routes": "01,02,21A,21B,27,33,37,57,62,77,78,89",
        "Search": "",
        "Status": "",
        "StopID": "1001980",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "964",
        "Lat": "20.958114624023",
        "Lng": "105.75917053223",
        "Name": "678 - 680 Quang Trung (Hà Đông)",
        "Routes": "01,02,21A,21B,27,33,37,57,62,77,78,89",
        "Search": "",
        "Status": "",
        "StopID": "100926",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "965",
        "Lat": "20.955003738403",
        "Lng": "105.75498962402",
        "Name": "Showroom ô tô Trường Sơn (đối diện Nissan Hà Đông km 14+600, Quốc lộ 6)",
        "Routes": "01,02,21A,21B,27,33,37,57,62,77,89",
        "Search": "",
        "Status": "",
        "StopID": "100927",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "1178",
        "Lat": "20.951616287231",
        "Lng": "105.75049591065",
        "Name": "Đối diện trường trung cấp kinh tế - Tài chính Hà Nội",
        "Routes": "01,02,21A,21B,27,33,37,57,62,75,77,89",
        "Search": "",
        "Status": "",
        "StopID": "1001138",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "B2",
        "Lat": "20.949649810791",
        "Lng": "105.74723052978",
        "Name": "(B) Bến xe Yên Nghĩa 02",
        "Routes": "02,02",
        "Search": "",
        "Status": "",
        "StopID": "1001699",
        "StopType": "",
        "Street": ""
    }
]
"""

OUTPUT_FILE = "./HaNoi_Bus_GTFS/stops.txt"

# 2. KHỞI TẠO TẬP HỢP ĐỂ LƯU CÁC MÃ TRẠM ĐÃ TỒN TẠI (Dùng set để tìm kiếm siêu nhanh)
existing_ids = set()
file_exists = os.path.exists(OUTPUT_FILE) and os.path.getsize(OUTPUT_FILE) > 0

# 3. LOGIC ĐỌC FILE CŨ ĐỂ KIỂM TRA TRÙNG LẶP
if file_exists:
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)  # Bỏ qua hàng tiêu đề
        for row in reader:
            if row:  # Nếu dòng không rỗng
                existing_ids.add(row[0])  # row[0] chính là cột stop_id
    print(f"[*] Phát hiện file cũ đang có sẵn {len(existing_ids)} trạm dừng.")
else:
    print("[*] File chưa tồn tại hoặc trống. Sẽ tạo mới hoàn toàn.")

# 4. TIẾN HÀNH GHI THÊM (APPEND) VỚI LOGIC CHỐNG TRÙNG
data_list = json.loads(raw_json)
count_added = 0
count_skipped = 0

# Mở file ở chế độ "a" (Append) để ghi tiếp vào cuối file
with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    
    # Nếu file trống trơn/chưa có, tiến hành viết hàng tiêu đề đầu tiên
    if not file_exists:
        writer.writerow(["stop_id", "stop_name", "stop_lat", "stop_lon"])
    
    for item in data_list:
        stop_id = f"ST_{item['StopID']}"
        
        # KIỂM TRA LÀM SẠCH: Nếu id này đã nằm trong danh sách cũ -> BỎ QUA
        if stop_id in existing_ids:
            count_skipped += 1
            continue
            
        stop_name = item['Name'].strip().replace(",", "-")
        stop_lat = item['Lat']
        stop_lon = item['Lng']
        
        # Ghi trạm mới hợp lệ vào cuối file
        writer.writerow([stop_id, stop_name, stop_lat, stop_lon])
        existing_ids.add(stop_id)  # Thêm vào bộ nhớ luôn để tránh trùng ngay trong cùng 1 file JSON mới
        count_added += 1

print("--- KẾT QUẢ XỬ LÝ ---")
print(f"[+] Đã thêm mới thành công: {count_added} trạm.")
print(f"[!] Đã phát hiện và loại bỏ: {count_skipped} trạm bị trùng lặp.")
print(f"[ SUCCESS ] Tổng số trạm hiện tại trong file: {len(existing_ids)}")