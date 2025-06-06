# filepath: d:\Ki_2_nam_4\KPI\tour\models.py
from typing import List, Dict
from datetime import datetime, timedelta
import json


class Worker:
    def __init__(
        self,
        id: str,
        name: str,
        position: str,
        productivity_kpi: int,
        quality_kpi: float,
        salary_per_hour: float,
        schedule: Dict[str, List[int]],
    ):
        self.id = id
        self.name = name
        self.position = position
        self.productivity_kpi = productivity_kpi
        self.quality_kpi = quality_kpi
        self.salary_per_hour = salary_per_hour
        self.schedule = schedule  # Lịch làm việc theo ngày (key: ngày, value: danh sách ca làm việc)

    def get_schedule_by_day(self, day: str) -> List[int]:
        """
        Trả về lịch làm việc của nhân viên trong một ngày cụ thể.
        :param day: Ngày cần lấy lịch làm việc (dạng chuỗi, ví dụ: '2025-04-21').
        :return: Danh sách các ca làm việc trong ngày đó. Nếu không có lịch, trả về danh sách rỗng.
        """
        return self.schedule.get(day, [])

    def __repr__(self):
        return f"Worker(id={self.id}, name={self.name}, position={self.position}, schedule={(self.schedule)})"


class Operation:
    def __init__(
        self,
        operation_id: str,
        production_order_id: str,
        name: str,
        required_machine_type: str,
        required_position: str,
        prev_operation: List[str],
        assigned_kpis: List[Dict[str, float]],
        achieved_kpis: List[float],
        start_date: str = None,
        start_shift: int = None,
        end_date: str = None,
        end_shift: int = None,
        detailed_schedule: List[Dict[str, str]] = None,
    ):
        """
        :param operation_id: ID của công đoạn
        :param production_order_id: ID của lệnh sản xuất mà công đoạn thuộc về
        :param name: Tên của công đoạn
        :param required_machine_type: Loại máy móc yêu cầu
        :param required_position: Vị trí nhân viên yêu cầu
        :param prev_operation: Danh sách các công đoạn trước đó (ID)
        :param assigned_kpis: KPI được giao (danh sách dictionary chứa id, name, value)
        :param achieved_kpis: KPI đạt được (mảng vì có nhiều loại KPI)
        :param start_date: Ngày bắt đầu
        :param start_shift: Ca bắt đầu
        :param end_date: Ngày kết thúc
        :param end_shift: Ca kết thúc
        :param detailed_schedule: Lịch chi tiết (danh sách các dictionary chứa thông tin ngày, ca, nhân viên, máy)
        """
        self.operation_id = operation_id
        self.production_order_id = production_order_id
        self.name = name
        self.required_machine_type = required_machine_type
        self.required_position = required_position
        self.prev_operation = prev_operation
        self.assigned_kpis = assigned_kpis
        self.achieved_kpis = achieved_kpis
        self.start_date = start_date
        self.start_shift = start_shift
        self.end_date = end_date
        self.end_shift = end_shift
        self.detailed_schedule = detailed_schedule if detailed_schedule else []

    def export_to_json(self, file_path: str) -> None:
        """
        Xuất thông tin của chính công đoạn này ra file JSON.
        :param file_path: Đường dẫn file JSON để ghi dữ liệu.
        """
        # Chuẩn bị dữ liệu để ghi
        operation_data = {
            "name": self.name,
            "achieved_kpi_0": self.achieved_kpis[0] if self.achieved_kpis else 0.0,
            "assigned_kpi_0": (
                self.assigned_kpis[0]["value"] if self.assigned_kpis else 0.0
            ),
            "achieved_kpi_1": self.achieved_kpis[1] if self.achieved_kpis and len(self.achieved_kpis) > 1 else 0.0,
            "assigned_kpi_1": (
                self.assigned_kpis[1]["value"] if self.assigned_kpis and len(self.assigned_kpis) > 1 else 0.0
            ),
            "detailed_schedule": self.detailed_schedule,
        }

        # Ghi dữ liệu ra file JSON ở chế độ append
        with open(file_path, "a", encoding="utf-8") as json_file:
            json.dump(operation_data, json_file, indent=4, ensure_ascii=False)
            json_file.write("\n")  # Thêm dòng mới để phân tách các đối tượng

    def update_detailed_schedule(
        self, day: str, shift: int, worker_id: str, asset_id: str
    ) -> None:
        """
        Cập nhật lịch chi tiết (detailed_schedule) cho công đoạn.
        :param day: Ngày làm việc (dạng chuỗi, ví dụ: '2025-04-21').
        :param shift: Ca làm việc (1, 2, 3, 4).
        :param worker_id: ID của nhân viên.
        :param asset_id: ID của máy móc.
        """
        # Tạo một mục mới cho lịch chi tiết
        schedule_entry = {
            "day": day,
            "shift": shift,
            "worker_id": worker_id,
            "asset_id": asset_id,
        }

        # Thêm mục mới vào detailed_schedule
        self.detailed_schedule.append(schedule_entry)

    def update_achieved_kpi_0(self, increment: float) -> bool:
        """
        Cập nhật giá trị KPI đạt được tại vị trí [0] bằng cách tăng thêm giá trị truyền vào.
        :param increment: Giá trị cần tăng thêm cho KPI[0].
        :return: Giá trị KPI[0] sau khi cập nhật.
        """
        if not self.achieved_kpis:
            # Nếu danh sách achieved_kpis rỗng, khởi tạo giá trị mặc định là 0
            self.achieved_kpis = [0.0]

        if len(self.achieved_kpis) < 1:
            # Đảm bảo danh sách có ít nhất 1 phần tử
            self.achieved_kpis.append(0.0)

        # Cập nhật KPI
        self.achieved_kpis[0] += increment

        # Kiểm tra KPI đạt được so với KPI được giao
        assigned_value = (
            self.assigned_kpis[0]["value"]
            if self.assigned_kpis and len(self.assigned_kpis) > 0
            else 0.0
        )
        return self.achieved_kpis[0] >= assigned_value

    def update_achieved_kpis(self, increment_kpi0: float, increment_kpi1: float) -> bool:
        """
        Cập nhật giá trị cả hai KPI đạt được tại vị trí [0] và [1].
        Nếu KPI đã vượt quá lượng cần thiết, sẽ trừ đi một lượng increment*x/5.5
        với x là giá trị nguyên lớn nhất sao cho vẫn đạt KPI. Giá trị x sẽ giống nhau cho cả 2 KPI.
        
        :param increment_kpi0: Giá trị cần tăng thêm cho KPI[0] (sản lượng).
        :param increment_kpi1: Giá trị cần tăng thêm cho KPI[1] (chất lượng).
        :return: True nếu tất cả KPI đạt hoặc vượt mức yêu cầu, False nếu chưa.
        """
        if not self.achieved_kpis:
            # Nếu danh sách achieved_kpis rỗng, khởi tạo giá trị mặc định là [0.0, 0.0]
            self.achieved_kpis = [0.0, 0.0]
        
        # Đảm bảo danh sách có ít nhất 2 phần tử
        while len(self.achieved_kpis) < 2:
            self.achieved_kpis.append(0.0)

        # Lấy giá trị KPI được giao
        assigned_value_0 = (
            self.assigned_kpis[0]["value"]
            if self.assigned_kpis and len(self.assigned_kpis) > 0
            else 0.0
        )
        assigned_value_1 = (
            self.assigned_kpis[1]["value"]
            if self.assigned_kpis and len(self.assigned_kpis) > 1
            else 0.0
        )
        
        # Kiểm tra xem có cần điều chỉnh không
        need_adjustment_kpi0 = self.achieved_kpis[0] + increment_kpi0 > assigned_value_0 and increment_kpi0 > 0
        need_adjustment_kpi1 = self.achieved_kpis[1] + increment_kpi1 > assigned_value_1 and increment_kpi1 > 0
        
        # Chỉ điều chỉnh nếu ít nhất một KPI vượt quá mức cần thiết
        if need_adjustment_kpi0 or need_adjustment_kpi1:
            # Tìm x lớn nhất sao cho cả hai KPI vẫn đạt được với công thức:
            # achieved_kpi + increment*(1-x/5.5) >= assigned_kpi
            
            # Rút gọn công thức để tìm x:
            # achieved_kpi + increment - increment*x/5.5 >= assigned_kpi
            # increment*x/5.5 <= achieved_kpi + increment - assigned_kpi
            # x <= 5.5 * (achieved_kpi + increment - assigned_kpi) / increment
            
            # Tính x_max cho từng KPI
            if need_adjustment_kpi0:
                max_x_kpi0 = 5.5 * (self.achieved_kpis[0] + increment_kpi0 - assigned_value_0) / increment_kpi0
            else:
                max_x_kpi0 = float('inf')  # Không giới hạn x nếu không cần điều chỉnh KPI0
                
            if need_adjustment_kpi1:
                max_x_kpi1 = 5.5 * (self.achieved_kpis[1] + increment_kpi1 - assigned_value_1) / increment_kpi1
            else:
                max_x_kpi1 = float('inf')  # Không giới hạn x nếu không cần điều chỉnh KPI1
            
            # Lấy giá trị x lớn nhất mà vẫn đảm bảo cả hai KPI đạt được (chọn min của cả hai)
            max_x = min(max_x_kpi0, max_x_kpi1)
            
            # Lấy phần nguyên của max_x
            x = int(max_x)
            
            # Áp dụng điều chỉnh với giá trị x cho cả hai KPI
            if need_adjustment_kpi0:
                increment_kpi0 = increment_kpi0 * (1 - x/5.5)
            
            if need_adjustment_kpi1:
                increment_kpi1 = increment_kpi1 * (1 - x/5.5)
        
        # Cập nhật các KPI với giá trị đã được điều chỉnh
        self.achieved_kpis[0] += increment_kpi0
        self.achieved_kpis[1] += increment_kpi1
        
        # Kiểm tra cả hai KPI đạt được so với KPI được giao
        return self.achieved_kpis[0] >= assigned_value_0 and self.achieved_kpis[1] >= assigned_value_1

    def get_workers_in_previous_shift(self, day: str, shift: int) -> List[str]:
        """
        Lấy danh sách các nhân viên đã làm việc vào ca trước của ngày và ca được nhập vào.
        :param day: Ngày cần kiểm tra (dạng chuỗi, ví dụ: '2025-04-21').
        :param shift: Ca làm việc cần kiểm tra (1, 2, 3, 4).
        :return: Danh sách ID các nhân viên đã làm việc vào ca trước đó. Nếu không có lịch, trả về danh sách rỗng.
        """
        # Xác định ca trước
        if shift == 1:
            # Nếu là ca 1, chuyển sang ngày trước và lấy ca 4
            previous_day = (
                datetime.strptime(day, "%Y-%m-%d") - timedelta(days=1)
            ).strftime("%Y-%m-%d")
            previous_shift = 4
        else:
            # Nếu không phải ca 1, chỉ cần giảm ca
            previous_day = day
            previous_shift = shift - 1

        # Lọc danh sách nhân viên từ detailed_schedule
        workers = [
            entry["worker_id"]
            for entry in self.detailed_schedule
            if entry["day"] == previous_day and int(entry["shift"]) == previous_shift
        ]
        return workers

    def __repr__(self):
        return (
            f"Operation(operation_id={self.operation_id}, production_order_id={self.production_order_id}, "
            f"name={self.name}, required_machine_type={self.required_machine_type}, "
            f"required_position={self.required_position}, prev_operation={self.prev_operation}, "
            f"assigned_kpis={self.assigned_kpis}, achieved_kpis={self.achieved_kpis}, "
            f"start_date={self.start_date}, start_shift={self.start_shift}, "
            f"end_date={self.end_date}, end_shift={self.end_shift}, "
            f"detailed_schedule={len(self.detailed_schedule)} entries)"
        )


class ProductionOrder:
    def __init__(
        self,
        order_id: str,
        name: str,
        quantity: int,
        start_date: str,
        start_shift: int,
        end_date: str,
        end_shift: int,
        operations: List[Operation],
        dependencies: Dict[str, List[str]],
    ):
        """
        :param order_id: ID của lệnh sản xuất
        :param name: Tên của lệnh sản xuất
        :param quantity: Số lượng sản phẩm cần sản xuất
        :param start_date: Ngày bắt đầu sản xuất
        :param start_shift: Ca bắt đầu sản xuất
        :param end_date: Ngày kết thúc dự kiến
        :param end_shift: Ca kết thúc dự kiến
        :param operations: Danh sách các công đoạn (dùng class Operation)
        :param dependencies: Ràng buộc giữa các công đoạn (key: công đoạn, value: danh sách các công đoạn trước đó)
        """
        self.order_id = order_id
        self.name = name
        self.quantity = quantity
        self.start_date = start_date
        self.start_shift = start_shift
        self.end_date = end_date
        self.end_shift = end_shift
        self.operations = operations  # Danh sách các công đoạn
        self.completed_operations = []  # Danh sách công đoạn đã hoàn thành
        self.dependencies = dependencies  # Ràng buộc prevOperation
        self.total_operations = len(operations)

    def add_operation(self, operation: Operation):
        """Thêm một công đoạn mới vào danh sách công đoạn."""
        self.operations.append(operation)

    def mark_operation_completed(self, operation_id: str):
        """Đánh dấu một công đoạn là đã hoàn thành."""
        if operation_id not in self.completed_operations:
            self.completed_operations.append(operation_id)

    def is_ready_to_start(self, operation_id: str) -> bool:
        """
        Kiểm tra xem một công đoạn có thể bắt đầu hay không.
        Một công đoạn chỉ có thể bắt đầu nếu tất cả các công đoạn trước đó đã hoàn thành.
        """
        required_operations = self.dependencies.get(operation_id, [])
        return all(op in self.completed_operations for op in required_operations)

    def __repr__(self):
        return (
            f"ProductionOrder(order_id={self.order_id}, name={self.name}, quantity={self.quantity}, "
            f"start_date={self.start_date}, start_shift={self.start_shift}, end_date={self.end_date}, "
            f"end_shift={self.end_shift}, operations={len(self.operations)}, "
            f"completed_operations={len(self.completed_operations)}, dependencies={len(self.dependencies)})"
        )


class Asset:
    def __init__(
        self,
        asset_id: str,
        name: str,
        asset_type: str,
        cost_per_hour: float,
        productivity: float,
    ):
        """
        :param asset_id: ID của máy
        :param name: Tên của máy
        :param asset_type: Loại máy (ví dụ: T001, T002, T003)
        :param cost_per_hour: Chi phí vận hành mỗi giờ
        :param productivity: Năng suất của máy (hiệu suất làm việc)
        """
        self.asset_id = asset_id
        self.name = name
        self.asset_type = asset_type
        self.cost_per_hour = cost_per_hour
        self.productivity = productivity

    def __repr__(self):
        return (
            f"asset(asset_id={self.asset_id}, name={self.name}, asset_type={self.asset_type}, "
            f"cost_per_hour={self.cost_per_hour}, productivity={self.productivity})"
        )
