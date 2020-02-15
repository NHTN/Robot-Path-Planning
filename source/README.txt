	Hướng dẫn cài đặt và chạy chương trình RobotPathFinding.py để tìm đường đi ngắn nhất cho robot trên ma trận chữ nhật.

__________________________________________________________________________________________

Step 1: Cài đặt thư viện matplotlib với câu lệnh sau:
	python -m pip install -U pip
	python -m pip install -U matplotlib

Step 2: Khởi tạo file input.txt chứa dữ liệu đầu vào theo format:
- Dòng đầu là giới hạn của không gian, được mô tả lần lượt bởi kích thước ngang, kích thước dọc.
- Dòng thức hai lần lượt là tọa độ điểm bắt đầu, tọa đọa điểm kết thúc và tập hợp các điểm đón (nếu có). 
- Dòng thứ ba là số lượng đa giác có trong không gian.
- Các dòng tiếp theo, mỗi dòng chứa một đa giác theo quy tắc: 
	+ Đa giác là tập hợp các điểm kế nhau theo chiều kim đồng hồ. Điểm cuối cùng sẽ được hiểu ngầm là sẽ được nối đến điểm đầu tiên để tạo thành một đa giác lồi hợp lệ. 
- Mỗi số trong dữ liệu input cách nhau bởi dấu phẩy. 

Step 3: Run chương trình RobotPathFinding.

Step 4: Nhập số nguyên [1, 4] để chọn thuật toán muốn hiện thực.
- 1. BFS 
- 2. UCS
- 3. A star
- 4. Giải thuật di truyền để tìm đường đi ngắn nhất với tập điểm đón

Step 5. Chương trình sẽ hiển thị chi phí đường đi trên màn hình console và biểu diễn đường đi và ma trận trực quan.



------------------------------------------------------------------------------------------



