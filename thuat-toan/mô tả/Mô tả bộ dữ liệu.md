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

bo 3
Completed Orders On Time: 3, Total Shifts: 7, Total Cost: 114097.5
Completed Orders On Time: 3, Total Shifts: 8, Total Cost: 112403.5
Completed Orders On Time: 3, Total Shifts: 8, Total Cost: 111303.5
Completed Orders On Time: 3, Total Shifts: 8, Total Cost: 112733.5
Completed Orders On Time: 3, Total Shifts: 7, Total Cost: 109703.0
Completed Orders On Time: 3, Total Shifts: 8, Total Cost: 110528.0
Completed Orders On Time: 3, Total Shifts: 8, Total Cost: 108405.0
Completed Orders On Time: 3, Total Shifts: 7, Total Cost: 116055.5
Completed Orders On Time: 3, Total Shifts: 7, Total Cost: 112497.0
Completed Orders On Time: 3, Total Shifts: 8, Total Cost: 111771.0
Completed Orders On Time: 3, Total Shifts: 7, Total Cost: 111826.0
Completed Orders On Time: 3, Total Shifts: 8, Total Cost: 110286.0
Completed Orders On Time: 3, Total Shifts: 8, Total Cost: 110775.5
Completed Orders On Time: 3, Total Shifts: 8, Total Cost: 111287.0
Completed Orders On Time: 3, Total Shifts: 8, Total Cost: 111259.5
Completed Orders On Time: 3, Total Shifts: 8, Total Cost: 111980.0
Completed Orders On Time: 3, Total Shifts: 8, Total Cost: 110929.5
Completed Orders On Time: 3, Total Shifts: 7, Total Cost: 112876.5
Completed Orders On Time: 3, Total Shifts: 8, Total Cost: 112508.0
Completed Orders On Time: 3, Total Shifts: 7, Total Cost: 113311.0
Completed Orders On Time: 3, Total Shifts: 8, Total Cost: 110082.5
Completed Orders On Time: 3, Total Shifts: 8, Total Cost: 109043.0
Completed Orders On Time: 3, Total Shifts: 7, Total Cost: 116143.5
Completed Orders On Time: 3, Total Shifts: 8, Total Cost: 111496.0
Completed Orders On Time: 3, Total Shifts: 8, Total Cost: 109686.5
Completed Orders On Time: 3, Total Shifts: 7, Total Cost: 112711.5
Completed Orders On Time: 3, Total Shifts: 7, Total Cost: 111688.5
Completed Orders On Time: 3, Total Shifts: 7, Total Cost: 111100.0
Completed Orders On Time: 3, Total Shifts: 7, Total Cost: 112161.5
Completed Orders On Time: 3, Total Shifts: 8, Total Cost: 110088.0
Thời gian thực thi thuật toán: 71.77 giây
Dữ liệu đã được ghi vào file ./out/best_solution.json
Tất cả công đoạn đã được ghi vào file ./out/schedule.json
Tối ưu: (3, 7, 109703.0)
anh may
![alt text](image-10.png)

anh nv
![alt text](image-11.png)

bo 4
Completed Orders On Time: 4, Total Shifts: 12, Total Cost: 191812.5
Completed Orders On Time: 4, Total Shifts: 12, Total Cost: 187324.5
Completed Orders On Time: 4, Total Shifts: 13, Total Cost: 188303.5
Completed Orders On Time: 4, Total Shifts: 13, Total Cost: 185482.0
Completed Orders On Time: 4, Total Shifts: 12, Total Cost: 189057.0
Completed Orders On Time: 4, Total Shifts: 12, Total Cost: 194133.5
Completed Orders On Time: 4, Total Shifts: 12, Total Cost: 188006.5
Completed Orders On Time: 4, Total Shifts: 13, Total Cost: 187913.0
Completed Orders On Time: 4, Total Shifts: 13, Total Cost: 186109.0
Completed Orders On Time: 4, Total Shifts: 12, Total Cost: 188738.0
Completed Orders On Time: 4, Total Shifts: 12, Total Cost: 189684.0
Completed Orders On Time: 4, Total Shifts: 13, Total Cost: 185493.0
Completed Orders On Time: 4, Total Shifts: 12, Total Cost: 195090.5
Completed Orders On Time: 4, Total Shifts: 12, Total Cost: 187907.5
Completed Orders On Time: 4, Total Shifts: 12, Total Cost: 191988.5
Completed Orders On Time: 4, Total Shifts: 12, Total Cost: 194216.0
Completed Orders On Time: 4, Total Shifts: 13, Total Cost: 187885.5
Completed Orders On Time: 4, Total Shifts: 12, Total Cost: 190701.5
Completed Orders On Time: 4, Total Shifts: 13, Total Cost: 187594.0
Completed Orders On Time: 4, Total Shifts: 13, Total Cost: 186934.0
Completed Orders On Time: 4, Total Shifts: 12, Total Cost: 185372.0
Completed Orders On Time: 4, Total Shifts: 12, Total Cost: 193407.5
Completed Orders On Time: 4, Total Shifts: 13, Total Cost: 188457.5
Completed Orders On Time: 4, Total Shifts: 13, Total Cost: 184338.0
Completed Orders On Time: 4, Total Shifts: 13, Total Cost: 188001.0
Completed Orders On Time: 4, Total Shifts: 12, Total Cost: 184167.5
Completed Orders On Time: 4, Total Shifts: 13, Total Cost: 186340.0
Completed Orders On Time: 4, Total Shifts: 12, Total Cost: 193182.0
Completed Orders On Time: 4, Total Shifts: 13, Total Cost: 188897.5
Completed Orders On Time: 4, Total Shifts: 12, Total Cost: 189150.5
Thời gian thực thi thuật toán: 50.89 giây
Dữ liệu đã được ghi vào file ./out/best_solution.json
Tất cả công đoạn đã được ghi vào file ./out/schedule.json
Tối ưu: (4, 12, 184167.5)

anh nv
![alt text](image-3.png)

anh may
![alt text](image-2.png)

bo 5:
Completed Orders On Time: 5, Total Shifts: 12, Total Cost: 274351.0
Completed Orders On Time: 5, Total Shifts: 13, Total Cost: 276771.0
Completed Orders On Time: 5, Total Shifts: 13, Total Cost: 275280.5
Completed Orders On Time: 5, Total Shifts: 12, Total Cost: 275572.0
Completed Orders On Time: 5, Total Shifts: 13, Total Cost: 290213.0
Completed Orders On Time: 5, Total Shifts: 12, Total Cost: 267630.0
Completed Orders On Time: 5, Total Shifts: 12, Total Cost: 282161.0
Completed Orders On Time: 5, Total Shifts: 13, Total Cost: 278261.5
Completed Orders On Time: 5, Total Shifts: 13, Total Cost: 271793.5
Completed Orders On Time: 5, Total Shifts: 13, Total Cost: 287391.5
Completed Orders On Time: 5, Total Shifts: 13, Total Cost: 279757.5
Completed Orders On Time: 5, Total Shifts: 13, Total Cost: 283893.5
Completed Orders On Time: 5, Total Shifts: 12, Total Cost: 278993.0
Completed Orders On Time: 5, Total Shifts: 13, Total Cost: 285367.5
Completed Orders On Time: 5, Total Shifts: 13, Total Cost: 285092.5
Completed Orders On Time: 5, Total Shifts: 13, Total Cost: 279812.5
Completed Orders On Time: 5, Total Shifts: 13, Total Cost: 288260.5
Completed Orders On Time: 5, Total Shifts: 13, Total Cost: 274906.5
Completed Orders On Time: 5, Total Shifts: 13, Total Cost: 282623.0
Completed Orders On Time: 5, Total Shifts: 13, Total Cost: 284471.0
Completed Orders On Time: 5, Total Shifts: 13, Total Cost: 282276.5
Completed Orders On Time: 5, Total Shifts: 12, Total Cost: 273740.5
Completed Orders On Time: 5, Total Shifts: 12, Total Cost: 276573.0
Completed Orders On Time: 5, Total Shifts: 14, Total Cost: 273861.5
Completed Orders On Time: 5, Total Shifts: 12, Total Cost: 281512.0
Completed Orders On Time: 5, Total Shifts: 13, Total Cost: 277150.5
Completed Orders On Time: 5, Total Shifts: 13, Total Cost: 273498.5
Completed Orders On Time: 5, Total Shifts: 12, Total Cost: 280324.0
Completed Orders On Time: 5, Total Shifts: 14, Total Cost: 270286.5
Completed Orders On Time: 5, Total Shifts: 12, Total Cost: 280494.5
Thời gian thực thi thuật toán: 96.90 giây
Dữ liệu đã được ghi vào file ./out/best_solution.json
Tất cả công đoạn đã được ghi vào file ./out/schedule.json
Tối ưu: (5, 12, 267630.0)

anh mm
![alt text](image-4.png)

anh nv
![alt text](image-5.png)

bo 6.
Completed Orders On Time: 6, Total Shifts: 29, Total Cost: 386199.0
Completed Orders On Time: 6, Total Shifts: 31, Total Cost: 403128.0
Completed Orders On Time: 6, Total Shifts: 31, Total Cost: 393173.0
Completed Orders On Time: 6, Total Shifts: 32, Total Cost: 384290.5
Completed Orders On Time: 6, Total Shifts: 31, Total Cost: 380792.5
Completed Orders On Time: 6, Total Shifts: 31, Total Cost: 398013.0
Completed Orders On Time: 6, Total Shifts: 26, Total Cost: 398860.0
Completed Orders On Time: 6, Total Shifts: 28, Total Cost: 395070.5
Completed Orders On Time: 6, Total Shifts: 30, Total Cost: 401082.0
Completed Orders On Time: 6, Total Shifts: 30, Total Cost: 389477.0
Completed Orders On Time: 6, Total Shifts: 28, Total Cost: 381584.5
Completed Orders On Time: 6, Total Shifts: 30, Total Cost: 395373.0
Completed Orders On Time: 6, Total Shifts: 29, Total Cost: 394696.5
Completed Orders On Time: 6, Total Shifts: 29, Total Cost: 397749.0
Completed Orders On Time: 6, Total Shifts: 27, Total Cost: 404899.0
Completed Orders On Time: 6, Total Shifts: 32, Total Cost: 385302.5
Completed Orders On Time: 6, Total Shifts: 29, Total Cost: 407577.5
Completed Orders On Time: 6, Total Shifts: 30, Total Cost: 403705.5
Completed Orders On Time: 6, Total Shifts: 30, Total Cost: 398469.5
Completed Orders On Time: 6, Total Shifts: 31, Total Cost: 390175.5
Completed Orders On Time: 6, Total Shifts: 32, Total Cost: 394168.5
Completed Orders On Time: 6, Total Shifts: 30, Total Cost: 387277.0
Completed Orders On Time: 6, Total Shifts: 27, Total Cost: 397969.0
Completed Orders On Time: 6, Total Shifts: 30, Total Cost: 401252.5
Completed Orders On Time: 6, Total Shifts: 29, Total Cost: 390010.5
Completed Orders On Time: 6, Total Shifts: 27, Total Cost: 383504.0
Completed Orders On Time: 6, Total Shifts: 31, Total Cost: 394080.5
Completed Orders On Time: 6, Total Shifts: 31, Total Cost: 397237.5
Completed Orders On Time: 6, Total Shifts: 32, Total Cost: 389339.5
Completed Orders On Time: 6, Total Shifts: 26, Total Cost: 396242.0
Thời gian thực thi thuật toán: 51.11 giây
Dữ liệu đã được ghi vào file ./out/best_solution.json
Tất cả công đoạn đã được ghi vào file ./out/schedule.json
Tối ưu: (6, 26, 396242.0)

anh nv
![alt text](image-7.png)

anh mm
![alt text](image-6.png)

bo 9.
Completed Orders On Time: 9, Total Shifts: 48, Total Cost: 611165.5
Completed Orders On Time: 9, Total Shifts: 49, Total Cost: 600083.0
Completed Orders On Time: 9, Total Shifts: 46, Total Cost: 598235.0
Completed Orders On Time: 9, Total Shifts: 47, Total Cost: 598130.5
Completed Orders On Time: 9, Total Shifts: 51, Total Cost: 598009.5
Completed Orders On Time: 9, Total Shifts: 48, Total Cost: 605154.0
Completed Orders On Time: 9, Total Shifts: 46, Total Cost: 603993.5
Completed Orders On Time: 9, Total Shifts: 53, Total Cost: 606672.0
Completed Orders On Time: 9, Total Shifts: 45, Total Cost: 587449.5
Completed Orders On Time: 9, Total Shifts: 54, Total Cost: 593989.0
Completed Orders On Time: 9, Total Shifts: 43, Total Cost: 593928.5
Completed Orders On Time: 9, Total Shifts: 46, Total Cost: 589149.0
Completed Orders On Time: 9, Total Shifts: 54, Total Cost: 589726.5
Completed Orders On Time: 9, Total Shifts: 48, Total Cost: 601441.5
Completed Orders On Time: 9, Total Shifts: 43, Total Cost: 591783.5
Completed Orders On Time: 9, Total Shifts: 52, Total Cost: 583995.5
Completed Orders On Time: 9, Total Shifts: 43, Total Cost: 594704.0
Completed Orders On Time: 9, Total Shifts: 48, Total Cost: 619751.0
Completed Orders On Time: 9, Total Shifts: 50, Total Cost: 598620.0
Completed Orders On Time: 9, Total Shifts: 49, Total Cost: 596035.0
Completed Orders On Time: 9, Total Shifts: 48, Total Cost: 610786.0
Completed Orders On Time: 9, Total Shifts: 51, Total Cost: 601568.0
Completed Orders On Time: 9, Total Shifts: 52, Total Cost: 615862.5
Completed Orders On Time: 9, Total Shifts: 44, Total Cost: 596623.5
Completed Orders On Time: 9, Total Shifts: 46, Total Cost: 608806.0
Completed Orders On Time: 9, Total Shifts: 49, Total Cost: 594302.5
Completed Orders On Time: 9, Total Shifts: 44, Total Cost: 587031.5
Completed Orders On Time: 9, Total Shifts: 45, Total Cost: 587114.0
Completed Orders On Time: 9, Total Shifts: 42, Total Cost: 600066.5
Completed Orders On Time: 9, Total Shifts: 48, Total Cost: 596563.0
Thời gian thực thi thuật toán: 62.02 giây
Dữ liệu đã được ghi vào file ./out/best_solution.json
Tất cả công đoạn đã được ghi vào file ./out/schedule.json
Tối ưu: (9, 42, 600066.5)

anh nv
![alt text](image-9.png)

anh mm
![alt text](image-8.png)