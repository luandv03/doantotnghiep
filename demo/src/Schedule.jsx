import React, { useState } from "react";
import monthlySchedule from "../../thuat-toan/data-2/monthly_schedule_t45.json"; // Lịch đăng ký
import assignedSchedule from "../../thuat-toan/out/out3/input3/schedule.json"; // Lịch phân công
import inputData from "../../thuat-toan/data-2/input3.json"; // Dữ liệu đầu vào

const Schedule = () => {
    const [selectedOperation, setSelectedOperation] = useState("All");

    // Tạo danh sách header từ dữ liệu đăng ký
    const generateHeaders = (data) => {
        return data.flatMap((daySchedule) =>
            Array.from({ length: daySchedule.shift_count }).map(
                (_, shiftIndex) => ({
                    date: daySchedule.date,
                    shift: `Ca ${shiftIndex + 1}`,
                })
            )
        );
    };

    // Tạo danh sách nhân viên từ dữ liệu đăng ký
    const generateWorkers = (data) => {
        const workers = new Set();
        data.forEach((daySchedule) => {
            Object.keys(daySchedule.schedule).forEach((workerId) =>
                workers.add(workerId)
            );
        });
        return Array.from(workers);
    };

    // Tìm công đoạn được phân công cho nhân viên theo ngày và ca
    const findAssignedOperation = (workerId, date, shiftIndex) => {
        for (const operation of assignedSchedule) {
            for (const detail of operation.detailed_schedule) {
                if (
                    detail.worker_id === workerId &&
                    detail.day === date &&
                    detail.shift === shiftIndex + 1
                ) {
                    return operation.id; // Trả về ID của công đoạn (ví dụ: OP001)
                }
            }
        }
        return null; // Không tìm thấy công đoạn nào
    };

    // Lấy danh sách công đoạn từ dữ liệu đầu vào
    const getOperations = () => {
        return [
            "All",
            ...inputData.operations.map((op) => ({
                id: op.id,
                name: op.name,
                requiredPosition: op.requiredPosition,
            })),
        ];
    };

    // Lọc nhân viên theo công đoạn được chọn
    const getWorkersByOperation = (selectedOp) => {
        if (selectedOp === "All") {
            return generateWorkers(monthlySchedule);
        }

        const operation = inputData.operations.find(
            (op) => op.id === selectedOp
        );
        if (!operation) {
            return [];
        }

        const allWorkers = generateWorkers(monthlySchedule);
        // Lọc nhân viên có position khớp với requiredPosition của công đoạn
        return inputData.workers
            .filter((worker) => worker.position === operation.requiredPosition)
            .map((worker) => worker.id)
            .filter((workerId) => allWorkers.includes(workerId)); // Chỉ lấy những worker có trong schedule
    };

    // Lấy danh sách máy theo loại máy yêu cầu của công đoạn
    const getMachinesByOperation = (selectedOp) => {
        if (selectedOp === "All") {
            return [];
        }

        const operation = inputData.operations.find(
            (op) => op.id === selectedOp
        );
        if (!operation) {
            return [];
        }

        // Lọc máy có machineType khớp với requiredMachineType của công đoạn
        return inputData.assets.filter(
            (asset) => asset.machineType === operation.requiredMachineType
        );
    };

    // Tìm nhân viên sử dụng máy theo ngày và ca
    const findWorkerUsingMachine = (assetId, date, shiftIndex) => {
        for (const operation of assignedSchedule) {
            for (const detail of operation.detailed_schedule) {
                if (
                    detail.asset_id === assetId &&
                    detail.day === date &&
                    detail.shift === shiftIndex + 1
                ) {
                    return detail.worker_id; // Trả về ID của nhân viên
                }
            }
        }
        return null; // Không có nhân viên nào sử dụng máy này
    };

    const headers = generateHeaders(monthlySchedule);
    const allWorkers = generateWorkers(monthlySchedule);
    const filteredWorkers = getWorkersByOperation(selectedOperation);
    const filteredMachines = getMachinesByOperation(selectedOperation);
    const operations = getOperations();

    return (
        <div className="schedule-container">
            <div className="filter-container" style={{ marginBottom: "20px" }}>
                <label htmlFor="operation-select">Lọc theo công đoạn: </label>
                <select
                    id="operation-select"
                    value={selectedOperation}
                    onChange={(e) => setSelectedOperation(e.target.value)}
                    style={{ marginLeft: "10px", padding: "5px" }}
                >
                    {operations.map((operation) => (
                        <option
                            key={operation === "All" ? "All" : operation.id}
                            value={operation === "All" ? "All" : operation.id}
                        >
                            {operation === "All"
                                ? "Tất cả"
                                : `${operation.id} - ${operation.name} (${operation.requiredPosition})`}
                        </option>
                    ))}
                </select>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>Nhân viên</th>
                        {headers.map((header, index) => (
                            <th key={index}>
                                {header.date} <br /> {header.shift}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {filteredWorkers.map((workerId) => (
                        <tr key={workerId}>
                            <td>{workerId}</td>
                            {headers.map((header, index) => {
                                const shiftIndex =
                                    parseInt(header.shift.split(" ")[1]) - 1;
                                const isRegistered =
                                    monthlySchedule.find(
                                        (day) => day.date === header.date
                                    )?.schedule[workerId]?.[shiftIndex] === 1;

                                const assignedOperation = findAssignedOperation(
                                    workerId,
                                    header.date,
                                    shiftIndex
                                );

                                return (
                                    <td
                                        key={index}
                                        style={{
                                            backgroundColor: assignedOperation
                                                ? "#e8f5e8"
                                                : isRegistered
                                                ? "#fff3cd"
                                                : "#f8f9fa",
                                            textAlign: "center",
                                            border: "1px solid #dee2e6",
                                            padding: "8px",
                                        }}
                                    >
                                        {assignedOperation
                                            ? assignedOperation
                                            : isRegistered
                                            ? "Đăng ký"
                                            : ""}
                                    </td>
                                );
                            })}
                        </tr>
                    ))}
                </tbody>
            </table>

            {filteredWorkers.length === 0 && selectedOperation !== "All" && (
                <div
                    style={{
                        marginTop: "20px",
                        textAlign: "center",
                        color: "#666",
                    }}
                >
                    Không có nhân viên nào phù hợp với công đoạn được chọn
                </div>
            )}

            {/* Bảng lịch máy móc */}
            {selectedOperation !== "All" && filteredMachines.length > 0 && (
                <div style={{ marginTop: "40px" }}>
                    <h3>
                        Lịch máy móc -{" "}
                        {
                            inputData.operations.find(
                                (op) => op.id === selectedOperation
                            )?.requiredMachineType
                        }
                    </h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Máy móc</th>
                                {headers.map((header, index) => (
                                    <th key={index}>
                                        {header.date} <br /> {header.shift}
                                    </th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {filteredMachines.map((machine) => (
                                <tr key={machine.id}>
                                    <td style={{ fontWeight: "bold" }}>
                                        {machine.id}
                                    </td>
                                    {headers.map((header, index) => {
                                        const shiftIndex =
                                            parseInt(
                                                header.shift.split(" ")[1]
                                            ) - 1;

                                        const workerUsing =
                                            findWorkerUsingMachine(
                                                machine.id,
                                                header.date,
                                                shiftIndex
                                            );

                                        return (
                                            <td
                                                key={index}
                                                style={{
                                                    backgroundColor: workerUsing
                                                        ? "#e8f5e8"
                                                        : "#f8f9fa",
                                                    textAlign: "center",
                                                    border: "1px solid #dee2e6",
                                                    padding: "8px",
                                                    fontSize: "12px",
                                                }}
                                            >
                                                {workerUsing || ""}
                                            </td>
                                        );
                                    })}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default Schedule;
