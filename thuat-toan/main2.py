from encoder import (
    load_json,
    parse_workers,
    parse_operations,
    parse_production_orders,
    parse_assets,
)
from harmony_search_nhanh_can_trong_so import HarmonySearch  # Import thuật toán Harmony Search
import json
import time
import sys

def write_parsed_data_to_txt(workers, operations, production_orders, assets, file_path):
    """
    Ghi tất cả dữ liệu đã được parse ra file TXT để kiểm tra.
    :param workers: Danh sách nhân viên.
    :param operations: Danh sách công đoạn.
    :param production_orders: Danh sách lệnh sản xuất.
    :param assets: Danh sách máy móc.
    :param file_path: Đường dẫn file TXT để ghi dữ liệu.
    """
    with open(file_path, "w", encoding="utf-8") as txt_file:
        txt_file.write("Workers:\n")
        for worker in workers:
            txt_file.write(f"{worker}\n")

        txt_file.write("\nOperations:\n")
        for operation in operations:
            txt_file.write(f"{operation}\n")

        txt_file.write("\nProduction Orders:\n")
        for production_order in production_orders:
            txt_file.write(f"{production_order}\n")

        txt_file.write("\nAssets:\n")
        for asset in assets:
            txt_file.write(f"{asset}\n")

    print(f"Dữ liệu đã được ghi vào file {file_path}")


def main():
    # # Kiểm tra xem có đủ tham số command line không
    # if len(sys.argv) < 2:
    #     print("Cách sử dụng: python main.py <input_file>")
    #     print("Ví dụ: python main.py input3.json")
    #     sys.exit(1)
    
    # # Lấy tên file từ command line argument
    # input_filename = sys.argv[1]
    
    # # Tạo đường dẫn đầy đủ
    # input_path = f"./data-2/{input_filename}"
    
    # # Đọc dữ liệu từ file JSON
    # try:
    #     input_data = load_json(input_path)
    # except FileNotFoundError:
    #     print(f"Không tìm thấy file: {input_path}")
    #     sys.exit(1)
    # except Exception as e:
    #     print(f"Lỗi khi đọc file {input_path}: {e}")
    #     sys.exit(1)

    # Đọc dữ liệu từ file JSON
    input_data = load_json("./data-2/input9_2.json")
    schedule_data = load_json("./data-2/monthly_schedule_t45.json")

    # Parse dữ liệu
    workers = parse_workers(input_data, schedule_data)
    operations = parse_operations(input_data)
    production_orders = parse_production_orders(input_data, operations)
    assets = parse_assets(input_data)

    # Khởi tạo và chạy Harmony Search
    hs = HarmonySearch(
        workers=workers,
        machines=assets,
        operations=operations,
        production_orders=production_orders,
    )
    # Đánh dấu thời gian bắt đầu
    start_time = time.time()
    
    # Chạy thuật toán tối ưu
    best_solution, best_fitness, operations_copy = hs.optimize()
    
    # Đánh dấu thời gian kết thúc và tính thời gian thực thi
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Thời gian thực thi thuật toán: {execution_time:.2f} giây")

    # Chuyển đổi best_solution thành JSON
    serialized_solution = serialize_best_solution(best_solution)

    # output_path = f"../out/out2/{input_filename}/best_solution.json"
    output_path ="./out/out2/input9_2/best_solution.json"
    write_data_to_json(
        serialized_solution,
        output_path,
    )

    # export_all_operations_to_json(
    #     operations_copy, f"../out/out2/{input_filename}/schedule.json"
    # )
    export_all_operations_to_json(
        operations_copy, "./out/out2/input9_2/schedule.json"
    )

    print(f"Tối ưu: {best_fitness}")


def serialize_best_solution(best_solution):
    """
    Chuyển đổi best_solution thành định dạng chỉ chứa ID của workers và machines.
    :param best_solution: Giải pháp tốt nhất.
    :return: Dữ liệu đã được chuyển đổi chỉ chứa ID.
    """
    return {
        operation_id: {
            "workers": [worker.id for worker in details["workers"]],
            "machines": [machine.asset_id for machine in details["machines"]],
        }
        for operation_id, details in best_solution.items()
    }


def write_data_to_json(data, file_path):
    """
    Ghi dữ liệu ra file JSON.
    :param data: Dữ liệu cần ghi.
    :param file_path: Đường dẫn file JSON để ghi dữ liệu.
    """
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(f"Dữ liệu đã được ghi vào file {file_path}")


def export_all_operations_to_json(operations, file_path: str) -> None:
    """
    Xuất tất cả các công đoạn (operations) ra file JSON.
    :param operations: Danh sách các đối tượng Operation.
    :param file_path: Đường dẫn file JSON để ghi dữ liệu.
    """
    # Chuẩn bị danh sách dữ liệu để ghi
    operations_data = []
    for operation in operations:
        operation_data = {
            "commandId": operation.production_order_id,
            "id": operation.operation_id,
            "name": operation.name,
            "achieved_kpi_0": (
                operation.achieved_kpis[0] if operation.achieved_kpis else 0.0
            ),
            "assigned_kpi_0": (
                operation.assigned_kpis[0]["value"] if operation.assigned_kpis else 0.0
            ),
            "achieved_kpi_1": (
                operation.achieved_kpis[1] if operation.achieved_kpis else 0.0
            ),
            "assigned_kpi_1": (
                operation.assigned_kpis[1]["value"] if operation.assigned_kpis else 0.0
            ),
            "detailed_schedule": operation.detailed_schedule,
        }
        operations_data.append(operation_data)

    # Ghi danh sách dữ liệu ra file JSON
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(operations_data, json_file, indent=4, ensure_ascii=False)
    print(f"Tất cả công đoạn đã được ghi vào file {file_path}")


if __name__ == "__main__":
    main()
