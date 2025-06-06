import json
from typing import List, Dict
from models import Worker, Operation, ProductionOrder, Asset


def load_json(file_path: str) -> dict:
    """Load dữ liệu từ file JSON."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def parse_workers(input_data: dict, schedule_data: list) -> List[Worker]:
    """Parse danh sách nhân viên từ input.json và monthly_schedule.json."""
    # Tạo dictionary để lưu lịch làm việc của từng nhân viên
    worker_schedules = {}

    # Duyệt qua dữ liệu lịch làm việc từ `monthly_schedule.json`
    for day in schedule_data:
        date = day["date"]
        for worker_id, shifts in day["schedule"].items():
            if worker_id not in worker_schedules:
                worker_schedules[worker_id] = {}
            worker_schedules[worker_id][date] = shifts

    # Tạo danh sách nhân viên từ `input.json`
    workers = []
    for worker_data in input_data["workers"]:
        worker_id = worker_data["id"]
        schedule = worker_schedules.get(worker_id, {})  # Lấy lịch làm việc nếu có
        worker = Worker(
            id=worker_id,
            name=worker_data["name"],
            position=worker_data["position"],
            productivity_kpi=worker_data["productivityKPI"],
            quality_kpi=worker_data["qualityKPI"],
            salary_per_hour=worker_data["salaryPerHour"],
            schedule=schedule,
        )
        workers.append(worker)

    return workers


def parse_operations(input_data: dict) -> List[Operation]:
    """Parse danh sách công đoạn từ input.json."""
    operations = []
    for operation_data in input_data["operations"]:
        operation = Operation(
            operation_id=operation_data["id"],
            production_order_id=operation_data["productionOrderId"],
            name=operation_data["name"],
            required_machine_type=operation_data["requiredMachineType"],
            required_position=operation_data["requiredPosition"],
            prev_operation=operation_data["prevOperation"],
            assigned_kpis=[
                {"id": kpi["id"], "name": kpi["name"], "value": kpi["value"]}
                for kpi in operation_data["kpis"]
            ],
            achieved_kpis=[],  # Mặc định là rỗng
            start_date=operation_data.get(
                "startDate"
            ),  # Lấy giá trị nếu có, mặc định là None
            start_shift=operation_data.get(
                "startShift"
            ),  # Lấy giá trị nếu có, mặc định là None
            end_date=operation_data.get(
                "endDate"
            ),  # Lấy giá trị nếu có, mặc định là None
            end_shift=operation_data.get(
                "endShift"
            ),  # Lấy giá trị nếu có, mặc định là None
            detailed_schedule=operation_data.get(
                "detailedSchedule", []
            ),  # Lấy giá trị nếu có, mặc định là rỗng
        )
        operations.append(operation)
    return operations


def parse_production_orders(
    input_data: dict, operations: List[Operation]
) -> List[ProductionOrder]:
    """Parse danh sách lệnh sản xuất từ input.json."""
    production_orders = []
    operation_map = {op.operation_id: op for op in operations}

    for order_data in input_data["productionOrders"]:
        # Lấy danh sách công đoạn liên quan đến lệnh sản xuất này
        order_operations = [
            operation_map[op["id"]]
            for op in input_data["operations"]
            if op["productionOrderId"] == order_data["id"]
        ]

        # Tạo đối tượng ProductionOrder
        production_order = ProductionOrder(
            order_id=order_data["id"],
            name=order_data["name"],
            quantity=order_data["quantity"],
            start_date=order_data["startDate"],
            start_shift=None,  # Sẽ được cập nhật sau
            end_date=order_data["endDate"],
            end_shift=None,  # Sẽ được cập nhật sau
            operations=order_operations,
            dependencies={
                op["id"]: op["prevOperation"]
                for op in input_data["operations"]
                if op["productionOrderId"] == order_data["id"]
            },
        )
        production_orders.append(production_order)

    return production_orders


def parse_assets(input_data: dict) -> List[Asset]:
    """Parse danh sách tài sản từ input.json."""
    assets = []
    for asset_data in input_data["assets"]:
        asset = Asset(
            asset_id=asset_data["id"],
            name=asset_data["name"],
            asset_type=asset_data["machineType"],
            cost_per_hour=asset_data["costPerHour"],
            productivity=asset_data["productivity"],
        )
        assets.append(asset)
    return assets
