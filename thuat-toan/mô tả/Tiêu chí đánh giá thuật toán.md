# Tiêu chí đánh giá thuật toán

Thuật toán lập lịch sản xuất trong bài toán này được đánh giá dựa trên ba tiêu chí chính, được sắp xếp theo thứ tự ưu tiên:

## 1. Số lệnh sản xuất hoàn thành đúng hạn

-   **Mục tiêu**: Tối đa hóa (càng nhiều càng tốt)
-   **Mô tả**: Đây là tiêu chí quan trọng nhất. Một lệnh sản xuất được coi là hoàn thành đúng hạn khi tất cả các công đoạn liên quan đến lệnh đó đều hoàn thành trước hoặc đúng ngày kết thúc (end_date) của lệnh. Một công đoạn được coi là hoàn thành nếu tất cả các chỉ tiêu KPI của công đoạn đó hoàn thành >= chỉ tiêu đề ra.
-   **Ảnh hưởng**: Giải pháp có nhiều lệnh hoàn thành đúng hạn sẽ được ưu tiên hơn, bất kể các tiêu chí khác.

## 2. Tổng số ca làm việc

-   **Mục tiêu**: Tối thiểu hóa (càng ít càng tốt)
-   **Mô tả**: Đây là tiêu chí thứ hai được xem xét. Tổng số ca làm việc đại diện cho tổng số ca sản xuất cần thiết để hoàn thành tất cả các lệnh sản xuất. Mỗi ngày có tối đa n ca. (Hiện tại các bộ dữ liệu đang xét đều mặc định 4 ca)
-   **Ảnh hưởng**: Khi hai giải pháp có cùng số lệnh hoàn thành đúng hạn, giải pháp có ít ca làm việc hơn sẽ được ưu tiên.

## 3. Tổng chi phí sản xuất

-   **Mục tiêu**: Tối thiểu hóa (càng thấp càng tốt)
-   **Mô tả**: Đây là tiêu chí cuối cùng. Tổng chi phí bao gồm chi phí nhân công và chi phí vận hành máy móc cho thực hiện tất cả các lệnh.
-   **Ảnh hưởng**: Khi hai giải pháp có cùng số lệnh hoàn thành đúng hạn và cùng số ca làm việc, giải pháp có chi phí thấp hơn sẽ được ưu tiên.

## Cách so sánh giải pháp

Khi so sánh hai giải pháp, thuật toán sẽ:

1. Trước tiên so sánh số lệnh hoàn thành đúng hạn (càng nhiều càng tốt)
2. Nếu bằng nhau, so sánh tổng số ca làm việc (càng ít càng tốt)
3. Nếu vẫn bằng nhau, so sánh tổng chi phí sản xuất (càng thấp càng tốt)

## Ảnh hưởng đến các chiến lược tối ưu hóa

-   **Phân bổ nguồn lực**: Thuật toán ưu tiên phân bổ nhân viên có năng suất và chất lượng cao cho các công đoạn thuộc lệnh sản xuất gần deadline.
-   **Lập lịch**: Các công đoạn được lập lịch theo thứ tự ưu tiên dựa trên deadline và các phụ thuộc giữa công đoạn.
-   **Tìm kiếm cục bộ**: Tối ưu hóa cục bộ tập trung vào việc cải thiện phân bổ nhân viên và máy móc để giảm thời gian hoàn thành và chi phí.
