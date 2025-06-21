import React, { useState } from "react";
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
    PieChart,
    Pie,
    Cell,
} from "recharts";
import maymocthongkeData from "../../thuat-toan/out/maymocthongke.json";
import machineCommandSwitchesData from "../../thuat-toan/out/machine_command_switches.json";

const MachineAnalysis = () => {
    // State để lưu loại máy được chọn
    const [selectedMachineType, setSelectedMachineType] = useState(
        maymocthongkeData[0]?.machineTypeName || ""
    );

    // Dữ liệu cho Bar Chart 1: Tỷ lệ thời gian sử dụng loại máy theo công đoạn
    const overviewChartData = maymocthongkeData.map((item) => ({
        machineTypeName: item.machineTypeName,
        total_time_operations: item.total_time_operations,
    }));

    // Dữ liệu cho loại máy được chọn
    const selectedMachineData = maymocthongkeData.find(
        (item) => item.machineTypeName === selectedMachineType
    );

    // Dữ liệu cho Pie Chart: Tỷ lệ máy sử dụng vs rảnh
    const pieChartData = selectedMachineData
        ? [
              {
                  name: "Máy đang sử dụng",
                  value:
                      selectedMachineData.total_machines -
                      selectedMachineData.idleMachines,
                  color: "#8884d8",
              },
              {
                  name: "Máy rảnh",
                  value: selectedMachineData.idleMachines,
                  color: "#82ca9d",
              },
          ]
        : [];

    // Dữ liệu cho Bar Chart 2: Thời gian sử dụng của từng máy
    const machineDetailChartData = selectedMachineData
        ? Object.entries(selectedMachineData.machines).map(
              ([machineId, shifts]) => ({
                  machineId,
                  shifts,
              })
          )
        : [];

    // Màu sắc cho Pie Chart
    const COLORS = ["#8884d8", "#82ca9d"];

    return (
        <div style={{ padding: "20px" }}>
            <h1>Phân tích máy móc</h1>

            {/* Bar Chart 1: Tổng quan thời gian sử dụng theo loại máy */}
            <div style={{ marginBottom: "40px" }}>
                <h2>Thời gian sử dụng theo loại máy</h2>
                <ResponsiveContainer width="100%" height={400}>
                    <BarChart data={overviewChartData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis
                            dataKey="machineTypeName"
                            angle={-45}
                            textAnchor="end"
                            height={100}
                        />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar
                            dataKey="total_time_operations"
                            fill="#8884d8"
                            name="Thời gian sử dụng (công đoạn)"
                        />
                    </BarChart>
                </ResponsiveContainer>
            </div>

            {/* Bộ lọc loại máy */}
            <div style={{ marginBottom: "20px" }}>
                <label htmlFor="machine-type-select">Chọn loại máy: </label>
                <select
                    id="machine-type-select"
                    value={selectedMachineType}
                    onChange={(e) => setSelectedMachineType(e.target.value)}
                    style={{ padding: "5px", fontSize: "16px" }}
                >
                    {maymocthongkeData.map((item) => (
                        <option
                            key={item.machineTypeName}
                            value={item.machineTypeName}
                        >
                            {item.machineTypeName}
                        </option>
                    ))}
                </select>
            </div>

            <div style={{ display: "flex", gap: "40px", flexWrap: "wrap" }}>
                {/* Pie Chart: Tỷ lệ máy sử dụng vs rảnh */}
                <div style={{ flex: "1", minWidth: "400px" }}>
                    <h2>Tỷ lệ máy sử dụng vs rảnh</h2>
                    <ResponsiveContainer width="100%" height={400}>
                        <PieChart>
                            <Pie
                                data={pieChartData}
                                cx="50%"
                                cy="50%"
                                labelLine={false}
                                label={({ name, value, percent }) =>
                                    `${name}: ${value} (${(
                                        percent * 100
                                    ).toFixed(1)}%)`
                                }
                                outerRadius={120}
                                fill="#8884d8"
                                dataKey="value"
                            >
                                {pieChartData.map((entry, index) => (
                                    <Cell
                                        key={`cell-${index}`}
                                        fill={COLORS[index % COLORS.length]}
                                    />
                                ))}
                            </Pie>
                            <Tooltip />
                            <Legend />
                        </PieChart>
                    </ResponsiveContainer>
                    {selectedMachineData && (
                        <div style={{ marginTop: "10px", fontSize: "14px" }}>
                            <p>
                                <strong>Tổng số máy:</strong>{" "}
                                {selectedMachineData.total_machines}
                            </p>
                            <p>
                                <strong>Máy đang sử dụng:</strong>{" "}
                                {selectedMachineData.total_machines -
                                    selectedMachineData.idleMachines}
                            </p>
                            <p>
                                <strong>Máy rảnh:</strong>{" "}
                                {selectedMachineData.idleMachines}
                            </p>
                        </div>
                    )}
                </div>

                {/* Bar Chart 2: Thời gian sử dụng của từng máy */}
                <div style={{ flex: "1", minWidth: "600px" }}>
                    <h2>Thời gian sử dụng của từng máy (số ca)</h2>
                    <ResponsiveContainer width="100%" height={400}>
                        <BarChart data={machineDetailChartData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis
                                dataKey="machineId"
                                angle={-45}
                                textAnchor="end"
                                height={80}
                            />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar
                                dataKey="shifts"
                                fill="#82ca9d"
                                name="Số ca sử dụng"
                            />
                        </BarChart>
                    </ResponsiveContainer>
                    {selectedMachineData && (
                        <div style={{ marginTop: "10px", fontSize: "14px" }}>
                            <p>
                                <strong>Máy sử dụng nhiều nhất:</strong>{" "}
                                {selectedMachineData.max_shift_machine}
                            </p>
                            <p>
                                <strong>Tổng số ca:</strong>{" "}
                                {selectedMachineData.total_shifts}
                            </p>
                        </div>
                    )}
                </div>
            </div>

            {/* Bảng thống kê số lần chuyển lệnh của từng máy */}
            <div style={{ marginTop: "40px" }}>
                <h2>Thống kê số lần chuyển lệnh của từng máy</h2>
                {selectedMachineData && (
                    <div style={{ overflowX: "auto" }}>
                        <table
                            style={{
                                width: "100%",
                                borderCollapse: "collapse",
                                marginTop: "20px",
                                border: "1px solid #ddd",
                            }}
                        >
                            <thead>
                                <tr style={{ backgroundColor: "#f4f4f4" }}>
                                    <th
                                        style={{
                                            border: "1px solid #ddd",
                                            padding: "10px",
                                            textAlign: "left",
                                        }}
                                    >
                                        Mã máy
                                    </th>
                                    <th
                                        style={{
                                            border: "1px solid #ddd",
                                            padding: "10px",
                                            textAlign: "center",
                                        }}
                                    >
                                        Tổng số lệnh tham gia
                                    </th>
                                    <th
                                        style={{
                                            border: "1px solid #ddd",
                                            padding: "10px",
                                            textAlign: "center",
                                        }}
                                    >
                                        Số lần di chuyển
                                    </th>
                                    <th
                                        style={{
                                            border: "1px solid #ddd",
                                            padding: "10px",
                                            textAlign: "center",
                                        }}
                                    >
                                        Tổng số ca làm việc
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                {Object.keys(selectedMachineData.machines)
                                    .map((machineId) => {
                                        const machineInfo =
                                            machineCommandSwitchesData.machines[
                                                machineId
                                            ];
                                        return {
                                            machineId,
                                            shifts: selectedMachineData
                                                .machines[machineId],
                                            totalCommands:
                                                machineInfo?.total_commands_participated ||
                                                0,
                                            commandSwitches:
                                                machineInfo?.command_switches ||
                                                0,
                                            totalActivities:
                                                machineInfo?.activities
                                                    ?.length || 0,
                                        };
                                    })
                                    .sort((a, b) => b.shifts - a.shifts) // Sắp xếp theo số ca giảm dần
                                    .map((machine, index) => (
                                        <tr
                                            key={machine.machineId}
                                            style={{
                                                backgroundColor:
                                                    index % 2 === 0
                                                        ? "#f9f9f9"
                                                        : "#ffffff",
                                                display:
                                                    machine.totalCommands <= 0
                                                        ? "none"
                                                        : "",
                                            }}
                                        >
                                            <td
                                                style={{
                                                    border: "1px solid #ddd",
                                                    padding: "10px",
                                                    fontWeight: "bold",
                                                }}
                                            >
                                                {machine.machineId}
                                            </td>
                                            <td
                                                style={{
                                                    border: "1px solid #ddd",
                                                    padding: "10px",
                                                    textAlign: "center",
                                                }}
                                            >
                                                {machine.totalCommands}
                                            </td>
                                            <td
                                                style={{
                                                    border: "1px solid #ddd",
                                                    padding: "10px",
                                                    textAlign: "center",
                                                    color:
                                                        machine.commandSwitches >
                                                        0
                                                            ? "#ff6b6b"
                                                            : "#51cf66",
                                                }}
                                            >
                                                {machine.commandSwitches}
                                            </td>
                                            <td
                                                style={{
                                                    border: "1px solid #ddd",
                                                    padding: "10px",
                                                    textAlign: "center",
                                                }}
                                            >
                                                {machine.totalActivities}
                                            </td>
                                        </tr>
                                    ))}
                            </tbody>
                        </table>

                        {/* Thống kê tổng quan */}
                        <div
                            style={{
                                marginTop: "20px",
                                padding: "15px",
                                backgroundColor: "#f8f9fa",
                                borderRadius: "5px",
                                border: "1px solid #e9ecef",
                            }}
                        >
                            <h4 style={{ marginTop: 0 }}>
                                Thống kê tổng quan cho {selectedMachineType}
                            </h4>
                            <div
                                style={{
                                    display: "grid",
                                    gridTemplateColumns:
                                        "repeat(auto-fit, minmax(200px, 1fr))",
                                    gap: "15px",
                                }}
                            >
                                <div>
                                    <strong>Tổng số máy:</strong>{" "}
                                    {
                                        Object.keys(
                                            selectedMachineData.machines
                                        ).length
                                    }
                                </div>
                                <div>
                                    <strong>Máy có chuyển lệnh:</strong>{" "}
                                    {
                                        Object.keys(
                                            selectedMachineData.machines
                                        ).filter((machineId) => {
                                            const machineInfo =
                                                machineCommandSwitchesData
                                                    .machines[machineId];
                                            return (
                                                machineInfo?.command_switches >
                                                0
                                            );
                                        }).length
                                    }
                                </div>
                                <div>
                                    <strong>Tổng lần chuyển lệnh:</strong>{" "}
                                    {Object.keys(
                                        selectedMachineData.machines
                                    ).reduce((total, machineId) => {
                                        const machineInfo =
                                            machineCommandSwitchesData.machines[
                                                machineId
                                            ];
                                        return (
                                            total +
                                            (machineInfo?.command_switches || 0)
                                        );
                                    }, 0)}
                                </div>
                                <div>
                                    <strong>Trung bình chuyển lệnh/máy:</strong>{" "}
                                    {(
                                        Object.keys(
                                            selectedMachineData.machines
                                        ).reduce((total, machineId) => {
                                            const machineInfo =
                                                machineCommandSwitchesData
                                                    .machines[machineId];
                                            return (
                                                total +
                                                (machineInfo?.command_switches ||
                                                    0)
                                            );
                                        }, 0) /
                                        Object.keys(
                                            selectedMachineData.machines
                                        ).length
                                    ).toFixed(2)}
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default MachineAnalysis;
