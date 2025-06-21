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
import nhanvienthongkeData from "../../thuat-toan/out/nhanvienthongke.json";

const WorkerAnalysis = () => {
    // State để lưu loại nhân viên được chọn
    const [selectedWorkerType, setSelectedWorkerType] = useState(
        nhanvienthongkeData[0]?.workerTypeName || ""
    );

    // Dữ liệu cho Bar Chart 1: Tỷ lệ thời gian sử dụng loại nhân viên theo công đoạn
    const overviewChartData = nhanvienthongkeData.map((item) => ({
        workerTypeName: item.workerTypeName,
        total_time_operations: item.total_time_operations,
    }));

    // Dữ liệu cho loại nhân viên được chọn
    const selectedWorkerData = nhanvienthongkeData.find(
        (item) => item.workerTypeName === selectedWorkerType
    );

    // Dữ liệu cho Pie Chart: Tỷ lệ nhân viên làm việc vs rảnh
    const pieChartData = selectedWorkerData
        ? [
              {
                  name: "Nhân viên đang làm việc",
                  value:
                      selectedWorkerData.total_workers -
                      selectedWorkerData.idleWorkers,
                  color: "#8884d8",
              },
              {
                  name: "Nhân viên rảnh",
                  value: selectedWorkerData.idleWorkers,
                  color: "#82ca9d",
              },
          ]
        : [];

    // Dữ liệu cho Bar Chart 2: Thời gian làm việc của từng nhân viên
    const workerDetailChartData = selectedWorkerData
        ? Object.entries(selectedWorkerData.workers).map(
              ([workerId, shifts]) => ({
                  workerId,
                  shifts,
              })
          )
        : [];

    // Màu sắc cho Pie Chart
    const COLORS = ["#8884d8", "#82ca9d"];

    return (
        <div style={{ padding: "20px" }}>
            <h1>Phân tích nhân viên</h1>

            {/* Bar Chart 1: Tổng quan thời gian làm việc theo loại nhân viên */}
            <div style={{ marginBottom: "40px" }}>
                <h2>Thời gian làm việc theo loại nhân viên</h2>
                <ResponsiveContainer width="100%" height={400}>
                    <BarChart data={overviewChartData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis
                            dataKey="workerTypeName"
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
                            name="Thời gian làm việc (công đoạn)"
                        />
                    </BarChart>
                </ResponsiveContainer>
            </div>

            {/* Bộ lọc loại nhân viên */}
            <div style={{ marginBottom: "20px" }}>
                <label htmlFor="worker-type-select">
                    Chọn loại nhân viên:{" "}
                </label>
                <select
                    id="worker-type-select"
                    value={selectedWorkerType}
                    onChange={(e) => setSelectedWorkerType(e.target.value)}
                    style={{ padding: "5px", fontSize: "16px" }}
                >
                    {nhanvienthongkeData.map((item) => (
                        <option
                            key={item.workerTypeName}
                            value={item.workerTypeName}
                        >
                            {item.workerTypeName}
                        </option>
                    ))}
                </select>
            </div>

            <div style={{ display: "flex", gap: "40px", flexWrap: "wrap" }}>
                {/* Pie Chart: Tỷ lệ nhân viên làm việc vs rảnh */}
                <div style={{ flex: "1", minWidth: "400px" }}>
                    <h2>Tỷ lệ nhân viên làm việc vs rảnh</h2>
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
                    {selectedWorkerData && (
                        <div style={{ marginTop: "10px", fontSize: "14px" }}>
                            <p>
                                <strong>Tổng số nhân viên:</strong>{" "}
                                {selectedWorkerData.total_workers}
                            </p>
                            <p>
                                <strong>Nhân viên đang làm việc:</strong>{" "}
                                {selectedWorkerData.total_workers -
                                    selectedWorkerData.idleWorkers}
                            </p>
                            <p>
                                <strong>Nhân viên rảnh:</strong>{" "}
                                {selectedWorkerData.idleWorkers}
                            </p>
                        </div>
                    )}
                </div>

                {/* Bar Chart 2: Thời gian làm việc của từng nhân viên */}
                <div style={{ flex: "1", minWidth: "600px" }}>
                    <h2>Thời gian làm việc của từng nhân viên (số ca)</h2>
                    <ResponsiveContainer width="100%" height={400}>
                        <BarChart data={workerDetailChartData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis
                                dataKey="workerId"
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
                                name="Số ca làm việc"
                            />
                        </BarChart>
                    </ResponsiveContainer>
                    {selectedWorkerData && (
                        <div style={{ marginTop: "10px", fontSize: "14px" }}>
                            <p>
                                <strong>Nhân viên làm việc nhiều nhất:</strong>{" "}
                                {selectedWorkerData.max_shift_worker}
                            </p>
                            <p>
                                <strong>Tổng số ca:</strong>{" "}
                                {selectedWorkerData.total_shifts}
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default WorkerAnalysis;
