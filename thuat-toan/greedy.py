# -*- coding: utf-8 -*-
"""
Phân bổ nguồn lực sử dụng thuật toán Greedy
Chương trình đọc dữ liệu từ file JSON và thực hiện lập lịch sản xuất
"""

import json
import time
import os
import sys

def load_data_files():
    """
    Tìm và đọc file input và schedule từ thư mục hiện tại
    """
    input_file = "./data-2/input9_2.json"  # Đường dẫn mặc định
    schedule_file = "./data-2/monthly_schedule_t45.json"  # Đường dẫn mặc định
    
    if not input_file:
        print("Không tìm thấy file input JSON. Vui lòng đặt file có tên chứa 'input' trong thư mục hiện tại.")
        sys.exit(1)
    
    if not schedule_file:
        print("Không tìm thấy file schedule JSON. Vui lòng đặt file có tên chứa 'schedule' trong thư mục hiện tại.")
        sys.exit(1)
    
    print(f"Đọc dữ liệu từ: {input_file} và {schedule_file}")
    
    try:
        with open(input_file, encoding='utf-8') as f:
            data = json.load(f)
        with open(schedule_file, encoding='utf-8') as f:
            schedules = json.load(f)
        return data, schedules
    except FileNotFoundError as e:
        print(f"Lỗi: Không tìm thấy file {e.filename}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Lỗi: File JSON không hợp lệ - {e}")
        sys.exit(1)

# BƯỚC 1: ĐỌC DỮ LIỆU
data, schedules = load_data_files()

# Khai báo các biến dữ liệu
production_orders = data['productionOrders']  # Danh sách lệnh sản xuất
operations = data['operations']               # Danh sách công đoạn
assets = data['assets']                       # Danh sách thiết bị/máy móc
workers = data['workers']                     # Danh sách nhân viên

# Tạo dict tiện tra cứu nhanh
assets_dict = {a['id']: a for a in assets}
workers_dict = {w['id']: w for w in workers}
operations_dict = {op['id']: op for op in operations}

print(f"Đã tải dữ liệu: {len(production_orders)} lệnh sản xuất, {len(operations)} công đoạn, {len(assets)} thiết bị, {len(workers)} nhân viên")

# BƯỚC 2: HÀM TIỆN ÍCH

def is_consecutive(assignments, date_idx, shift_idx):
    """
    Kiểm tra nhân viên đã bị phân lịch vào ca liên tiếp chưa (không cho phép 2 ca liên tiếp).
    """
    if shift_idx > 0 and (date_idx, shift_idx-1) in assignments:
        return True
    if shift_idx < 3 and (date_idx, shift_idx+1) in assignments:
        return True
    if shift_idx == 0 and (date_idx-1, 3) in assignments:
        return True
    if shift_idx == 3 and (date_idx+1, 0) in assignments:
        return True
    return False

def calc_kpi(worker, asset, hours):
    """
    Tính toán năng suất (ns) và chất lượng (cl) dựa vào worker, máy, số giờ làm việc.
    """
    ns = worker['productivityKPI'] * asset['productivity'] * hours
    cl = ns * worker['qualityKPI']
    return ns, cl

def calc_cost(worker, asset, hours):
    """
    Tính chi phí cho một ca làm việc: (lương nhân viên/giờ + chi phí máy/giờ) * số giờ.
    """
    return (worker.get('salaryPerHour', 0) + asset.get('costPerHour', 0)) * hours

# BƯỚC 3: LẬP LỊCH GREEDY (chọn tốt nhất, break ngay khi đủ KPI)

print("\n=== BẮT ĐẦU LẬP LỊCH GREEDY ===")

worker_assignments = {}   # Lưu lại ca đã phân cho từng nhân viên
machine_assignments = {}  # Lưu lại ca đã phân cho từng máy
operation_progress = {}   # Lưu tiến độ từng công đoạn: kpi, lịch sử, trạng thái, chi phí
op_status = {}            # op_id -> True/False: đã hoàn thành chưa
op_end_time = {}          # op_id -> (date_idx, shift_idx): ca hoàn thành cuối cùng

start_time = time.time()  # Đo thời gian thực thi thuật toán

pending_ops = operations.copy()  # Danh sách công đoạn chưa lập lịch xong

while pending_ops:
    next_pending = []
    for op in pending_ops:
        op_id = op['id']
        prev_ops = op.get('prevOperation', [])
        # Nếu còn công đoạn tiên quyết chưa xong thì bỏ qua lần này
        if prev_ops and not all(op_status.get(pid, False) for pid in prev_ops):
            next_pending.append(op)
            continue

        # Xác định thời điểm bắt đầu sớm nhất
        if prev_ops:
            prev_end_times = [op_end_time[pid] for pid in prev_ops]
            latest_end = max(prev_end_times)
            prev_date, prev_shift = latest_end
            max_shift_idx = schedules[0]['shift_count'] - 1
            if prev_shift < max_shift_idx:
                earliest_start = (prev_date, prev_shift + 1)
            else:
                earliest_start = (prev_date + 1, 0)
        else:
            earliest_start = (0, 0)  # Nếu là công đoạn đầu thì bắt đầu từ ngày đầu

        # Chuẩn bị các biến tích lũy
        kpi_targets = {k['id']: k['value'] for k in op['kpis']}  # Giá trị mục tiêu KPI
        kpi_accum = {k['id']: 0 for k in op['kpis']}             # Giá trị đạt được thực tế
        op_history = []  # Lịch sử các lần phân bổ cho công đoạn này
        op_cost = 0
        done = False
        last_used = (0, 0)

        # ====== Lập lịch greedy từng ngày, từng ca ======
        break_outer = False  # Dùng để break cả 2 vòng lặp khi đã đạt KPI
        for date_idx, sch in enumerate(schedules):
            if break_outer:
                break
            for shift_idx in range(sch['shift_count']):
                if (date_idx, shift_idx) < earliest_start:
                    continue

                # ==== Check KPI trước khi phân bổ: Nếu đủ rồi thì dừng luôn ====
                if all(kpi_accum[kid] >= kpi_targets[kid] for kid in kpi_targets):
                    done = True
                    break_outer = True
                    break

                # ==== Lấy nhân viên hợp lệ cho ca này ====
                valid_workers = []
                for wid, slots in sch['schedule'].items():
                    if slots[shift_idx] == 1:
                        w = workers_dict.get(wid)
                        if not w or w['position'] != op['requiredPosition']:
                            continue
                        assignments = worker_assignments.get(wid, set())
                        if is_consecutive(assignments, date_idx, shift_idx):
                            continue
                        if (date_idx, shift_idx) in assignments:
                            continue
                        valid_workers.append((wid, w))
                # Ưu tiên nhân viên mạnh nhất
                valid_workers.sort(key=lambda x: x[1]['productivityKPI'] * x[1]['qualityKPI'], reverse=True)

                # ==== Lấy máy hợp lệ cho ca này ====
                valid_machines = []
                for aid, a in assets_dict.items():
                    if a['machineType'] != op['requiredMachineType']:
                        continue
                    assignments = machine_assignments.get(aid, set())
                    if (date_idx, shift_idx) in assignments:
                        continue
                    valid_machines.append((aid, a))
                # Ưu tiên máy mạnh nhất
                valid_machines.sort(key=lambda x: x[1]['productivity'], reverse=True)

                # ==== Ghép từng cặp nhân viên - máy ====
                num_pairs = min(len(valid_workers), len(valid_machines))
                used_workers = set()
                used_machines = set()
                for i in range(num_pairs):
                    # === Kiểm tra lại KPI, nếu đủ thì dừng ngay vòng nhỏ nhất ===
                    if all(kpi_accum[kid] >= kpi_targets[kid] for kid in kpi_targets):
                        done = True
                        break_outer = True
                        break

                    wid, w = valid_workers[i]
                    aid, a = valid_machines[i]
                    if wid in used_workers or aid in used_machines:
                        continue
                    hours = sch['work_duration_per_shift']
                    ns, cl = calc_kpi(w, a, hours)
                    cost = calc_cost(w, a, hours)

                    # Chỉ cộng KPI nếu chỉ tiêu đó chưa đạt (tránh cộng quá lố)
                    for k_idx, kpi in enumerate(op['kpis']):
                        if k_idx == 0:
                            kpi_accum[kpi['id']] += ns
                        else:
                            kpi_accum[kpi['id']] += cl

                    # Ghi lịch sử và cập nhật chi phí
                    op_history.append({
                        'date': sch['date'], 'shift': shift_idx+1,
                        'worker_id': wid, 'worker_name': w['name'],
                        'machine_id': aid, 'machine_name': a['name'],
                        'ns': ns, 'cl': cl,
                        'cost': cost
                    })
                    op_cost += cost
                    # Đánh dấu đã phân công ca này
                    worker_assignments.setdefault(wid, set()).add((date_idx, shift_idx))
                    machine_assignments.setdefault(aid, set()).add((date_idx, shift_idx))
                    used_workers.add(wid)
                    used_machines.add(aid)
                    last_used = (date_idx, shift_idx)
                # Sau mỗi ca cũng kiểm tra lại KPI (đủ là dừng luôn)
                if all(kpi_accum[kid] >= kpi_targets[kid] for kid in kpi_targets):
                    done = True
                    break_outer = True
                    break

        # Lưu kết quả cho công đoạn
        operation_progress[op_id] = {
            'kpi': kpi_accum, 'done': done, 'history': op_history, 'cost': op_cost
        }
        op_status[op_id] = done
        op_end_time[op_id] = last_used

    # Nếu không lập lịch được thêm công đoạn nào, báo lỗi phụ thuộc hoặc thiếu nguồn lực
    if len(next_pending) == len(pending_ops):
        print("\n⚠️ Có công đoạn không thể lập lịch do phụ thuộc lẫn nhau hoặc không đủ nguồn lực!")
        print("Các công đoạn còn pending:", [op['id'] for op in next_pending])
        break
    pending_ops = next_pending

end_time = time.time()  # Đo thời gian kết thúc

# BƯỚC 4: IN KẾT QUẢ PHÂN BỔ & TỔNG HỢP

print("\n" + "="*60)
print("KẾT QUẢ PHÂN BỔ NGUỒN LỰC")
print("="*60)

num_done = 0
total_cost = 0
all_working_slots = set()  # (ngày, ca)
opid_to_orderid = {op['id']: op['productionOrderId'] for op in operations}
orderid_to_ops = {}
for op in operations:
    orderid_to_ops.setdefault(op['productionOrderId'], []).append(op['id'])

for op_id, result in operation_progress.items():
    status = 'HOÀN THÀNH' if result['done'] else 'CHƯA HOÀN THÀNH'
    print(f"\n== Công đoạn {op_id}: {status} ==")
    for entry in result['history']:
        print(f"  Ngày {entry['date']} - Ca {entry['shift']}: "
              f"{entry['worker_id']} ({entry['worker_name']}) + "
              f"{entry['machine_id']} ({entry['machine_name']}) | "
              f"Năng suất: {entry['ns']:.2f}, Chất lượng: {entry['cl']:.2f}, "
              f"Chi phí: {entry['cost']:.0f}")
        all_working_slots.add((entry['date'], entry['shift']))
    print("Tổng KPI:", result['kpi'])
    print(f"Tổng chi phí công đoạn: {result['cost']:.0f}")
    if result['done']:
        num_done += 1
        total_cost += result['cost']

# Đếm số lệnh sản xuất hoàn thành
order_done = 0
for order in production_orders:
    order_id = order['id']
    ops = orderid_to_ops.get(order_id, [])
    if all(operation_progress.get(opid, {}).get('done', False) for opid in ops):
        order_done += 1

# Đếm tổng số ca sử dụng (không trùng lặp)
total_shifts = len(all_working_slots)

print("\n" + "="*60)
print("TỔNG KẾT")
print("="*60)
print(f">> Tổng số lệnh sản xuất hoàn thành: {order_done}/{len(production_orders)}")
print(f">> Tổng số công đoạn hoàn thành: {num_done}/{len(operations)}")
print(f">> Tổng số ca sử dụng: {total_shifts}")
print(f">> Tổng chi phí sản xuất: {total_cost:.0f}")
print(f">> Thời gian thực thi thuật toán: {end_time - start_time:.4f} giây")

# Ghi kết quả ra file (định dạng mới)
def save_results():
    """Lưu kết quả vào file JSON với định dạng mới"""
    operations_result = []
    
    for op_id, result in operation_progress.items():
        op_info = operations_dict[op_id]
        
        # Tạo detailed_schedule từ history
        detailed_schedule = []
        for entry in result['history']:
            detailed_schedule.append({
                "day": entry['date'],
                "shift": entry['shift'],
                "worker_id": entry['worker_id'],
                "asset_id": entry['machine_id']
            })
        
        # Tạo operation record theo định dạng yêu cầu
        operation_record = {
            "commandId": op_info['productionOrderId'],
            "id": op_id,
            "name": op_info['name'],
            "detailed_schedule": detailed_schedule
        }
        
        # Thêm achieved_kpi và assigned_kpi theo số lượng KPI
        kpi_list = sorted(result['kpi'].keys())  # Sắp xếp để đảm bảo thứ tự
        target_kpis = {k['id']: k['value'] for k in op_info['kpis']}
        
        for i, kpi_id in enumerate(kpi_list):
            operation_record[f"achieved_kpi_{i}"] = result['kpi'][kpi_id]
            operation_record[f"assigned_kpi_{i}"] = target_kpis[kpi_id]
        
        operations_result.append(operation_record)
    
    # Tạo kết quả tổng hợp
    # final_results = {
    #     'summary': {
    #         'completed_orders': order_done,
    #         'total_orders': len(production_orders),
    #         'completed_operations': num_done,
    #         'total_operations': len(operations),
    #         'total_shifts_used': total_shifts,
    #         'total_cost': total_cost,
    #         'execution_time': end_time - start_time
    #     },
    #     'operations': operations_result
    # }

    final_results = operations_result
    
    
    output_file = './out/out3/input9_2/schedule.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)
    print(f"\n>> Kết quả đã được lưu vào file: {output_file}")

# Hỏi người dùng có muốn lưu kết quả không
try:
    save_choice = input("\nBạn có muốn lưu kết quả vào file JSON không? (y/n): ").lower().strip()
    if save_choice in ['y', 'yes', 'có']:
        save_results()
except (EOFError, KeyboardInterrupt):
    print("\nChương trình kết thúc.")