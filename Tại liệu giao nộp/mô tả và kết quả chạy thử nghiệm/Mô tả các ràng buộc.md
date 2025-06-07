# Ràng buộc của bài toán lập lịch sản xuất đang xét

Thuật toán hiện tại đang xét đến các ràng buộc sau:

## 1. Ràng buộc về nhân viên

-   **Vị trí phù hợp**: Mỗi công đoạn yêu cầu nhân viên có vị trí công việc cụ thể . Nhân viên chỉ có thể được phân công vào các công đoạn phù hợp với vị trí của họ.

-   **Lịch làm việc**: Nhân viên chỉ có thể làm việc trong các ca theo lịch làm việc đã định trước . Mỗi nhân viên chỉ có thể làm việc khi giá trị ca tương ứng là 1.

-   **Không làm việc liên tiếp**: Nhân viên không được phép làm việc trong hai ca liên tiếp.

-   **Không làm nhiều công đoạn cùng lúc**: Trong cùng một ca, nhân viên chỉ có thể làm việc tại một công đoạn.

## 2. Ràng buộc về máy móc

-   **Loại máy phù hợp**: Mỗi công đoạn yêu cầu máy móc có loại cụ thể. Máy móc chỉ có thể được sử dụng trong các công đoạn phù hợp với loại của chúng.

-   **Không sử dụng cùng lúc**: Mỗi máy móc chỉ có thể được sử dụng cho một công đoạn trong cùng một ca.

## 3. Ràng buộc về công đoạn

-   **Thứ tự công đoạn**: Công đoạn chỉ có thể bắt đầu khi tất cả các công đoạn tiên quyết đã hoàn thành.

-   **Yêu cầu tối thiểu**: Mỗi công đoạn cần ít nhất 1 nhân viên và 1 máy móc để hoạt động.

-   **KPI hoàn thành**: Công đoạn chỉ được coi là hoàn thành khi đạt được / vượt ngưỡng các giá trị KPI đề ra.

## 4. Ràng buộc về lệnh sản xuất

-   **Deadline**: Mỗi lệnh sản xuất có thời hạn hoàn thành. Lệnh sản xuất được coi là hoàn thành đúng hạn khi tất cả các công đoạn thuộc lệnh đó hoàn thành trước hoặc đúng deadline.

-   **Hoàn thành toàn bộ**: Một lệnh sản xuất chỉ được coi là hoàn thành khi toàn bộ các công đoạn thuộc lệnh đó đều hoàn thành

## 5. Ràng buộc về thời gian

-   **Số ca mỗi ngày**: Mỗi ngày có tối đa n ca làm việc. (bộ dữ liệu hiện tại đang xét n = 4)

-   **Thời gian ca làm việc**: Mỗi ca làm việc có thời lượng cố định là k giờ.

## 6. Tiêu chí đánh giá (Phần này sẽ được nêu rõ hơn ở Tiêu chí đánh giá giải thuật)

Các giải pháp được đánh giá theo thứ tự ưu tiên sau:

1. **Số lệnh sản xuất hoàn thành đúng hạn**: Tối đa hóa số lượng lệnh sản xuất hoàn thành đúng thời hạn.
2. **Tổng số ca làm việc**: Tối thiểu hóa tổng số ca làm việc cần thiết.
3. **Tổng chi phí**: Tối thiểu hóa tổng chi phí sản xuất (chi phí nhân viên + chi phí máy móc).
