# Mô tả bộ dữ liệu

## I. Cấu trúc bộ dữ liệu

### File 1: input.json

-   **Kiểu file**: JSON
-   **Mô tả file**: Lưu các dữ liệu về lệnh sản xuất, công đoạn sản xuất, nhân viên, máy móc
-   **Input gồm**:
    -   **productionOrders**: danh sách các lệnh sản xuất
        -   `id`: Mã lệnh sản xuất
        -   `name`: Tên lệnh sản xuất
        -   `quantity`: Số lượng cần đạt được
        -   `startDate`: Ngày bắt đầu dự kiến
        -   `endDate`: Ngày kết thúc dự kiến
    -   **operations**: danh sách công đoạn
        -   `id`: Mã công đoạn
        -   `productionOrderId`: Mã lệnh sản xuất
        -   `name`: Tên công đoạn
        -   `requiredMachineType`: Loại máy móc yêu cầu
        -   `requiredPosition`: Vị trí nhân viên yêu cầu
        -   `prevOperation`: Danh sách các công đoạn tiền nhiệm
        -   `kpis`: Danh sách các mục tiêu KPI đặt ra
            -   `id`: Mã KPI
            -   `name`: Tên KPI
            -   `weight`: Trọng số
            -   `value`: Giá trị ngưỡng đặt ra
            -   Hiện tại mỗi công đoạn đang xét có 2 loại KPI chính:
                -   KPI năng suất: số sản phẩm cần hoàn thành đúng hạn
                -   KPI chất lượng: số sản phẩm đạt chuẩn
    -   **assets**: danh sách các máy móc
        -   `id`: Mã máy móc
        -   `name`: Tên máy móc
        -   `machineType`: Loại máy móc
        -   `costPerHour`: Chi phí theo giờ
        -   `productivity`: Hệ số hiệu suất
    -   **workers**: danh sách nhân viên
        -   `id`: Mã nhân viên (ví dụ: W0001)
        -   `name`: Tên nhân viên
        -   `position`: Vị trí nhân viên
        -   `productivityKPI`: Năng suất làm việc trong 1 đơn vị thời gian (\_Lưu ý: 2 tiêu chí productivityKPI và qualityKPI được thiết lập ở đây để đơn giản khi chạy giải thuật, trên thực tế các giá trị này của nhân viên trong mỗi công đoạn là khác nhau)
        -   `qualityKPI`: Chất lượng làm việc
        -   `salaryPerHour`: Lương theo giờ

### File 2: monthly_schedule.json

-   **Kiểu file**: JSON
-   **Mô tả file**: Lưu lịch đục lỗ các ca làm việc của nhân viên (hiện tại: 0 là nhân viên không làm việc ca đó, 1 là nhân viên có thể làm việc ca đó)
-   **Input gồm**: danh lịch ca làm việc của nhân viên theo ngày
    -   `date`: Ngày
    -   `shift_count`: Số ca trong 1 ngày
    -   `work_duration_per_shift`: Thời gian làm việc mỗi ca tính theo giờ
    -   `schedule`: Danh sách các ca và trạng thái mỗi ca của nhân viên
        -   Mã nhân viên: Danh sách trạng thái mỗi

## II. Các tập dữ liệu thử nghiệm

1. Bộ dữ liệu 1
    - 1 lệnh sản xuất, 7 công đoạn
    - Kết quả đầu ra:
2. Bộ dữ liệu 2
3. Bộ dữ liệu 3
4. Bộ dữ liệu 4
5. Bộ dữ liệu 5

Bộ 3 173 mm of 389 160 nhân viên odd 180

Bộ 4 worker 160 mm: 199

Bộ 5 worker: 170 mm: 251

Bộ 6 worker: 180 mm: 303

Bộ 9 180 379
