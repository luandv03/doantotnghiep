import random
from typing import List, Dict
import copy
import json
from datetime import datetime, timedelta
import math

class HarmonySearch:
    def preprocess_data(self):
        """
        Tiền xử lý dữ liệu để nhóm nhân viên, máy móc và công đoạn theo yêu cầu.
        """
        # Nhóm nhân viên theo vị trí
        self.workers_by_position = {}
        for worker in self.workers:
            if worker.position not in self.workers_by_position:
                self.workers_by_position[worker.position] = []
            self.workers_by_position[worker.position].append(worker)

        # Nhóm máy móc theo loại
        self.machines_by_type = {}
        for machine in self.machines:
            if machine.asset_type not in self.machines_by_type:
                self.machines_by_type[machine.asset_type] = []
            self.machines_by_type[machine.asset_type].append(machine)

        # Nhóm công đoạn theo các tiêu chí khác nhau
        self.operations_by_requirements = {}
        self.operations_by_worker = {}
        self.operations_by_asset = {}

        for operation in self.operations:
            # Nhóm theo vị trí và loại máy móc
            key = (operation.required_position, operation.required_machine_type)
            if key not in self.operations_by_requirements:
                self.operations_by_requirements[key] = []
            self.operations_by_requirements[key].append(operation)

            # Nhóm theo vị trí nhân viên (required_position)
            position = operation.required_position
            if position not in self.operations_by_worker:
                self.operations_by_worker[position] = []
            self.operations_by_worker[position].append(operation)

            # Nhóm theo loại máy móc (required_machine_type)
            asset_type = operation.required_machine_type
            if asset_type not in self.operations_by_asset:
                self.operations_by_asset[asset_type] = []
            self.operations_by_asset[asset_type].append(operation)

        # Ánh xạ công đoạn với các công đoạn phụ thuộc
        self.operation_dependencies = {}
        for operation in self.operations:
            self.operation_dependencies[operation.operation_id] = set(
                operation.prev_operation or []
            )

    def __init__(
        self,
        workers: List[Dict],
        machines: List[Dict],
        operations: List[Dict],
        production_orders: List[Dict],
        harmony_memory_size: int = None,
        max_iterations: int = None,
        harmony_consideration_rate: float = 0.9,
        pitch_adjustment_rate: float = 0.3,
    ):
        """
        :param workers: Danh sách nhân viên (mỗi nhân viên là một dictionary chứa thông tin)
        :param machines: Danh sách máy móc (mỗi máy là một dictionary chứa thông tin)
        :param operations: Danh sách công đoạn cần ghép
        :param production_orders: Danh sách lệnh sản xuất
        :param harmony_memory_size: Kích thước bộ nhớ Harmony (tự động tính toán nếu không nhập)
        :param max_iterations: Số lần lặp tối đa (tự động tính toán nếu không nhập)
        :param harmony_consideration_rate: Tỷ lệ xem xét Harmony Memory
        :param pitch_adjustment_rate: Tỷ lệ điều chỉnh pitch
        """
        self.workers = workers
        self.machines = machines
        self.operations = operations
        self.production_orders = production_orders
        
        # Tự động điều chỉnh tham số dựa trên kích thước dữ liệu
        data_size = len(workers) + len(machines) + len(operations) + len(production_orders)
        
        # Xác định harmony_memory_size
        if harmony_memory_size is None:
            if data_size < 50:  # Dữ liệu nhỏ
                self.harmony_memory_size = 10
            elif data_size < 100:  # Dữ liệu trung bình
                self.harmony_memory_size = 20
            else:  # Dữ liệu lớn
                self.harmony_memory_size = 30
        else:
            self.harmony_memory_size = harmony_memory_size
            
        # Xác định max_iterations
        if max_iterations is None:
            if data_size < 50:  # Dữ liệu nhỏ
                self.max_iterations = 10
            elif data_size < 100:  # Dữ liệu trung bình
                self.max_iterations = 20
            else:  # Dữ liệu lớn
                self.max_iterations = 100
        else:
            self.max_iterations = max_iterations
            
        self.harmony_consideration_rate = harmony_consideration_rate
        self.pitch_adjustment_rate = pitch_adjustment_rate
        self.harmony_memory = []

        # Tiền xử lý dữ liệu
        self.preprocess_data()

    def initialize_harmony_memory(self):
        """Khởi tạo Harmony Memory với các giải pháp ngẫu nhiên."""
        for _ in range(self.harmony_memory_size):
            solution, operations_copy = self.generate_random_solution()
            fitness = self.evaluate_solution(solution, operations_copy)
            self.harmony_memory.append((solution, fitness, operations_copy))

    def generate_random_solution(self) -> tuple[Dict, List]:
        """
        Tạo một giải pháp ngẫu nhiên bằng cách gán nhân viên và máy móc cho tất cả công đoạn.
        Đảm bảo mỗi công đoạn có ít nhất 1 nhân viên và 1 máy móc.
        :return: Tuple gồm giải pháp (solution) và bản deepcopy của danh sách operations.
        """
        solution = {
            operation.operation_id: {"workers": [], "machines": []}
            for operation in self.operations
        }
        available_workers = set(self.workers)  # Tập nhân viên khả dụng
        available_machines = set(self.machines)  # Tập máy móc khả dụng

        # Bước 1: Đảm bảo mỗi công đoạn có ít nhất 1 nhân viên và 1 máy móc
        for operation in self.operations:
            # Gán 1 nhân viên phù hợp
            eligible_workers = self.workers_by_position.get(
                operation.required_position, []
            )
            if eligible_workers:
                selected_worker = random.choice(eligible_workers)
                solution[operation.operation_id]["workers"].append(selected_worker)
                available_workers.discard(selected_worker)

            # Gán 1 máy móc phù hợp
            eligible_machines = self.machines_by_type.get(
                operation.required_machine_type, []
            )
            if eligible_machines:
                selected_machine = random.choice(eligible_machines)
                solution[operation.operation_id]["machines"].append(selected_machine)
                available_machines.discard(selected_machine)

        # Bước 2: Phân bổ phần còn lại theo trọng số Softmax
        # Gán nhân viên còn lại
        for worker in available_workers:
            eligible_operations = self.operations_by_worker.get(worker.position, [])

            if eligible_operations:
                weights = [
                    math.exp(-len(solution[op.operation_id]["workers"]))
                    for op in eligible_operations
                ]
                total_weight = sum(weights)
                weights = [w / total_weight for w in weights]

                selected_operation = random.choices(
                    eligible_operations, weights=weights, k=1
                )[0]
                solution[selected_operation.operation_id]["workers"].append(worker)

        # Gán máy móc còn lại
        for machine in available_machines:
            eligible_operations = self.operations_by_asset.get(machine.asset_type, [])

            if eligible_operations:
                weights = [
                    math.exp(-len(solution[op.operation_id]["machines"]))
                    for op in eligible_operations
                ]
                total_weight = sum(weights)
                weights = [w / total_weight for w in weights]

                selected_operation = random.choices(
                    eligible_operations, weights=weights, k=1
                )[0]
                solution[selected_operation.operation_id]["machines"].append(machine)

        # Tạo một bản deepcopy của danh sách operations
        operations_copy = copy.deepcopy(self.operations)

        return solution, operations_copy

    def evaluate_solution(
        self, solution: Dict, operations: List
    ) -> tuple[int, int, int]:
        """
        Hàm đánh giá giải pháp.
        :param solution: Giải pháp hiện tại.
        :param operations: Danh sách các công đoạn.
        :return: Tuple gồm số lệnh sản xuất hoàn thành đúng hạn và tổng số ca làm việc.
        """
        return self.schedule_operations(solution, operations)

    def optimize(self):
        """Chạy thuật toán Harmony Search với cải tiến hội tụ sớm và cải tiến giải pháp cục bộ."""
        # Bắt đầu đo thời gian
        start_time = datetime.now()
        
        self.initialize_harmony_memory()

        # Theo dõi số lần lặp không cải tiến
        no_improvement_counter = 0
        best_fitness_so_far = (-float('inf'), float('inf'), float('inf'))  # (completed_orders, shifts, cost)
        
        # Biến theo dõi để thực hiện tái khởi tạo
        restarts = 0
        max_restarts = 2
        
        # Lưu trữ giải pháp tốt nhất từng tìm thấy
        global_best_solution = None
        global_best_fitness = (-float('inf'), float('inf'), float('inf'))
        global_best_operations_copy = None
        
        # Thêm điều kiện dừng sớm cho dữ liệu nhỏ
        early_stop_threshold = 5  # Số lần lặp không cải thiện trước khi dừng sớm với dữ liệu nhỏ
        data_size = len(self.workers) + len(self.machines) + len(self.operations) + len(self.production_orders)
        early_stop_enabled = data_size < 50  # Chỉ bật dừng sớm cho dữ liệu nhỏ
        
        # Biến theo dõi mức độ hoàn thành
        perfect_solution_found = False
        # Nếu tất cả các lệnh sản xuất được hoàn thành đúng hạn, đây là giải pháp hoàn hảo
        all_orders_count = len(self.production_orders)

        # Biến theo dõi số lần lặp thực tế
        actual_iterations = 0

        for iteration in range(self.max_iterations):
            actual_iterations = iteration + 1
            
            # Giai đoạn học tập: điều chỉnh tham số dựa trên kết quả trước đó
            if iteration > 0 and iteration % 10 == 0:
                self.update_parameters_based_on_performance()
            
            # Tạo nhiều giải pháp mới trong mỗi lần lặp
            num_new_solutions = max(3, 5 - restarts)  # Giảm số lượng giải pháp mới khi tái khởi tạo
            best_new_solution = None
            best_new_fitness = (-float('inf'), float('inf'), float('inf'))

            for _ in range(num_new_solutions):
                # Tạo và đánh giá giải pháp mới
                new_solution, operations_copy = self.improvise_new_solution()
                
                # Áp dụng cải tiến cục bộ cho giải pháp mới
                if random.random() < 0.3:  # 30% cơ hội cải tiến cục bộ
                    new_solution, operations_copy = self.local_refinement(new_solution, operations_copy)
                
                fitness = self.evaluate_solution(new_solution, operations_copy)
                
                # Cập nhật giải pháp tốt nhất trong lần lặp này
                if self.is_better_fitness(fitness, best_new_fitness):
                    best_new_solution = (new_solution, fitness, operations_copy)
                    best_new_fitness = fitness

            # Lấy giải pháp mới tốt nhất
            new_solution, fitness, operations_copy = best_new_solution
            completed_orders_on_time, total_shift, total_cost = fitness
            
            # Áp dụng lai tạo với giải pháp tốt nhất hiện tại (nếu có)
            if global_best_solution is not None and random.random() < 0.4:
                hybrid_solution = self.hybridize_solutions(new_solution, global_best_solution)
                hybrid_operations_copy = copy.deepcopy(self.operations)
                hybrid_fitness = self.evaluate_solution(hybrid_solution, hybrid_operations_copy)
                
                if self.is_better_fitness(hybrid_fitness, fitness):
                    new_solution, fitness, operations_copy = hybrid_solution, hybrid_fitness, hybrid_operations_copy
                    completed_orders_on_time, total_shift, total_cost = hybrid_fitness
            
            print(
                f"New fitness: Completed Orders On Time = {completed_orders_on_time}, Total Shifts = {total_shift}, Total Cost = {total_cost}"
            )

            # Tìm giải pháp tệ nhất trong Harmony Memory
            worst_solution_index = self.find_worst_solution_index()

            # So sánh giải pháp mới với giải pháp tệ nhất
            if self.is_better_fitness(fitness, self.harmony_memory[worst_solution_index][1]):
                self.harmony_memory[worst_solution_index] = (
                    new_solution,
                    (completed_orders_on_time, total_shift, total_cost),
                    operations_copy,
                )

            # Tìm giải pháp tốt nhất hiện tại
            best_solution_index = self.find_best_solution_index()
            current_best_fitness = self.harmony_memory[best_solution_index][1]
            print(f"Iteration {iteration + 1}: Best fitness = {current_best_fitness}")

            # Cập nhật giải pháp tốt nhất toàn cục
            if self.is_better_fitness(current_best_fitness, global_best_fitness):
                global_best_solution = copy.deepcopy(self.harmony_memory[best_solution_index][0])
                global_best_fitness = current_best_fitness
                global_best_operations_copy = copy.deepcopy(self.harmony_memory[best_solution_index][2])
                
                # Kiểm tra nếu đã tìm thấy giải pháp hoàn hảo (tất cả lệnh sản xuất hoàn thành đúng hạn)
                # if global_best_fitness[0] == all_orders_count:
                #     perfect_solution_found = True
                #     print("Tìm thấy giải pháp hoàn hảo! Tất cả các lệnh sản xuất đều hoàn thành đúng hạn.")
                #     break

            # Kiểm tra cải tiến
            if self.is_better_fitness(current_best_fitness, best_fitness_so_far):
                best_fitness_so_far = current_best_fitness
                no_improvement_counter = 0
                
                # Đa dạng hóa Harmony Memory nếu cải thiện được giải pháp
                if iteration > self.max_iterations // 3:
                    self.diversify_harmony_memory(0.1)  # Thay thế 10% giải pháp tệ nhất
            else:
                no_improvement_counter += 1
                
                # Điều chỉnh Harmony Consideration Rate và Pitch Adjustment Rate
                if no_improvement_counter >= 10:
                    self.harmony_consideration_rate = max(0.7, self.harmony_consideration_rate * 0.95)
                    self.pitch_adjustment_rate = min(0.5, self.pitch_adjustment_rate * 1.05)
                    print(f"Adjusted HCR: {self.harmony_consideration_rate:.2f}, PAR: {self.pitch_adjustment_rate:.2f}")
                    no_improvement_counter = 0
                
                # Dừng sớm cho dữ liệu nhỏ nếu không có cải tiến
                if early_stop_enabled and no_improvement_counter >= early_stop_threshold:
                    print(f"Dừng sớm tại lần lặp {iteration + 1} - không có cải tiến sau {early_stop_threshold} lần lặp")
                    break
                    
                # Tái khởi tạo nếu không có cải tiến sau nhiều lần lặp
                if no_improvement_counter >= 15 and restarts < max_restarts:
                    print(f"Tái khởi tạo Harmony Memory lần {restarts + 1}")
                    self.restart_search(global_best_solution)
                    restarts += 1
                    no_improvement_counter = 0
                # Dừng sớm nếu không có cải tiến sau nhiều lần lặp và đã tái khởi tạo đủ số lần
                elif no_improvement_counter >= 20 and iteration > self.max_iterations // 2 and restarts >= max_restarts:
                    print(f"Dừng sớm tại lần lặp {iteration + 1} do không có cải tiến")
                    break

        # Tính thời gian thực thi
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        print(f"Thuật toán đã thực thi trong {execution_time:.2f} giây và {actual_iterations} lần lặp")

        print("Tất cả các giá trị fitness đã tìm được:")
        for entry in self.harmony_memory:
            print(
                f"Completed Orders On Time: {entry[1][0]}, Total Shifts: {entry[1][1]}, Total Cost: {entry[1][2]}"
            )

        # Ghi thông tin Harmony Memory ra file với thời gian thực thi
        # self.print_harmony_memory(execution_time)

        # Kiểm tra xem giải pháp tốt nhất toàn cục có tốt hơn giải pháp tốt nhất trong harmony_memory không
        best_hm_solution = min(
            self.harmony_memory,
            key=lambda x: (-x[1][0], x[1][1], x[1][2]),
        )
        
        if self.is_better_fitness(global_best_fitness, best_hm_solution[1]):
            return global_best_solution, global_best_fitness, global_best_operations_copy
        else:
            return best_hm_solution
            
    def is_better_fitness(self, fitness1, fitness2):
        """
        So sánh hai giá trị fitness để xác định cái nào tốt hơn.
        :param fitness1: Tuple (completed_orders, shifts, cost)
        :param fitness2: Tuple (completed_orders, shifts, cost)
        :return: True nếu fitness1 tốt hơn fitness2, False nếu ngược lại
        """
        # Ưu tiên số lệnh hoàn thành đúng hạn (càng nhiều càng tốt)
        if fitness1[0] > fitness2[0]:
            return True
        elif fitness1[0] < fitness2[0]:
            return False
        
        # Nếu số lệnh bằng nhau, ưu tiên số ca làm việc (càng ít càng tốt)
        if fitness1[1] < fitness2[1]:
            return True
        elif fitness1[1] > fitness2[1]:
            return False
        
        # Nếu số ca bằng nhau, ưu tiên chi phí (càng ít càng tốt)
        return fitness1[2] < fitness2[2]
        
    def find_worst_solution_index(self):
        """Tìm chỉ số của giải pháp tệ nhất trong Harmony Memory."""
        return max(
            range(len(self.harmony_memory)),
            key=lambda i: (
                -self.harmony_memory[i][1][0],  # Ưu tiên số lệnh đúng hạn
                self.harmony_memory[i][1][1],   # Sau đó ưu tiên tổng số ca
                self.harmony_memory[i][1][2],   # Cuối cùng ưu tiên tổng chi phí
            ),
        )
        
    def find_best_solution_index(self):
        """Tìm chỉ số của giải pháp tốt nhất trong Harmony Memory."""
        return min(
            range(len(self.harmony_memory)),
            key=lambda i: (
                -self.harmony_memory[i][1][0],  # Ưu tiên số lệnh đúng hạn
                self.harmony_memory[i][1][1],   # Sau đó ưu tiên tổng số ca
                self.harmony_memory[i][1][2],   # Cuối cùng ưu tiên tổng chi phí
            ),
        )
    
    def local_refinement(self, solution, operations_copy):
        """
        Cải tiến cục bộ cho giải pháp bằng cách hoán đổi tài nguyên.
        
        :param solution: Giải pháp cần cải tiến
        :param operations_copy: Bản sao của các công đoạn
        :return: Giải pháp đã cải tiến và bản sao operations mới
        """
        refined_solution = copy.deepcopy(solution)
        
        # Lựa chọn ngẫu nhiên một số công đoạn để tối ưu
        num_operations_to_refine = min(5, len(self.operations))
        operations_to_refine = random.sample(self.operations, num_operations_to_refine)
        
        for operation in operations_to_refine:
            op_id = operation.operation_id
            
            # 1. Sắp xếp lại nhân viên theo năng suất và chất lượng
            if refined_solution[op_id]["workers"]:
                # Thay thế nhân viên năng suất thấp bằng nhân viên năng suất cao
                current_workers = refined_solution[op_id]["workers"]
                eligible_workers = [
                    w for w in self.workers 
                    if w.position == operation.required_position
                    and w not in current_workers
                ]
                
                if eligible_workers:
                    # Thay thế nhân viên có kết hợp (năng suất*chất lượng) thấp nhất
                    worst_worker = min(current_workers, key=lambda w: w.productivity_kpi * w.quality_kpi)
                    better_workers = [w for w in eligible_workers 
                                     if w.productivity_kpi * w.quality_kpi > worst_worker.productivity_kpi * worst_worker.quality_kpi]
                    
                    if better_workers:
                        best_replacement = max(better_workers, key=lambda w: w.productivity_kpi * w.quality_kpi)
                        refined_solution[op_id]["workers"].remove(worst_worker)
                        refined_solution[op_id]["workers"].append(best_replacement)
            
            # 2. Sắp xếp lại máy móc theo năng suất
            if refined_solution[op_id]["machines"]:
                # Thay thế máy móc năng suất thấp bằng máy móc năng suất cao
                current_machines = refined_solution[op_id]["machines"]
                eligible_machines = [
                    m for m in self.machines 
                    if m.asset_type == operation.required_machine_type
                    and m not in current_machines
                ]
                
                if eligible_machines:
                    # Thay thế máy móc có năng suất thấp nhất
                    worst_machine = min(current_machines, key=lambda m: m.productivity)
                    better_machines = [m for m in eligible_machines if m.productivity > worst_machine.productivity]
                    
                    if better_machines:
                        best_replacement = max(better_machines, key=lambda m: m.productivity)
                        refined_solution[op_id]["machines"].remove(worst_machine)
                        refined_solution[op_id]["machines"].append(best_replacement)
        
        # Cập nhật operations_copy
        new_operations_copy = copy.deepcopy(self.operations)
        
        return refined_solution, new_operations_copy
    
    def restart_search(self, best_solution=None):
        """
        Tái khởi tạo Harmony Memory nhưng giữ lại một số giải pháp tốt.
        
        :param best_solution: Giải pháp tốt nhất tìm được đến thời điểm hiện tại
        """
        # Lưu lại giải pháp tốt nhất
        if best_solution is not None:
            best_entry = [entry for entry in self.harmony_memory if entry[0] == best_solution]
            if best_entry:
                best_entry = best_entry[0]
            else:
                best_entry = min(self.harmony_memory, key=lambda x: (-x[1][0], x[1][1], x[1][2]))
        else:
            best_entry = min(self.harmony_memory, key=lambda x: (-x[1][0], x[1][1], x[1][2]))
        
        # Xóa bộ nhớ Harmony cũ
        self.harmony_memory = []
        
        # Khởi tạo lại Harmony Memory
        for i in range(self.harmony_memory_size):
            if i == 0 and best_entry is not None:
                # Giữ lại giải pháp tốt nhất
                self.harmony_memory.append(best_entry)
            else:
                # Tạo giải pháp mới với độ đa dạng cao
                solution, operations_copy = self.generate_random_solution()
                fitness = self.evaluate_solution(solution, operations_copy)
                self.harmony_memory.append((solution, fitness, operations_copy))
        
        # Reset tham số về giá trị ban đầu
        self.harmony_consideration_rate = 0.9
        self.pitch_adjustment_rate = 0.3
    
    def update_parameters_based_on_performance(self):
        """
        Cập nhật tham số dựa trên hiệu suất của thuật toán.
        Mục tiêu: Tăng cường khám phá khi hiệu suất kém, tăng cường
        khai thác khi hiệu suất tốt.
        """
        # Tính mức độ đa dạng của Harmony Memory
        diversity = self.calculate_harmony_memory_diversity()
        
        if diversity < 0.3:  # Đa dạng thấp
            # Tăng khám phá
            self.harmony_consideration_rate = max(0.7, self.harmony_consideration_rate * 0.95)
            self.pitch_adjustment_rate = min(0.5, self.pitch_adjustment_rate * 1.05)
        elif diversity > 0.7:  # Đa dạng cao
            # Tăng khai thác
            self.harmony_consideration_rate = min(0.95, self.harmony_consideration_rate * 1.05)
            self.pitch_adjustment_rate = max(0.2, self.pitch_adjustment_rate * 0.95)
    
    def calculate_harmony_memory_diversity(self):
        """
        Tính độ đa dạng của Harmony Memory.
        :return: Giá trị từ 0 (không đa dạng) đến 1 (rất đa dạng)
        """
        if len(self.harmony_memory) <= 1:
            return 1.0
        
        total_diversity = 0
        combinations_count = 0
        
        # So sánh từng cặp giải pháp
        for i in range(len(self.harmony_memory)):
            for j in range(i+1, len(self.harmony_memory)):
                similarity = self.calculate_solution_similarity(
                    self.harmony_memory[i][0], 
                    self.harmony_memory[j][0]
                )
                diversity = 1 - similarity
                total_diversity += diversity
                combinations_count += 1
        
        return total_diversity / combinations_count if combinations_count > 0 else 1.0
    
    def calculate_solution_similarity(self, solution1, solution2):
        """
        Tính độ tương đồng giữa hai giải pháp.
        :return: Giá trị từ 0 (hoàn toàn khác nhau) đến 1 (hoàn toàn giống nhau)
        """
        total_count = 0
        similar_count = 0
        
        for operation_id in solution1:
            # So sánh workers
            workers1 = set(solution1[operation_id]["workers"])
            workers2 = set(solution2[operation_id]["workers"])
            
            # So sánh machines
            machines1 = set(solution1[operation_id]["machines"])
            machines2 = set(solution2[operation_id]["machines"])
            
            # Tính số lượng nhân viên và máy móc chung
            common_workers = len(workers1.intersection(workers2))
            common_machines = len(machines1.intersection(machines2))
            
            # Tổng số nhân viên và máy móc
            total_workers = len(workers1) + len(workers2)
            total_machines = len(machines1) + len(machines2)
            
            if total_workers > 0:
                similar_count += 2 * common_workers
                total_count += total_workers
            
            if total_machines > 0:
                similar_count += 2 * common_machines
                total_count += total_machines
        
        return similar_count / total_count if total_count > 0 else 0
    
    def hybridize_solutions(self, solution1, solution2):
        """
        Lai tạo hai giải pháp để tạo ra giải pháp mới.
        :param solution1: Giải pháp thứ nhất
        :param solution2: Giải pháp thứ hai
        :return: Giải pháp mới sau khi lai tạo
        """
        hybrid_solution = {}
        
        for operation_id in solution1:
            # Khởi tạo công đoạn mới
            hybrid_solution[operation_id] = {"workers": [], "machines": []}
            
            # Lấy thông tin công đoạn tương ứng
            operation = next((op for op in self.operations if op.operation_id == operation_id), None)
            if not operation:
                continue
            
            # Lai tạo workers (lấy từ một trong hai giải pháp gốc)
            workers_pool = set()
            
            # Tạo tập hợp tất cả nhân viên có thể sử dụng
            if random.random() < 0.7:  # 70% lấy từ giải pháp 1, 30% lấy từ giải pháp 2
                for worker in solution1[operation_id]["workers"]:
                    if worker.position == operation.required_position:
                        workers_pool.add(worker)
            else:
                for worker in solution2[operation_id]["workers"]:
                    if worker.position == operation.required_position:
                        workers_pool.add(worker)
            
            # Lấy thêm nhân viên từ giải pháp còn lại nếu chưa đủ
            if len(workers_pool) < 2:
                for worker in solution2[operation_id]["workers"] + solution1[operation_id]["workers"]:
                    if worker.position == operation.required_position and worker not in workers_pool:
                        workers_pool.add(worker)
                        if len(workers_pool) >= 2:
                            break
            
            # Chuyển từ set sang list và sắp xếp theo cả năng suất và chất lượng
            workers_list = sorted(list(workers_pool), key=lambda w: w.productivity_kpi * w.quality_kpi, reverse=True)
            
            # Lấy tối đa 3 nhân viên năng suất và chất lượng cao nhất
            hybrid_solution[operation_id]["workers"] = workers_list[:3]
            
            # Lai tạo machines (tương tự như workers)
            machines_pool = set()
            
            if random.random() < 0.7:  # 70% lấy từ giải pháp 1, 30% lấy từ giải pháp 2
                for machine in solution1[operation_id]["machines"]:
                    if machine.asset_type == operation.required_machine_type:
                        machines_pool.add(machine)
            else:
                for machine in solution2[operation_id]["machines"]:
                    if machine.asset_type == operation.required_machine_type:
                        machines_pool.add(machine)
            
            # Lấy thêm máy móc từ giải pháp còn lại nếu chưa đủ
            if len(machines_pool) < 2:
                for machine in solution2[operation_id]["machines"] + solution1[operation_id]["machines"]:
                    if machine.asset_type == operation.required_machine_type and machine not in machines_pool:
                        machines_pool.add(machine)
                        if len(machines_pool) >= 2:
                            break
            
            # Chuyển từ set sang list và sắp xếp theo năng suất
            machines_list = sorted(list(machines_pool), key=lambda m: m.productivity, reverse=True)
            
            # Lấy tối đa 3 máy móc năng suất cao nhất
            hybrid_solution[operation_id]["machines"] = machines_list[:3]
            
            # Đảm bảo mỗi công đoạn có ít nhất 1 worker và 1 machine
            if not hybrid_solution[operation_id]["workers"]:
                eligible_workers = [
                    worker for worker in self.workers
                    if worker.position == operation.required_position
                ]
                if eligible_workers:
                    selected_worker = max(eligible_workers, key=lambda w: w.productivity_kpi)
                    hybrid_solution[operation_id]["workers"].append(selected_worker)
            
            if not hybrid_solution[operation_id]["machines"]:
                eligible_machines = [
                    machine for machine in self.machines
                    if machine.asset_type == operation.required_machine_type
                ]
                if eligible_machines:
                    selected_machine = max(eligible_machines, key=lambda m: m.productivity)
                    hybrid_solution[operation_id]["machines"].append(selected_machine)
        
        return hybrid_solution

    def print_harmony_memory(self, execution_time=None):
        """
        In toàn bộ Harmony Memory theo định dạng yêu cầu.
        
        :param execution_time: Thời gian chạy thuật toán (nếu có)
        """
        formatted_memory = []

        for solution, fitness, operations_copy in self.harmony_memory:
            formatted_solution = {"operations": []}

            for operation_id, allocation in solution.items():
                formatted_operation = {
                    "id": operation_id,
                    "worker": [{"id": worker.id} for worker in allocation["workers"]],
                    "asset": [
                        {"id": machine.asset_id} for machine in allocation["machines"]
                    ],
                }
                formatted_solution["operations"].append(formatted_operation)

            formatted_memory.append(formatted_solution)

        # Lấy thông tin về giải pháp tốt nhất
        best_solution_index = self.find_best_solution_index()
        best_fitness = self.harmony_memory[best_solution_index][1]
        
        # Thêm thông tin về tham số và kết quả
        algorithm_info = {
            "algorithm_params": {
                "harmony_memory_size": self.harmony_memory_size,
                "max_iterations": self.max_iterations,
                "harmony_consideration_rate": self.harmony_consideration_rate,
                "pitch_adjustment_rate": self.pitch_adjustment_rate
            },
            "data_size": {
                "workers": len(self.workers),
                "machines": len(self.machines),
                "operations": len(self.operations),
                "production_orders": len(self.production_orders)
            },
            "best_result": {
                "completed_orders_on_time": best_fitness[0],
                "total_shifts": best_fitness[1],
                "total_cost": best_fitness[2]
            }
        }
        
        if execution_time is not None:
            algorithm_info["execution_time_seconds"] = execution_time
        
        # Lưu thông tin thuật toán vào file riêng
        algo_file_path = "tour/algorithm_info.json"
        with open(algo_file_path, "w", encoding="utf-8") as json_file:
            json.dump(algorithm_info, json_file, ensure_ascii=False, indent=4)
        print(f"Thông tin thuật toán đã được ghi vào file: {algo_file_path}")
        
        # In thông tin tổng quan
        print(f"\nTổng quan thuật toán:")
        print(f"Kích thước dữ liệu: {len(self.workers)} nhân viên, {len(self.machines)} máy móc, " 
              f"{len(self.operations)} công đoạn, {len(self.production_orders)} lệnh sản xuất")
        print(f"Tham số: HMS={self.harmony_memory_size}, MaxIter={self.max_iterations}, "
              f"HCR={self.harmony_consideration_rate:.2f}, PAR={self.pitch_adjustment_rate:.2f}")
        print(f"Kết quả tốt nhất: {best_fitness[0]} lệnh hoàn thành đúng hạn, {best_fitness[1]} ca làm việc, "
              f"{best_fitness[2]} chi phí")
        if execution_time is not None:
            print(f"Thời gian chạy: {execution_time:.2f} giây")

    def improvise_new_solution(self) -> tuple[Dict, List]:
        """
        Tạo một giải pháp mới dựa trên Harmony Memory với cải tiến heuristic.
        :return: Tuple gồm giải pháp (solution) và bản deepcopy của danh sách operations.
        """
        solution = {
            operation.operation_id: {"workers": [], "machines": []}
            for operation in self.operations
        }

        used_workers = set()  # Lưu trữ nhân viên đã được sử dụng
        used_machines = set()  # Lưu trữ máy móc đã được sử dụng
        
        # Sắp xếp các công đoạn theo độ ưu tiên (ví dụ: dựa trên dependencies)
        operations_priority = {}
        for op in self.operations:
            # Số lượng công đoạn phụ thuộc vào công đoạn này
            dependent_count = sum(1 for deps in self.operation_dependencies.values() if op.operation_id in deps)
            # Số lượng công đoạn mà công đoạn này phụ thuộc vào
            dependency_count = len(op.prev_operation) if op.prev_operation else 0
            # Độ ưu tiên: công đoạn có nhiều dependencies nhưng ít dependents sẽ có ưu tiên cao hơn
            operations_priority[op.operation_id] = dependency_count - 0.5 * dependent_count
            
        # Sắp xếp các công đoạn theo độ ưu tiên tăng dần
        sorted_operations = sorted(
            self.operations, 
            key=lambda op: operations_priority[op.operation_id]
        )

        # Bước 1: Áp dụng Harmony Consideration cho các công đoạn theo thứ tự ưu tiên
        for operation in sorted_operations:
            operation_id = operation.operation_id
            
            if random.random() < self.harmony_consideration_rate:
                # Chọn một giải pháp ngẫu nhiên từ Harmony Memory, thiên vị các giải pháp tốt
                weights = [1 / (i + 1) for i in range(len(self.harmony_memory))]
                sorted_hm = sorted(
                    self.harmony_memory,
                    key=lambda x: (-x[1][0], x[1][1], x[1][2])
                )
                selected_solution = random.choices(
                    [entry[0] for entry in sorted_hm],
                    weights=weights,
                    k=1
                )[0]

                # Sao chép worker và machine từ giải pháp đã chọn
                if operation_id in selected_solution:
                    # Workers
                    for worker in selected_solution[operation_id]["workers"]:
                        if worker not in used_workers and worker.position == operation.required_position:
                            solution[operation_id]["workers"].append(worker)
                            used_workers.add(worker)
                            
                            # Áp dụng Pitch Adjustment với xác suất PAR
                            if random.random() < self.pitch_adjustment_rate:
                                # Tìm công đoạn khác có cùng yêu cầu
                                alternative_ops = [
                                    op for op in sorted_operations
                                    if op.required_position == worker.position and op.operation_id != operation_id
                                ]
                                if alternative_ops:
                                    alt_op = random.choice(alternative_ops)
                                    solution[operation_id]["workers"].remove(worker)
                                    solution[alt_op.operation_id]["workers"].append(worker)
                    
                    # Machines
                    for machine in selected_solution[operation_id]["machines"]:
                        if machine not in used_machines and machine.asset_type == operation.required_machine_type:
                            solution[operation_id]["machines"].append(machine)
                            used_machines.add(machine)
                            
                            # Áp dụng Pitch Adjustment với xác suất PAR
                            if random.random() < self.pitch_adjustment_rate:
                                # Tìm công đoạn khác có cùng yêu cầu
                                alternative_ops = [
                                    op for op in sorted_operations
                                    if op.required_machine_type == machine.asset_type and op.operation_id != operation_id
                                ]
                                if alternative_ops:
                                    alt_op = random.choice(alternative_ops)
                                    solution[operation_id]["machines"].remove(machine)
                                    solution[alt_op.operation_id]["machines"].append(machine)
        
        # Bước 2: Phân bổ workers chưa được gán với heuristic cải tiến
        unassigned_workers = [worker for worker in self.workers if worker not in used_workers]
        
        # Sắp xếp workers theo năng suất giảm dần
        unassigned_workers.sort(key=lambda w: w.productivity_kpi, reverse=True)
        
        for worker in unassigned_workers:
            eligible_operations = [
                op for op in self.operations
                if op.required_position == worker.position
            ]
            
            if eligible_operations:
                # Trọng số dựa trên số lượng workers đã có và độ ưu tiên của công đoạn
                weights = []
                for op in eligible_operations:
                    # Trọng số ngược với số lượng workers đã có
                    worker_weight = math.exp(-len(solution[op.operation_id]["workers"]))
                    # Trọng số theo độ ưu tiên của công đoạn
                    priority_weight = math.exp(-operations_priority[op.operation_id])
                    # Kết hợp các trọng số
                    weights.append(worker_weight * priority_weight)
                
                total_weight = sum(weights) if sum(weights) > 0 else 1
                norm_weights = [w / total_weight for w in weights]
                
                selected_operation = random.choices(eligible_operations, weights=norm_weights, k=1)[0]
                solution[selected_operation.operation_id]["workers"].append(worker)
                used_workers.add(worker)

        # Bước 3: Phân bổ machines chưa được gán với heuristic cải tiến
        unassigned_machines = [machine for machine in self.machines if machine not in used_machines]
        
        # Sắp xếp machines theo năng suất giảm dần
        unassigned_machines.sort(key=lambda m: m.productivity, reverse=True)
        
        for machine in unassigned_machines:
            eligible_operations = [
                op for op in self.operations
                if op.required_machine_type == machine.asset_type
            ]
            
            if eligible_operations:
                # Trọng số dựa trên số lượng machines đã có và độ ưu tiên của công đoạn
                weights = []
                for op in eligible_operations:
                    # Trọng số ngược với số lượng machines đã có
                    machine_weight = math.exp(-len(solution[op.operation_id]["machines"]))
                    # Trọng số theo độ ưu tiên của công đoạn
                    priority_weight = math.exp(-operations_priority[op.operation_id])
                    # Kết hợp các trọng số
                    weights.append(machine_weight * priority_weight)
                
                total_weight = sum(weights) if sum(weights) > 0 else 1
                norm_weights = [w / total_weight for w in weights]
                
                selected_operation = random.choices(eligible_operations, weights=norm_weights, k=1)[0]
                solution[selected_operation.operation_id]["machines"].append(machine)
                used_machines.add(machine)

        # Bước 4: Đảm bảo mọi công đoạn có ít nhất 1 worker và 1 machine
        for operation in self.operations:
            operation_id = operation.operation_id
            
            # Thêm worker nếu chưa có
            if not solution[operation_id]["workers"]:
                eligible_workers = [
                    worker for worker in self.workers
                    if worker.position == operation.required_position
                ]
                if eligible_workers:
                    # Ưu tiên nhân viên có năng suất cao nhất
                    selected_worker = max(eligible_workers, key=lambda w: w.productivity_kpi)
                    solution[operation_id]["workers"].append(selected_worker)
            
            # Thêm machine nếu chưa có
            if not solution[operation_id]["machines"]:
                eligible_machines = [
                    machine for machine in self.machines
                    if machine.asset_type == operation.required_machine_type
                ]
                if eligible_machines:
                    # Ưu tiên máy có năng suất cao nhất
                    selected_machine = max(eligible_machines, key=lambda m: m.productivity)
                    solution[operation_id]["machines"].append(selected_machine)

        # Tạo một bản deepcopy của danh sách operations
        operations_copy = copy.deepcopy(self.operations)

        return solution, operations_copy

    def diversify_harmony_memory(self, percentage: float):
        """
        Đa dạng hóa một phần của Harmony Memory bằng cách thay thế các giải pháp tệ nhất
        bằng các giải pháp ngẫu nhiên mới.
        
        :param percentage: Phần trăm (0-1) của Harmony Memory cần đa dạng hóa
        """
        # Số lượng giải pháp cần thay thế
        num_to_replace = max(1, int(percentage * self.harmony_memory_size))
        
        # Xác định các giải pháp tệ nhất trong Harmony Memory
        worst_indices = sorted(
            range(len(self.harmony_memory)),
            key=lambda i: (-self.harmony_memory[i][1][0], self.harmony_memory[i][1][1], self.harmony_memory[i][1][2]),
            reverse=True
        )[:num_to_replace]
        
        # Thay thế các giải pháp tệ nhất bằng các giải pháp mới
        for idx in worst_indices:
            # Tạo giải pháp mới với xáo trộn cao hơn
            old_harmony_consideration_rate = self.harmony_consideration_rate
            old_pitch_adjustment_rate = self.pitch_adjustment_rate
            
            # Tạm thời tăng mức độ xáo trộn
            self.harmony_consideration_rate = 0.6  # Giảm để tăng tính ngẫu nhiên
            self.pitch_adjustment_rate = 0.5      # Tăng để thúc đẩy đa dạng
            
            # Tạo giải pháp mới
            new_solution, operations_copy = self.generate_random_solution()
            fitness = self.evaluate_solution(new_solution, operations_copy)
            
            # Khôi phục tham số
            self.harmony_consideration_rate = old_harmony_consideration_rate
            self.pitch_adjustment_rate = old_pitch_adjustment_rate
            
            # Thay thế giải pháp tệ
            self.harmony_memory[idx] = (new_solution, fitness, operations_copy)
            
        print(f"Đã đa dạng hóa {num_to_replace} giải pháp trong Harmony Memory")

    def parallel_evaluate_solutions(self, solutions_list):
        """
        Đánh giá song song nhiều giải pháp để cải thiện hiệu suất.
        
        :param solutions_list: Danh sách các cặp (solution, operations_copy)
        :return: Danh sách các kết quả đánh giá
        """
        results = []
        for solution, operations_copy in solutions_list:
            fitness = self.evaluate_solution(solution, operations_copy)
            results.append((solution, fitness, operations_copy))
        return results

    def schedule_operations(
        self, solution: Dict, operations: List
    ) -> tuple[int, int, int]:
        """
        Lên lịch cho các công đoạn dựa trên giải pháp - phiên bản cải tiến với chiến lược lập lịch thông minh.
        :param solution: Giải pháp hiện tại (mapping công đoạn với nhân viên và máy móc).
        :param operations: Danh sách các công đoạn.
        """
        total_shift = 0  # Tổng số ca làm việc
        total_cost = 0
        completed_orders_on_time = 0  # Số lệnh sản xuất hoàn thành đúng hạn
        completed_operations_by_order = {
            order.order_id: 0 for order in self.production_orders
        }  # Số công đoạn hoàn thành theo từng production_order_id

        start_date = "2025-04-01"
        completed_operations = []  # Danh sách các công đoạn đã hoàn thành
        current_date = datetime.strptime(start_date, "%Y-%m-%d")  # Ngày bắt đầu
        solution_copy = copy.deepcopy(solution)
        workers_in_completed_operation = set()
        machines_in_completed_operation = set()

        workers_in_last_shift = set()  # Tập hợp nhân viên đã làm việc trong ca trước
        
        # Tạo priority_queue - hàng đợi ưu tiên cho các công đoạn sẵn sàng
        ready_operations = []  # (độ ưu tiên, operation) - số càng thấp, ưu tiên càng cao
        
        # Hàm cập nhật hàng đợi công đoạn sẵn sàng
        def update_ready_operations():
            ready_operations.clear()
            for op in operations:
                if op.operation_id in completed_operations:
                    continue
                
                # Kiểm tra nếu tất cả công đoạn tiên quyết đã hoàn thành
                if all(prev_op in completed_operations for prev_op in op.prev_operation):
                    # Tính độ ưu tiên
                    # 1. Ưu tiên lệnh sản xuất gần deadline
                    order = next((o for o in self.production_orders if o.order_id == op.production_order_id), None)
                    days_to_deadline = 0
                    if order:
                        deadline = datetime.strptime(order.end_date, "%Y-%m-%d")
                        days_to_deadline = (deadline - current_date).days
                    
                    # 2. Ưu tiên giá trị KPI cao
                    kpi_value = op.assigned_kpis[0]["value"] if op.assigned_kpis else 0
                    
                    # 3. Ưu tiên công đoạn có nhiều dependents (nhiều công đoạn phụ thuộc vào nó)
                    dependent_count = sum(1 for deps in self.operation_dependencies.values() if op.operation_id in deps)
                    
                    # Tính tổng trọng số - số càng nhỏ ưu tiên càng cao
                    priority = days_to_deadline - 0.2 * kpi_value - 0.5 * dependent_count
                    
                    ready_operations.append((priority, op))
            
            # Sắp xếp theo độ ưu tiên tăng dần
            ready_operations.sort(key=lambda x: x[0])

        # Chiến lược lập lịch cải tiến
        max_days = 59  # Giới hạn số ngày
        
        while True:
            # Chuyển đổi datetime thành chuỗi
            day_str = current_date.strftime("%Y-%m-%d")
            
            # Cập nhật hàng đợi ưu tiên
            update_ready_operations()
            
            for shift in range(1, 5):  # Duyệt qua các ca từ 1 đến 4
                operations_completed_in_shift = []
                workers_in_current_shift = set()
                
                # Xử lý các công đoạn theo thứ tự ưu tiên
                for _, operation in ready_operations:
                    # Kiểm tra nếu công đoạn đã hoàn thành, bỏ qua
                    if operation.operation_id in completed_operations:
                        continue

                    # Lọc danh sách nhân viên phù hợp (không làm ca trước)
                    available_workers = [
                        worker
                        for worker in solution_copy[operation.operation_id]["workers"]
                        if worker.id not in workers_in_last_shift
                        and worker.schedule.get(day_str, [0, 0, 0, 0])[shift - 1] == 1
                        and worker.id not in workers_in_current_shift  # Thêm kiểm tra này để đảm bảo nhân viên không làm việc trong nhiều công đoạn cùng ca
                    ]

                    # Lọc danh sách máy móc phù hợp
                    available_machines = solution_copy[operation.operation_id]["machines"]

                    # Sắp xếp nhân viên và máy móc theo năng suất giảm dần
                    available_workers.sort(key=lambda w: w.productivity_kpi, reverse=True)
                    available_machines.sort(key=lambda m: m.productivity, reverse=True)

                    # Ghép cặp nhân viên và máy móc, tính tổng sản lượng
                    total_output_kpi0 = 0
                    total_output_kpi1 = 0
                    min_length = min(len(available_workers), len(available_machines))

                    # Phương án tối ưu hóa: nếu cần ít KPI để hoàn thành, chỉ sử dụng nguồn lực cần thiết
                    remaining_kpi = operation.assigned_kpis[0]["value"] - (operation.achieved_kpis[0] if operation.achieved_kpis else 0)
                    estimated_workers_needed = 1
                    
                    if min_length > 0:
                        # Ước tính số lượng nhân viên cần thiết dựa trên KPI còn lại
                        avg_worker_productivity = sum(w.productivity_kpi for w in available_workers[:min_length]) / min_length
                        avg_machine_productivity = sum(m.productivity for m in available_machines[:min_length]) / min_length
                        avg_pair_output = 5.5 * (avg_worker_productivity * avg_machine_productivity)
                        
                        if avg_pair_output > 0:
                            estimated_workers_needed = min(min_length, max(1, math.ceil(remaining_kpi / avg_pair_output)))
                    
                    # Ghép cặp nhân viên và máy móc theo năng suất cao nhất, chỉ sử dụng số lượng cần thiết
                    used_worker_ids = set()
                    for i in range(min(min_length, estimated_workers_needed)):
                        worker = available_workers[i]
                        machine = available_machines[i]
                        
                        # Tính KPI loại 0 (sản lượng)
                        pair_output_kpi0 = 5.5 * (worker.productivity_kpi * machine.productivity)
                        total_output_kpi0 += pair_output_kpi0
                        
                        # Tính KPI loại 1 (chất lượng)
                        pair_output_kpi1 = 5.5 * worker.productivity_kpi * machine.productivity * worker.quality_kpi
                        total_output_kpi1 += pair_output_kpi1

                        total_cost += 5.5 * (worker.salary_per_hour + machine.cost_per_hour)

                        # Thêm thông tin vào detailed_schedule
                        operation.update_detailed_schedule(
                            day=day_str,
                            shift=shift,
                            worker_id=worker.id,
                            asset_id=machine.asset_id,
                        )

                        workers_in_current_shift.add(worker.id)
                        used_worker_ids.add(worker.id)

                    # Cập nhật cả hai KPI
                    is_completed = operation.update_achieved_kpis(total_output_kpi0, total_output_kpi1)

                    # Kiểm tra nếu công đoạn đã hoàn thành
                    if is_completed:
                        operations_completed_in_shift.append(operation.operation_id)
                        completed_operations_by_order[operation.production_order_id] += 1

                        # Kiểm tra nếu lệnh sản xuất đã hoàn thành
                        order = next(
                            (o for o in self.production_orders if o.order_id == operation.production_order_id),
                            None,
                        )
                        if (
                            order
                            and completed_operations_by_order[order.order_id] == order.total_operations
                        ):
                            # So sánh thời gian hiện tại với end_date
                            order_end_date = datetime.strptime(order.end_date, "%Y-%m-%d")
                            if current_date <= order_end_date:
                                completed_orders_on_time += 1
                
                workers_in_last_shift.clear()
                workers_in_last_shift.update(workers_in_current_shift)

                # Thêm các công đoạn hoàn thành trong ca này vào danh sách completed_operations
                completed_operations.extend(operations_completed_in_shift)

                total_shift += 1  # Tăng total_shift lên 1 cho mỗi ca làm việc

                # Cập nhật hàng đợi ưu tiên sau mỗi ca
                if operations_completed_in_shift:
                    update_ready_operations()
                
                # Tối ưu hóa đánh giá sớm: nếu tất cả công đoạn đã hoàn thành thì dừng
                if len(completed_operations) == len(operations):
                    break

                # Lặp qua tất cả các công đoạn đã hoàn thành trong ca này
                for completed_operation_id in operations_completed_in_shift:
                    # Thêm nhân viên và máy móc từ công đoạn đã hoàn thành vào tập available_workers và available_machines
                    workers_in_completed_operation.update(
                        solution_copy[completed_operation_id]["workers"]
                    )
                    machines_in_completed_operation.update(
                        solution_copy[completed_operation_id]["machines"]
                    )

                    # Xóa nhân viên và máy móc khỏi công đoạn đã hoàn thành
                    solution_copy[completed_operation_id]["workers"] = []
                    solution_copy[completed_operation_id]["machines"] = []

                # Phân bổ lại tài nguyên thông minh
                self._reallocate_resources(solution_copy, completed_operations, operations, day_str, shift, 
                                          workers_in_completed_operation, machines_in_completed_operation)

            # Điều kiện dừng (break)
            if len(completed_operations) == len(operations) or total_shift > max_days * 4:
                break

            # Tăng ngày lên 1
            current_date += timedelta(days=1)
            if (current_date - datetime.strptime(start_date, "%Y-%m-%d")).days > max_days:
                break

        return completed_orders_on_time, total_shift, total_cost
    
    def _reallocate_resources(self, solution_copy, completed_operations, operations, day_str, shift,
                             workers_in_completed_operation, machines_in_completed_operation):
        """
        Phân bổ lại tài nguyên từ các công đoạn đã hoàn thành cho các công đoạn sẵn sàng tiếp theo.
        Hàm này được tách ra để làm rõ logic và dễ bảo trì.
        """
        # Lấy danh sách các công đoạn sẵn sàng tiếp theo
        ready_next_operations = []
        for op in operations:
            if op.operation_id not in completed_operations and all(
                prev_op in completed_operations for prev_op in op.prev_operation
            ):
                ready_next_operations.append(op)
        
        # Sắp xếp theo độ ưu tiên (ví dụ: deadline gần hơn, KPI cao hơn)
        ready_next_operations.sort(key=lambda op: (
            op.end_date if op.end_date else "9999-12-31",  # Ưu tiên deadline gần
            -sum(kpi["value"] for kpi in op.assigned_kpis) if op.assigned_kpis else 0  # Ưu tiên KPI cao
        ))
        
        # Phân bổ workers thông minh
        for worker in workers_in_completed_operation.copy():
            eligible_operations = [
                op for op in ready_next_operations
                if op.required_position == worker.position
            ]
            
            if eligible_operations:
                # Nếu worker có quality_kpi cao, ưu tiên cho các công đoạn có KPI yêu cầu cao
                if worker.quality_kpi > 0.8:  # Ngưỡng chất lượng cao
                    eligible_operations.sort(key=lambda op: 
                        -sum(kpi["value"] for kpi in op.assigned_kpis) if op.assigned_kpis else 0
                    )
                
                # Chọn công đoạn có độ ưu tiên cao nhất
                target_operation = eligible_operations[0]
                
                # Ghép worker với công đoạn
                solution_copy[target_operation.operation_id]["workers"].append(worker)
                workers_in_completed_operation.discard(worker)
        
        # Phân bổ machines thông minh
        for machine in machines_in_completed_operation.copy():
            eligible_operations = [
                op for op in ready_next_operations
                if op.required_machine_type == machine.asset_type
            ]
            
            if eligible_operations:
                # Nếu machine có productivity cao, ưu tiên cho các công đoạn có KPI yêu cầu cao
                if machine.productivity > 0.8:  # Ngưỡng năng suất cao
                    eligible_operations.sort(key=lambda op: 
                        -sum(kpi["value"] for kpi in op.assigned_kpis) if op.assigned_kpis else 0
                    )
                
                # Chọn công đoạn có độ ưu tiên cao nhất
                target_operation = eligible_operations[0]
                
                # Ghép machine với công đoạn
                solution_copy[target_operation.operation_id]["machines"].append(machine)
                machines_in_completed_operation.discard(machine)
