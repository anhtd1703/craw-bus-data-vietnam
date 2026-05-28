import csv
import json
import os

# 1. DỮ LIỆU JSON MỚI BẠN MUỐN NẠP THÊM (Ví dụ minh họa trạm mới và trạm cũ trùng)
raw_json = """
[
    {
        "AddressNo": "",
        "Code": "A26",
        "Lat": "20.98365",
        "Lng": "105.86335",
        "Name": "(A) Mai \u0110\u1ed9ng 26",
        "Routes": "26,26",
        "Search": "",
        "Status": "",
        "StopID": "1001638",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "831",
        "Lat": "20.984739303589",
        "Lng": "105.86377716065",
        "Name": "C\u00f4ng ty da gi\u1ea7y H\u00e0 N\u1ed9i - 441 Nguy\u1ec5n Tam Trinh",
        "Routes": "26,30,38,42",
        "Search": "",
        "Status": "",
        "StopID": "100793",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "832",
        "Lat": "20.98886680603",
        "Lng": "105.86332702637",
        "Name": "251-253 Nguy\u1ec5n Tam Trinh",
        "Routes": "26,30,38,42",
        "Search": "",
        "Status": "",
        "StopID": "100794",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "04",
        "Lat": "20.994079589844",
        "Lng": "105.86274719238",
        "Name": "89 Nguy\u1ec5n Tam Trinh",
        "Routes": "04,26,30,38,42",
        "Search": "",
        "Status": "",
        "StopID": "100795",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "04",
        "Lat": "20.997272491455",
        "Lng": "105.86196899414",
        "Name": "\u0110\u1ed1i di\u1ec7n 346 Kim Ng\u01b0u - (Ng\u00e3 4 Kim Ng\u01b0u - Minh Khai)",
        "Routes": "04,26,30,42",
        "Search": "",
        "Status": "",
        "StopID": "1002688",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "04",
        "Lat": "21.002075195312",
        "Lng": "105.86148071289",
        "Name": "\u0110\u1ed1i di\u1ec7n T\u1eadp th\u1ec3 E6 Qu\u1ef3nh Mai - Kim Ng\u01b0u",
        "Routes": "04,26,30,42",
        "Search": "",
        "Status": "",
        "StopID": "1002689",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "1226",
        "Lat": "21.002916666667",
        "Lng": "105.85923333333",
        "Name": "B\u1ec7nh vi\u1ec7n Thanh Nh\u00e0n - 42 Thanh Nh\u00e0n",
        "Routes": "26,51",
        "Search": "",
        "Status": "",
        "StopID": "1001185",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "1227",
        "Lat": "21.003005981445",
        "Lng": "105.85321044922",
        "Name": "G\u1ea7n chung c\u01b0 A3B (s\u1ed1 92) Thanh Nh\u00e0n",
        "Routes": "18,26",
        "Search": "",
        "Status": "",
        "StopID": "1001186",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "606",
        "Lat": "21.002851486206",
        "Lng": "105.8475189209",
        "Name": "Qua Vi\u1ec7n tin h\u1ecdc ph\u00e1p ng\u1eef 20m - L\u00ea Thanh Ngh\u1ecb",
        "Routes": "08,18,23,26,31",
        "Search": "",
        "Status": "",
        "StopID": "100570",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "607",
        "Lat": "21.001914978027",
        "Lng": "105.84419250488",
        "Name": "170 - 172 L\u00ea Thanh Ngh\u1ecb",
        "Routes": "23,26",
        "Search": "",
        "Status": "",
        "StopID": "100571",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "431",
        "Lat": "21.004522323608",
        "Lng": "105.84154510498",
        "Name": "17 Gi\u1ea3i Ph\u00f3ng - Bi\u1ec3n b\u00e1o s\u1ed1 1",
        "Routes": "03B,21A,21B,26,41",
        "Search": "",
        "Status": "",
        "StopID": "100395",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "913",
        "Lat": "21.009742736816",
        "Lng": "105.83541870117",
        "Name": "101A2 TT Trung T\u1ef1 - Ph\u1ea1m Ng\u1ecdc Th\u1ea1ch",
        "Routes": "21A,21B,26,35A,44,51",
        "Search": "",
        "Status": "",
        "StopID": "100875",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "914",
        "Lat": "21.007858276367",
        "Lng": "105.833152771",
        "Name": "104 C1 T\u1eadp th\u1ec3 Trung T\u1ef1 - Ph\u1ea1m Ng\u1ecdc Th\u1ea1ch",
        "Routes": "21A,21B,26,35A,44,51",
        "Search": "",
        "Status": "",
        "StopID": "100876",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "12",
        "Lat": "21.007392883301",
        "Lng": "105.82864379883",
        "Name": "C\u00f4ng ty in th\u01b0\u01a1ng m\u1ea1i & d\u1ecbch v\u1ee5 ng\u00e2n h\u00e0ng - S\u1ed110 Ch\u00f9a B\u1ed9c",
        "Routes": "12,18,21A,21B,23,26,35A,44,51",
        "Search": "",
        "Status": "",
        "StopID": "100127",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "12",
        "Lat": "21.00986289978",
        "Lng": "105.8233795166",
        "Name": "2 Th\u00e1i H\u00e0",
        "Routes": "12,26,35A,84",
        "Search": "",
        "Status": "",
        "StopID": "1001173",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "12",
        "Lat": "21.013072967529",
        "Lng": "105.81997680664",
        "Name": "176 Th\u00e1i H\u00e0",
        "Routes": "12,26,35A,84",
        "Search": "",
        "Status": "",
        "StopID": "1001174",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "12",
        "Lat": "21.016067504883",
        "Lng": "105.81583404541",
        "Name": "R\u1ea1p chi\u1ebfu phim Qu\u1ed1c Gia - Th\u00e1i H\u00e0",
        "Routes": "12,26,30,35A,50",
        "Search": "",
        "Status": "",
        "StopID": "1001175",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "500",
        "Lat": "21.017017364502",
        "Lng": "105.81423187256",
        "Name": "\u0110\u1ed1i di\u1ec7n \u0110\u00e0i Truy\u1ec1n h\u00ecnh H\u00e0 N\u1ed9i",
        "Routes": "09,12,26,35A",
        "Search": "",
        "Status": "",
        "StopID": "100464",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "501",
        "Lat": "21.019468307495",
        "Lng": "105.80910491943",
        "Name": "20 Hu\u1ef3nh Th\u00fac Kh\u00e1ng",
        "Routes": "09,12,26,35A",
        "Search": "",
        "Status": "",
        "StopID": "100465",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "770",
        "Lat": "21.021419525146",
        "Lng": "105.80936431885",
        "Name": "89 Nguy\u1ec5n Ch\u00ed Thanh - KTX \u0110\u1ea1i h\u1ecdc Lu\u1eadt",
        "Routes": "09,12,26,27",
        "Search": "",
        "Status": "",
        "StopID": "100733",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "12",
        "Lat": "21.023818969727",
        "Lng": "105.81076049805",
        "Name": "73 Nguy\u1ec5n Ch\u00ed Thanh - \u0110\u1ed1i di\u1ec7n Kh\u00e1ch s\u1ea1n B\u1ea3o S\u01a1n",
        "Routes": "12,26,27",
        "Search": "",
        "Status": "",
        "StopID": "100734",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "180",
        "Lat": "21.02730178833",
        "Lng": "105.80941009522",
        "Name": "Ng\u00f5 1072 \u0110\u00ea La Th\u00e0nh",
        "Routes": "26,49",
        "Search": "",
        "Status": "",
        "StopID": "100174",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "181",
        "Lat": "21.028392791748",
        "Lng": "105.80609893799",
        "Name": "1144 \u0110\u00ea La Th\u00e0nh (\u0111\u1ed1i di\u1ec7n 191 - \u0110SQ Nga)",
        "Routes": "26,49",
        "Search": "",
        "Status": "",
        "StopID": "100175",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "2034",
        "Lat": "21.029136657715",
        "Lng": "105.80386352539",
        "Name": "CV Th\u1ee7 L\u1ec7 (C\u1ed9t 2)",
        "Routes": "07,20A,20B,24,26,49,55A",
        "Search": "",
        "Status": "",
        "StopID": "1002034",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "114",
        "Lat": "21.031717300415",
        "Lng": "105.79975891113",
        "Name": "106-108 C\u1ea7u Gi\u1ea5y - Kh\u00e1ch s\u1ea1n C\u1ea7u Gi\u1ea5y",
        "Routes": "07,16,20A,20B,26,27,28,32,34,49",
        "Search": "",
        "Status": "",
        "StopID": "100112",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "115",
        "Lat": "21.034324645996",
        "Lng": "105.79648590088",
        "Name": "250-252 C\u1ea7u Gi\u1ea5y",
        "Routes": "16,20A,20B,26,27,28,32,34,49",
        "Search": "",
        "Status": "",
        "StopID": "100113",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "2309",
        "Lat": "21.035882949829",
        "Lng": "105.79191589356",
        "Name": "H\u00e8 tr\u01b0\u1edbc s\u1ed1 370 C\u1ea7u Gi\u1ea5y - Nh\u00e0 kh\u00e1ch qu\u1ed1c t\u1ebf B\u1ed9 C\u00f4ng an",
        "Routes": "16,20A,20B,26,32,34",
        "Search": "",
        "Status": "",
        "StopID": "1002309",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "116",
        "Lat": "21.03652381897",
        "Lng": "105.78904724121",
        "Name": "H\u1ecdc vi\u1ec7n B\u00e1o ch\u00ed v\u00e0 Tuy\u00ean truy\u1ec1n - 36 Xu\u00e2n Th\u1ee7y",
        "Routes": "16,20A,20B,26,32,34",
        "Search": "",
        "Status": "",
        "StopID": "100114",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "1454",
        "Lat": "21.036729812622",
        "Lng": "105.78411102295",
        "Name": "G\u1ea7n nh\u00e0 s\u00e1ch S\u01b0 ph\u1ea1m (\u0110\u1ea1i h\u1ecdc S\u01b0 ph\u1ea1m H\u00e0 N\u1ed9i) - 136 Xu\u00e2n Th\u1ee7y",
        "Routes": "16,20A,20B,26,32,34",
        "Search": "",
        "Status": "",
        "StopID": "1001412",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "2023",
        "Lat": "21.037563323975",
        "Lng": "105.77500152588",
        "Name": "\u0110\u1ed1i di\u1ec7n \u0110H Th\u01b0\u01a1ng M\u1ea1i - 6 H\u1ed3 T\u00f9ng M\u1eadu (C\u1ed9t 2)",
        "Routes": "13,26,49",
        "Search": "",
        "Status": "",
        "StopID": "1002023",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "593",
        "Lat": "21.036010742188",
        "Lng": "105.77070617676",
        "Name": "Trung \u01b0\u01a1ng H\u1ed9i KHH Gia \u0111\u00ecnh Vi\u1ec7t Nam - 2 L\u00ea \u0110\u1ee9c Th\u1ecd",
        "Routes": "26,49",
        "Search": "",
        "Status": "",
        "StopID": "100557",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "594",
        "Lat": "21.031633333333",
        "Lng": "105.7693",
        "Name": "Nh\u00e0 CT2B K\u0110T M\u1ef9 \u0110\u00ecnh - L\u00ea \u0110\u1ee9c Th\u1ecd",
        "Routes": "26",
        "Search": "",
        "Status": "",
        "StopID": "100558",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "597",
        "Lat": "21.025169372559",
        "Lng": "105.76695251465",
        "Name": "\u0110\u1ed1i di\u1ec7n \u0111\u01b0\u1eddng v\u00e0o Tr\u01b0\u1eddng C\u0110 ngh\u1ec1 Tr\u1ea7n H\u01b0ng \u0110\u1ea1o - L\u00ea \u0110\u1ee9c Th\u1ecd",
        "Routes": "26,84",
        "Search": "",
        "Status": "",
        "StopID": "100561",
        "StopType": "",
        "Street": ""
    },
    {
        "AddressNo": "",
        "Code": "B26",
        "Lat": "21.019466400146",
        "Lng": "105.7673034668",
        "Name": "(B) S\u00e2n v\u1eadn \u0111\u1ed9ng Qu\u1ed1c Gia 26",
        "Routes": "26,26",
        "Search": "",
        "Status": "",
        "StopID": "1001708",
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