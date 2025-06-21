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
        -   Mã nhân viên: Danh sách trạng thái mỗi ca

## II. Các tập dữ liệu thử nghiệm

-   Các tập dữ liệu dưới đây đại diện cho các kịch bản thử nghiệm:

Mỗi bộ dữ liệu được thiết kế để kiểm tra khả năng thích ứng của thuật toán trong các điều kiện khác nhau về quy mô và độ phức tạp. Các bộ dữ liệu được tạo ra theo nguyên tắc tăng dần về số lượng lệnh sản xuất, công đoạn, và nguồn lực, giúp đánh giá hiệu suất mở rộng của thuật toán.

    +   Dư thừa tài nguyên: Các bộ dữ liệu này có số lượng máy móc và nhân viên nhiều hơn so với nhu cầu thực tế của các công đoạn, giúp kiểm tra khả năng tối ưu chi phí của thuật toán khi có nhiều lựa chọn. Bộ dữ liệu 1, 2, 3 nằm trong nhóm này, với tỷ lệ máy móc/công đoạn cao (>5).
    +   Thiếu máy móc: Các bộ dữ liệu này mô phỏng tình huống khi doanh nghiệp có đủ nhân viên nhưng thiếu máy móc, buộc thuật toán phải tối ưu việc sử dụng máy móc hiệu quả nhất. Bộ dữ liệu 7 và 8 được thiết kế với số lượng máy móc bị giảm xuống so với bộ 6 (252 và 145 máy so với 379 máy), trong khi giữ nguyên số lượng công đoạn và nhân viên.
    +   Thiếu nhân viên: Các bộ dữ liệu này mô phỏng tình huống khi doanh nghiệp có đủ máy móc nhưng thiếu nhân viên có kỹ năng phù hợp, đòi hỏi thuật toán phải tối ưu hóa việc phân bổ nguồn nhân lực hiếm có. Một số kịch bản trong bộ dữ liệu 4, 5, 6 cũng tập trung vào thách thức này, khi số công đoạn tăng lên đáng kể nhưng số nhân viên không tăng tương ứng.

1. Bộ dữ liệu 1

-   3 lệnh sản xuất, 21 công đoạn, 173 máy móc, 160 nhân viên

2. Bộ dữ liệu 2

-   4 lệnh sản xuất, 28 công đoạn, 190 máy móc, 160 nhân viên

3. Bộ dữ liệu 3

-   5 lệnh sản xuất, 35 công đoạn, 251 máy móc. 170 nhân viên

4. Bộ dữ liệu 4

-   6 lệnh sản xuất, 48 công đoạn, 303 máy móc, 170 nhân viên

5. Bộ dữ liệu 5

-   9 lệnh sản xuất, 63 công đoạn, 379 máy móc, 180 nhân viên

6. Bộ dữ liệu 6

-   18 lệnh sản xuất, 126 công đoạn, 379 máy móc, 180 nhân viên

6. Bộ dữ liệu 7

-   18 lệnh sản xuất, 126 công đoạn, 252 máy móc, 180 nhân viên

6. Bộ dữ liệu 8

-   18 lệnh sản xuất, 126 công đoạn, 145 máy móc, 180 nhân viên

## III. Kết quả chạy thử nghiệm

### Bộ 1

| Giải pháp | Số lệnh hoàn thành đúng hạn | Tổng số ca | Tổng chi phí |
| --------- | --------------------------- | ---------- | ------------ |
| 1         | 3                           | 7          | 114097.5     |
| 2         | 3                           | 8          | 112403.5     |
| 3         | 3                           | 8          | 111303.5     |
| 4         | 3                           | 8          | 112733.5     |
| 5         | 3                           | 7          | 109703.0     |
| 6         | 3                           | 8          | 110528.0     |
| 7         | 3                           | 8          | 108405.0     |
| 8         | 3                           | 7          | 116055.5     |
| 9         | 3                           | 7          | 112497.0     |
| 10        | 3                           | 8          | 111771.0     |
| 11        | 3                           | 7          | 111826.0     |
| 12        | 3                           | 8          | 110286.0     |
| 13        | 3                           | 8          | 110775.5     |
| 14        | 3                           | 8          | 111287.0     |
| 15        | 3                           | 8          | 111259.5     |
| 16        | 3                           | 8          | 111980.0     |
| 17        | 3                           | 8          | 110929.5     |
| 18        | 3                           | 7          | 112876.5     |
| 19        | 3                           | 8          | 112508.0     |
| 20        | 3                           | 7          | 113311.0     |
| 21        | 3                           | 8          | 110082.5     |
| 22        | 3                           | 8          | 109043.0     |
| 23        | 3                           | 7          | 116143.5     |
| 24        | 3                           | 8          | 111496.0     |
| 25        | 3                           | 8          | 109686.5     |
| 26        | 3                           | 7          | 112711.5     |
| 27        | 3                           | 7          | 111688.5     |
| 28        | 3                           | 7          | 111100.0     |
| 29        | 3                           | 7          | 112161.5     |
| 30        | 3                           | 8          | 110088.0     |

-   Lời giải tối ưu nhất: (3, 7, 109703.0)
-   Thời gian thực thi thuật toán: 11.77 giây

![alt text](image-10.png)

![alt text](image-11.png)

> **Nhận xét:** Nguyên nhân chính dẫn đến hiện tượng máy móc và nhân viên nhàn rỗi khi vẫn có công việc trong ca:
>
> -   Công đoạn đã phân bổ hết công việc
> -   Thiếu cân đối nguồn lực: có nhân viên nhưng không đủ máy móc để vận hành
> -   Thiếu cân đối nguồn lực: có máy móc nhưng không có nhân viên phù hợp để vận hành

### Bộ 2

| Giải pháp | Số lệnh hoàn thành đúng hạn | Tổng số ca | Tổng chi phí |
| --------- | --------------------------- | ---------- | ------------ |
| 1         | 4                           | 12         | 191812.5     |
| 2         | 4                           | 12         | 187324.5     |
| 3         | 4                           | 13         | 188303.5     |
| 4         | 4                           | 13         | 185482.0     |
| 5         | 4                           | 12         | 189057.0     |
| 6         | 4                           | 12         | 194133.5     |
| 7         | 4                           | 12         | 188006.5     |
| 8         | 4                           | 13         | 187913.0     |
| 9         | 4                           | 13         | 186109.0     |
| 10        | 4                           | 12         | 188738.0     |
| 11        | 4                           | 12         | 189684.0     |
| 12        | 4                           | 13         | 185493.0     |
| 13        | 4                           | 12         | 195090.5     |
| 14        | 4                           | 12         | 187907.5     |
| 15        | 4                           | 12         | 191988.5     |
| 16        | 4                           | 12         | 194216.0     |
| 17        | 4                           | 13         | 187885.5     |
| 18        | 4                           | 12         | 190701.5     |
| 19        | 4                           | 13         | 187594.0     |
| 20        | 4                           | 13         | 186934.0     |
| 21        | 4                           | 12         | 185372.0     |
| 22        | 4                           | 12         | 193407.5     |
| 23        | 4                           | 13         | 188457.5     |
| 24        | 4                           | 13         | 184338.0     |
| 25        | 4                           | 13         | 188001.0     |
| 26        | 4                           | 12         | 184167.5     |
| 27        | 4                           | 13         | 186340.0     |
| 28        | 4                           | 12         | 193182.0     |
| 29        | 4                           | 13         | 188897.5     |
| 30        | 4                           | 12         | 189150.5     |

-   Thời gian thực thi thuật toán: 20.89 giây
-   Lời giải tối ưu nhất: (4, 12, 184167.5)

![alt text](image-3.png)

![alt text](image-2.png)

### Bộ 3:

| Giải pháp | Số lệnh hoàn thành đúng hạn | Tổng số ca | Tổng chi phí |
| --------- | --------------------------- | ---------- | ------------ |
| 1         | 5                           | 12         | 274351.0     |
| 2         | 5                           | 13         | 276771.0     |
| 3         | 5                           | 13         | 275280.5     |
| 4         | 5                           | 12         | 275572.0     |
| 5         | 5                           | 13         | 290213.0     |
| 6         | 5                           | 12         | 267630.0     |
| 7         | 5                           | 12         | 282161.0     |
| 8         | 5                           | 13         | 278261.5     |
| 9         | 5                           | 13         | 271793.5     |
| 10        | 5                           | 13         | 287391.5     |
| 11        | 5                           | 13         | 279757.5     |
| 12        | 5                           | 13         | 283893.5     |
| 13        | 5                           | 12         | 278993.0     |
| 14        | 5                           | 13         | 285367.5     |
| 15        | 5                           | 13         | 285092.5     |
| 16        | 5                           | 13         | 279812.5     |
| 17        | 5                           | 13         | 288260.5     |
| 18        | 5                           | 13         | 274906.5     |
| 19        | 5                           | 13         | 282623.0     |
| 20        | 5                           | 13         | 284471.0     |
| 21        | 5                           | 13         | 282276.5     |
| 22        | 5                           | 12         | 273740.5     |
| 23        | 5                           | 12         | 276573.0     |
| 24        | 5                           | 14         | 273861.5     |
| 25        | 5                           | 12         | 281512.0     |
| 26        | 5                           | 13         | 277150.5     |
| 27        | 5                           | 13         | 273498.5     |
| 28        | 5                           | 12         | 280324.0     |
| 29        | 5                           | 14         | 270286.5     |
| 30        | 5                           | 12         | 280494.5     |

-   Thời gian thực thi thuật toán: 26.90 giây
-   Lời giải tối ưu nhất: (5, 12, 267630.0)

![alt text](image-4.png)

![alt text](image-5.png)

### Bộ 4:

| Giải pháp | Số lệnh hoàn thành đúng hạn | Tổng số ca | Tổng chi phí |
| --------- | --------------------------- | ---------- | ------------ |
| 1         | 6                           | 29         | 386199.0     |
| 2         | 6                           | 31         | 403128.0     |
| 3         | 6                           | 31         | 393173.0     |
| 4         | 6                           | 32         | 384290.5     |
| 5         | 6                           | 31         | 380792.5     |
| 6         | 6                           | 31         | 398013.0     |
| 7         | 6                           | 26         | 398860.0     |
| 8         | 6                           | 28         | 395070.5     |
| 9         | 6                           | 30         | 401082.0     |
| 10        | 6                           | 30         | 389477.0     |
| 11        | 6                           | 28         | 381584.5     |
| 12        | 6                           | 30         | 395373.0     |
| 13        | 6                           | 29         | 394696.5     |
| 14        | 6                           | 29         | 397749.0     |
| 15        | 6                           | 27         | 404899.0     |
| 16        | 6                           | 32         | 385302.5     |
| 17        | 6                           | 29         | 407577.5     |
| 18        | 6                           | 30         | 403705.5     |
| 19        | 6                           | 30         | 398469.5     |
| 20        | 6                           | 31         | 390175.5     |
| 21        | 6                           | 32         | 394168.5     |
| 22        | 6                           | 30         | 387277.0     |
| 23        | 6                           | 27         | 397969.0     |
| 24        | 6                           | 30         | 401252.5     |
| 25        | 6                           | 29         | 390010.5     |
| 26        | 6                           | 27         | 383504.0     |
| 27        | 6                           | 31         | 394080.5     |
| 28        | 6                           | 31         | 397237.5     |
| 29        | 6                           | 32         | 389339.5     |
| 30        | 6                           | 26         | 396242.0     |

-   Thời gian thực thi thuật toán: 31.11 giây
-   Lời giải tối ưu nhất: (6, 26, 396242.0)

![alt text](image-7.png)

![alt text](image-6.png)

### Bộ 5:

| Giải pháp | Số lệnh hoàn thành đúng hạn | Tổng số ca | Tổng chi phí |
| --------- | --------------------------- | ---------- | ------------ |
| 1         | 9                           | 48         | 611165.5     |
| 2         | 9                           | 49         | 600083.0     |
| 3         | 9                           | 46         | 598235.0     |
| 4         | 9                           | 47         | 598130.5     |
| 5         | 9                           | 51         | 598009.5     |
| 6         | 9                           | 48         | 605154.0     |
| 7         | 9                           | 46         | 603993.5     |
| 8         | 9                           | 53         | 606672.0     |
| 9         | 9                           | 45         | 587449.5     |
| 10        | 9                           | 54         | 593989.0     |
| 11        | 9                           | 43         | 593928.5     |
| 12        | 9                           | 46         | 589149.0     |
| 13        | 9                           | 54         | 589726.5     |
| 14        | 9                           | 48         | 601441.5     |
| 15        | 9                           | 43         | 591783.5     |
| 16        | 9                           | 52         | 583995.5     |
| 17        | 9                           | 43         | 594704.0     |
| 18        | 9                           | 48         | 619751.0     |
| 19        | 9                           | 50         | 598620.0     |
| 20        | 9                           | 49         | 596035.0     |
| 21        | 9                           | 48         | 610786.0     |
| 22        | 9                           | 51         | 601568.0     |
| 23        | 9                           | 52         | 615862.5     |
| 24        | 9                           | 44         | 596623.5     |
| 25        | 9                           | 46         | 608806.0     |
| 26        | 9                           | 49         | 594302.5     |
| 27        | 9                           | 44         | 587031.5     |
| 28        | 9                           | 45         | 587114.0     |
| 29        | 9                           | 42         | 600066.5     |
| 30        | 9                           | 48         | 596563.0     |

-   Thời gian thực thi thuật toán: 36.02 giây
-   Lời giải tối ưu nhất: (9, 42, 600066.5)

![alt text](image-9.png)

![alt text](image-8.png)

### Bộ 6

| Giải pháp | Số lệnh hoàn thành đúng hạn | Tổng số ca | Tổng chi phí |
| --------- | --------------------------- | ---------- | ------------ |
| 1         | 15                          | 85         | 1183633.0    |
| 2         | 17                          | 84         | 1214609.0    |
| 3         | 15                          | 89         | 1193247.0    |
| 4         | 15                          | 94         | 1213685.0    |
| 5         | 15                          | 82         | 1202102.0    |
| 6         | 15                          | 83         | 1204175.5    |
| 7         | 15                          | 87         | 1191140.5    |
| 8         | 15                          | 95         | 1207151.0    |
| 9         | 15                          | 89         | 1188583.0    |
| 10        | 15                          | 82         | 1191360.5    |
| 11        | 15                          | 85         | 1197251.0    |
| 12        | 15                          | 84         | 1212893.0    |
| 13        | 17                          | 80         | 1216825.5    |
| 14        | 15                          | 83         | 1210940.5    |
| 15        | 17                          | 83         | 1182654.0    |
| 16        | 15                          | 87         | 1178353.0    |
| 17        | 15                          | 86         | 1209686.5    |
| 18        | 16                          | 81         | 1184606.5    |
| 19        | 15                          | 83         | 1216165.5    |
| 20        | 15                          | 84         | 1236026.0    |
| 21        | 15                          | 85         | 1199313.5    |
| 22        | 17                          | 80         | 1233930.5    |
| 23        | 15                          | 90         | 1193379.0    |
| 24        | 17                          | 83         | 1216858.5    |
| 25        | 16                          | 81         | 1186795.5    |
| 26        | 16                          | 84         | 1190871.0    |
| 27        | 15                          | 93         | 1186938.5    |
| 28        | 15                          | 89         | 1231004.5    |
| 29        | 15                          | 93         | 1187774.5    |
| 30        | 18                          | 77         | 1217392.0    |

-   Thời gian thực thi thuật toán: 41.63 giây
-   Lời giải tối ưu nhất:(18, 77, 1217392.0)

![alt text](image-12.png)

![alt text](image-13.png)

### Bộ 7

| Giải pháp | Số lệnh hoàn thành đúng hạn | Tổng số ca | Tổng chi phí |
| --------- | --------------------------- | ---------- | ------------ |
| 1         | 17                          | 89         | 1156848.0    |
| 2         | 14                          | 85         | 1133429.0    |
| 3         | 15                          | 101        | 1157453.0    |
| 4         | 14                          | 91         | 1193032.5    |
| 5         | 16                          | 99         | 1212035.0    |
| 6         | 15                          | 96         | 1169976.5    |
| 7         | 16                          | 94         | 1163404.0    |
| 8         | 15                          | 89         | 1178254.0    |
| 9         | 15                          | 94         | 1155654.5    |
| 10        | 16                          | 101        | 1159669.5    |
| 11        | 14                          | 88         | 1152420.5    |
| 12        | 15                          | 96         | 1155330.0    |
| 13        | 14                          | 88         | 1149269.0    |
| 14        | 16                          | 99         | 1142647.0    |
| 15        | 16                          | 96         | 1152789.0    |
| 16        | 18                          | 79         | 1179414.5    |
| 17        | 16                          | 93         | 1166220.0    |
| 18        | 16                          | 90         | 1163723.0    |
| 19        | 15                          | 95         | 1101892.0    |
| 20        | 18                          | 75         | 1180679.5    |
| 21        | 15                          | 90         | 1151903.5    |
| 22        | 14                          | 89         | 1152811.0    |
| 23        | 14                          | 87         | 1161506.5    |
| 24        | 13                          | 89         | 1203801.5    |
| 25        | 15                          | 93         | 1129832.0    |
| 26        | 16                          | 94         | 1162073.0    |
| 27        | 15                          | 90         | 1180410.0    |
| 28        | 15                          | 98         | 1164982.5    |
| 29        | 15                          | 90         | 1167281.5    |
| 30        | 15                          | 112        | 1188132.0    |

-   Lời giải tối ưu nhất: (18, 75, 1180679.5)
-   Lời giải tối ưu nhất: 47.96 giây
-   Nhận xét: khi giảm số lượng máy móc của bộ 6 nhưng vẫn giữ nguyên các đầu vào khác thì chất lượng fitness có vẻ không thay đổi, tuy nhiên tốc độ tính toán có thể thấy chậm hơn, tỷ lệ máy móc rảnh rỗi cũng giảm đi đáng kể.

![alt text](image-16.png)

![alt text](image-17.png)

### Bộ 8

| Giải pháp | Số lệnh hoàn thành đúng hạn | Tổng số ca | Tổng chi phí |
| --------- | --------------------------- | ---------- | ------------ |
| 1         | 17                          | 87         | 1176268.5    |
| 2         | 18                          | 77         | 1194759.5    |
| 3         | 18                          | 69         | 1179854.5    |
| 4         | 18                          | 75         | 1176175.0    |
| 5         | 16                          | 82         | 1181246.0    |
| 6         | 18                          | 79         | 1156166.0    |
| 7         | 18                          | 75         | 1176213.5    |
| 8         | 16                          | 87         | 1182648.5    |
| 9         | 18                          | 80         | 1182835.5    |
| 10        | 18                          | 76         | 1217067.5    |
| 11        | 18                          | 74         | 1178567.5    |
| 12        | 18                          | 73         | 1186174.0    |
| 13        | 18                          | 79         | 1167155.0    |
| 14        | 18                          | 75         | 1156331.0    |
| 15        | 18                          | 78         | 1187026.5    |
| 16        | 17                          | 88         | 1166214.5    |
| 17        | 17                          | 80         | 1168711.5    |
| 18        | 18                          | 78         | 1179029.5    |
| 19        | 17                          | 80         | 1173469.0    |
| 20        | 18                          | 75         | 1194858.5    |
| 21        | 18                          | 77         | 1170807.0    |
| 22        | 18                          | 75         | 1179442.0    |
| 23        | 18                          | 77         | 1183105.0    |
| 24        | 18                          | 78         | 1168299.0    |
| 25        | 17                          | 81         | 1202492.5    |
| 26        | 18                          | 80         | 1176334.5    |
| 27        | 16                          | 83         | 1181790.5    |
| 28        | 18                          | 69         | 1193131.5    |
| 29        | 18                          | 80         | 1174948.5    |
| 30        | 16                          | 85         | 1197916.5    |

-   Lời giải tối ưu nhất: (18, 69, 1179854.5)
-   Thời gian thực thi thuật toán: 60.87 giây
-   Nhận xét: Bộ dữ liệu 8 là kịch bản với số lượng máy móc bị giới hạn (145 máy cho 126 công đoạn). Thời gian thực thi tăng đáng kể (60.87 giây) do thuật toán phải xử lý nhiều ràng buộc hơn trong quá trình tìm kiếm lời giải. Mặc dù vậy, kết quả vẫn đạt được 18 lệnh hoàn thành với số ca tối ưu thấp nhất (69 ca). Đồng dựa vào đồ thị tỷ lệ rảnh của máy móc ta có thể thấy tỷ lệ này đã giảm đáng kể so với bộ 7. Điều này chứng tỏ khi nguồn lực máy móc bị hạn chế, thuật toán đã tập trung vào việc phân bổ hiệu quả hơn, đảm bảo các máy được tận dụng tối đa trong từng ca làm việc.

![alt text](image-20.png)

![alt text](image-21.png)

## IV. Đánh giá kết quả

### Hiệu suất giải thuật

| Bộ dữ liệu | Số lệnh SX | Số công đoạn | Số máy móc | Số nhân viên | Số lệnh hoàn thành | Tối ưu ca | Tổng chi phí | Thời gian chạy (s) |
| ---------- | ---------- | ------------ | ---------- | ------------ | ------------------ | --------- | ------------ | ------------------ |
| Bộ 1       | 3          | 21           | 173        | 160          | 3                  | 7         | 109,703.0    | 11.77              |
| Bộ 2       | 4          | 28           | 190        | 160          | 4                  | 12        | 184,167.5    | 20.89              |
| Bộ 3       | 5          | 35           | 251        | 170          | 5                  | 12        | 267,630.0    | 26.90              |
| Bộ 4       | 6          | 48           | 303        | 180          | 6                  | 26        | 396,242.0    | 31.11              |
| Bộ 5       | 9          | 63           | 379        | 180          | 9                  | 42        | 600,066.5    | 36.02              |
| Bộ 6       | 18         | 126          | 379        | 180          | 18                 | 77        | 1217392.0    | 41.63              |
| Bộ 7       | 18         | 126          | 252        | 180          | 17                 | 75        | 1180679.5    | 47.96              |
| Bộ 8       | 18         | 126          | 145        | 180          | 18                 | 69        | 1179854.5    | 60.87              |

### Nhận xét

-   Qua các bộ dữ liệu ta có thể thấy, tùy vào mỗi lần chạy cho ra kết quả fitness khác nhau
-   Thời gian thực hiện qua các bộ dữ liệu có số lượng công đoạn lớn có cùng tập nhân viên, máy móc với bộ dữ liệu có số lượng công đoạn vừa là không đáng kể vì độ phức tạp về thời gian chủ yếu phụ thuộc vào số lượng nguồn lực (nhân viên, máy móc)
