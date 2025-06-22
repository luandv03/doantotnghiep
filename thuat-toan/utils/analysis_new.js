const fs = require("fs");
const path = require("path");

const scheduleData = require("../out/out3/input9_2/schedule.json");
const assetsData = require("../data-2/input9_2.json");
const workersData = require("../data-2/input9_2.json");

const outputData1 = "thuat-toan/out/out3/input9_2/maymocthongke.json";
const outputData2 = "thuat-toan/out/out3/input9_2/nhanvienthongke.json";

/**
 * Đếm số ca làm việc của một máy cụ thể.
 *
 * @param {string} machineId - ID của máy cần đếm ca làm việc
 * @param {string|null} schedulePath - Đường dẫn đến file schedule.json
 * @returns {number} Số ca làm việc
 */
function countMachineShifts(machineId, scheduleData = null) {
    try {
        // Đọc dữ liệu từ file schedule.json
        const operationsData = scheduleData;

        // Đếm số ca làm việc của máy
        let shiftCount = 0;
        for (const operation of operationsData) {
            if (
                operation.detailed_schedule &&
                Array.isArray(operation.detailed_schedule)
            ) {
                for (const shiftEntry of operation.detailed_schedule) {
                    if (
                        shiftEntry.asset_id &&
                        shiftEntry.asset_id === machineId
                    ) {
                        shiftCount += 1;
                    }
                }
            }
        }

        return shiftCount;
    } catch (error) {
        return 0;
    }
}

/**
 * Lấy danh sách N máy có số ca làm việc nhiều nhất.
 *
 * @param {number} topN - Số lượng máy muốn lấy
 * @param {string|null} schedulePath - Đường dẫn đến file schedule.json
 * @returns {Array} Danh sách các array [machine_id, shift_count] đã sắp xếp
 */
function getTopUtilizedMachines(topN = 10, scheduleData = null) {
    try {
        // Đọc dữ liệu từ file schedule.json
        const operationsData = scheduleData;

        // Thu thập tất cả ID máy móc duy nhất
        const machineIds = new Set();
        for (const operation of operationsData) {
            if (
                operation.detailed_schedule &&
                Array.isArray(operation.detailed_schedule)
            ) {
                for (const shiftEntry of operation.detailed_schedule) {
                    if (shiftEntry.asset_id) {
                        machineIds.add(shiftEntry.asset_id);
                    }
                }
            }
        }

        // Đếm số ca làm việc cho mỗi máy
        const machineUtilization = {};
        for (const machineId of machineIds) {
            machineUtilization[machineId] = countMachineShifts(
                machineId,
                scheduleData
            );
        }

        // Sắp xếp theo số ca làm việc giảm dần và lấy top N
        const topMachines = Object.entries(machineUtilization)
            .sort((a, b) => b[1] - a[1])
            .slice(0, topN);

        return topMachines;
    } catch (error) {
        console.log(`Lỗi: ${error.message}`);
        return [];
    }
}

/**
 * Lấy thông tin về các loại máy từ file assets và schedule.
 *
 * @param {string|null} schedulePath - Đường dẫn đến file schedule.json
 * @param {string|null} assetsPath - Đường dẫn đến file input có thông tin máy móc
 * @returns {Object} Object với key là machine_id và value là machine_type
 */
function getMachineTypes(scheduleData = null, assetsData = null) {
    try {
        // Đọc dữ liệu từ file assets
        const inputData = assetsData;

        // Tạo mapping từ machine_id đến machine_type
        const machineTypes = {};
        if (inputData.assets && Array.isArray(inputData.assets)) {
            for (const asset of inputData.assets) {
                if (asset.id && asset.machineType) {
                    machineTypes[asset.id] = asset.machineType;
                }
            }
        }

        return machineTypes;
    } catch (error) {
        console.log(`Lỗi khi đọc thông tin máy móc: ${error.message}`);
        return {};
    }
}

/**
 * Lấy danh sách tất cả các máy móc có trong hệ thống, kể cả chưa được gán việc.
 *
 * @param {string|null} assetsPath - Đường dẫn đến file input có thông tin máy móc
 * @returns {Object} Object với key là machine_id và value là thông tin máy
 */
function getAllMachines(assetData = null) {
    try {
        // Đọc dữ liệu từ file assets
        const inputData = assetData;

        // Lấy tất cả máy móc
        const machines = {};
        if (inputData.assets && Array.isArray(inputData.assets)) {
            for (const asset of inputData.assets) {
                if (asset.id) {
                    machines[asset.id] = asset;
                }
            }
        }

        return machines;
    } catch (error) {
        console.log(`Lỗi khi đọc thông tin máy móc: ${error.message}`);
        return {};
    }
}

/**
 * Tính tổng thời gian hoạt động bằng cách tạo union của các khoảng thời gian để tránh double-counting
 * @param {Array} timeRanges - Mảng các object {day, shift}
 * @returns {number} Tổng số ca làm việc duy nhất
 */
function calculateTimeRangeUnion(timeRanges) {
    if (!timeRanges || timeRanges.length === 0) {
        return 0;
    }

    // Tạo Set để lưu các shift duy nhất (day-shift combination)
    const uniqueShifts = new Set();

    for (const range of timeRanges) {
        if (range.day && range.shift) {
            const shiftKey = `${range.day}-${range.shift}`;
            uniqueShifts.add(shiftKey);
        }
    }

    return uniqueShifts.size;
}

/**
 * Tính số ca làm việc của mỗi loại máy theo requiredMachineType và từng máy cụ thể.
 * Tổng số ca làm việc của mỗi loại máy được tính bằng time range union để tránh double-counting.
 *
 * @param {string|null} schedulePath - Đường dẫn đến file schedule.json
 * @param {string|null} assetsPath - Đường dẫn đến file input có thông tin máy móc
 * @param {boolean} includeUnassigned - Có hiển thị máy chưa được gán việc hay không
 * @returns {Object} Object với key là loại máy và value là object thống kê
 */
function countMachineTypeShifts(
    scheduleData = null,
    assetsData = null,
    includeUnassigned = true
) {
    try {
        // Đọc dữ liệu từ file schedule.json
        const operationsData = scheduleData;

        // Đọc dữ liệu từ file input9.json để lấy thông tin operations và assets
        const inputData = assetsData;

        // Tạo mapping từ operation id sang requiredMachineType
        const operationToMachineType = {};
        if (inputData.operations) {
            for (const op of inputData.operations) {
                operationToMachineType[op.id] =
                    op.requiredMachineType || "Không xác định";
            }
        }

        // Lấy thông tin loại máy từ assets
        const machineTypes = getMachineTypes(scheduleData, assetsData);
        const allMachines = includeUnassigned ? getAllMachines(assetsData) : {};

        // Tổng hợp dữ liệu theo requiredMachineType
        const machineTypeStats = {};
        const machineTypeTimeRanges = {}; // Lưu time ranges cho mỗi machine type

        // Đếm số ca làm việc cho mỗi máy và tổng hợp theo requiredMachineType
        const machineShifts = {};

        for (const operation of operationsData) {
            const requiredMachineType =
                operationToMachineType[operation.id] || "Không xác định";

            if (
                operation.detailed_schedule &&
                Array.isArray(operation.detailed_schedule)
            ) {
                // Khởi tạo machine type stats nếu chưa có
                if (!machineTypeStats[requiredMachineType]) {
                    machineTypeStats[requiredMachineType] = {
                        total_machines: 0,
                        total_shifts: 0,
                        total_time_operations: 0,
                        max_shift_machine: "",
                        machines: {},
                    };
                    machineTypeTimeRanges[requiredMachineType] = [];
                }

                // Thu thập time ranges cho machine type này
                for (const shiftEntry of operation.detailed_schedule) {
                    if (
                        shiftEntry.asset_id &&
                        shiftEntry.day &&
                        shiftEntry.shift
                    ) {
                        // Đếm shifts cho từng máy cụ thể
                        machineShifts[shiftEntry.asset_id] =
                            (machineShifts[shiftEntry.asset_id] || 0) + 1;

                        // Thu thập time range cho machine type
                        machineTypeTimeRanges[requiredMachineType].push({
                            day: shiftEntry.day,
                            shift: shiftEntry.shift,
                        });
                    }
                }
            }
        }

        // Tính total_time_operations cho mỗi machine type bằng time range union
        for (const [machineType, timeRanges] of Object.entries(
            machineTypeTimeRanges
        )) {
            machineTypeStats[machineType].total_time_operations =
                calculateTimeRangeUnion(timeRanges);
        }

        // Thêm tất cả máy móc vào thống kê, nhóm theo machine type của chúng
        if (includeUnassigned) {
            for (const [machineId, machineInfo] of Object.entries(
                allMachines
            )) {
                const actualMachineType =
                    machineInfo.machineType || "Không xác định";

                // Tìm requiredMachineType tương ứng với actualMachineType này
                // Nếu không có operation nào yêu cầu loại máy này, vẫn tạo entry
                if (!machineTypeStats[actualMachineType]) {
                    machineTypeStats[actualMachineType] = {
                        total_machines: 0,
                        total_shifts: 0,
                        total_time_operations: 0,
                        max_shift_machine: "",
                        machines: {},
                    };
                }

                if (!(machineId in machineShifts)) {
                    machineShifts[machineId] = 0; // Ghi nhận là có 0 ca làm việc
                }
            }
        }

        // Cập nhật thống kê cho từng máy theo machine type thực tế của chúng
        for (const [machineId, shiftCount] of Object.entries(machineShifts)) {
            const actualMachineType =
                allMachines[machineId]?.machineType ||
                machineTypes[machineId] ||
                "Không xác định";

            // Đảm bảo machine type này có trong stats
            if (!machineTypeStats[actualMachineType]) {
                machineTypeStats[actualMachineType] = {
                    total_machines: 0,
                    total_shifts: 0,
                    total_time_operations: 0,
                    max_shift_machine: "",
                    machines: {},
                };
            }

            // Cập nhật thông tin cho loại máy này
            machineTypeStats[actualMachineType].machines[machineId] =
                shiftCount;

            // Cập nhật số ca tối đa cho loại máy
            if (shiftCount > machineTypeStats[actualMachineType].total_shifts) {
                machineTypeStats[actualMachineType].total_shifts = shiftCount;
                machineTypeStats[actualMachineType].max_shift_machine =
                    machineId;
            }
        }

        // Tính tổng số máy cho mỗi loại
        for (const machineType of Object.keys(machineTypeStats)) {
            machineTypeStats[machineType].total_machines = Object.keys(
                machineTypeStats[machineType].machines
            ).length;
        }

        return machineTypeStats;
    } catch (error) {
        console.log(`Lỗi: ${error.message}`);
        return {};
    }
}

/**
 * In ra thống kê về số ca làm việc của mỗi loại máy và từng máy cụ thể.
 *
 * @param {string|null} schedulePath - Đường dẫn đến file schedule.json
 * @param {string|null} assetsPath - Đường dẫn đến file input có thông tin máy móc
 * @param {boolean} includeUnassigned - Có hiển thị máy chưa được gán việc hay không
 * @param {boolean} showZeroShifts - Có hiển thị các máy có 0 ca làm việc hay không
 */
function printMachineTypeStatistics(
    scheduleData = null,
    assetsData = null,
    includeUnassigned = true,
    showZeroShifts = true
) {
    const stats = countMachineTypeShifts(
        scheduleData,
        assetsData,
        includeUnassigned
    );

    if (Object.keys(stats).length === 0) {
        console.log("Không có dữ liệu thống kê.");
        return;
    }

    console.log("\n===== THỐNG KÊ CA LÀM VIỆC THEO LOẠI MÁY =====\n");

    // Sắp xếp theo tổng số ca làm việc giảm dần
    const sortedStats = Object.entries(stats).sort(
        (a, b) => b[1].total_shifts - a[1].total_shifts
    );

    // Chuyển đổi sang định dạng mong muốn với total_time_operations
    const formattedOutput = sortedStats.map(([machineTypeName, data]) => {
        // Tính số máy idle (không có ca làm việc)
        const idleMachines = Object.values(data.machines).filter(
            (shifts) => shifts === 0
        ).length;

        return {
            machineTypeName: machineTypeName,
            total_time_operations: data.total_time_operations || 0,
            total_machines: data.total_machines,
            total_shifts: data.total_shifts,
            max_shift_machine: data.max_shift_machine,
            machines: data.machines,
            idleMachines: idleMachines,
        };
    });

    return formattedOutput;
}

/**
 * Lấy thông tin về các loại nhân viên từ file input.
 *
 * @param {string|null} schedulePath - Đường dẫn đến file schedule.json
 * @param {string|null} workersPath - Đường dẫn đến file input có thông tin nhân viên (input6.json)
 * @returns {Object} Object với key là worker_id và value là worker_type (position)
 */
function getWorkerTypes(scheduleData = null, workersData = null) {
    try {
        // Đọc dữ liệu từ file input chứa thông tin nhân viên
        const inputData = workersData;

        // Tạo mapping từ worker_id đến worker_type (position)
        const workerTypes = {};

        // File input có trường workers
        if (inputData.workers && Array.isArray(inputData.workers)) {
            for (const worker of inputData.workers) {
                if (worker.id) {
                    // Lấy thông tin position nếu có, mặc định là "Không xác định"
                    if (worker.position) {
                        workerTypes[worker.id] = worker.position;
                    }
                    // Nếu không có position nhưng có workerType
                    else if (worker.workerType) {
                        workerTypes[worker.id] = worker.workerType;
                    } else {
                        workerTypes[worker.id] = "Không xác định";
                    }
                }
            }
        }

        // Nếu không tìm thấy thông tin nhân viên từ file input, thu thập từ schedule
        if (Object.keys(workerTypes).length === 0) {
            // Lấy ID nhân viên từ schedule
            const operationsData = scheduleData;

            const workerIds = new Set();
            for (const operation of operationsData) {
                if (
                    operation.detailed_schedule &&
                    Array.isArray(operation.detailed_schedule)
                ) {
                    for (const shiftEntry of operation.detailed_schedule) {
                        if (shiftEntry.worker_id) {
                            workerIds.add(shiftEntry.worker_id);
                        }
                    }
                }
            }

            // Tạo mapping với thông tin mặc định
            for (const workerId of workerIds) {
                // Phân loại dựa trên ID (phương án dự phòng)
                if (workerId.startsWith("W0")) {
                    const workerNumber = parseInt(workerId.slice(1));
                    if (workerNumber <= 200) {
                        workerTypes[workerId] = "Công nhân sản xuất";
                    } else if (workerNumber <= 300) {
                        workerTypes[workerId] = "Kỹ thuật viên";
                    } else if (workerNumber <= 400) {
                        workerTypes[workerId] = "Quản đốc phân xưởng";
                    } else if (workerNumber <= 500) {
                        workerTypes[workerId] = "Nhân viên bảo trì";
                    } else {
                        workerTypes[workerId] = "Nhân viên hỗ trợ";
                    }
                } else {
                    workerTypes[workerId] = "Không xác định";
                }
            }
        }

        return workerTypes;
    } catch (error) {
        console.log(`Lỗi khi đọc thông tin nhân viên: ${error.message}`);
        return {};
    }
}

/**
 * Lấy danh sách tất cả các nhân viên có trong hệ thống, bao gồm cả từ lịch làm việc thực tế.
 *
 * @param {string|null} workersPath - Đường dẫn đến file input có thông tin nhân viên (input6.json)
 * @param {string|null} schedulePath - Đường dẫn đến file schedule.json để trích xuất thông tin nhân viên bổ sung
 * @returns {Object} Object với key là worker_id và value là thông tin nhân viên
 */
function getAllWorkers(workersData = null, scheduleData = null) {
    const workers = {};

    try {
        // Đọc thông tin nhân viên từ file input nếu có
        if (workersData) {
            const inputData = workersData;

            // File input có trường workers
            if (inputData.workers && Array.isArray(inputData.workers)) {
                for (const worker of inputData.workers) {
                    if (worker.id) {
                        workers[worker.id] = worker;
                    }
                }
            }
        }

        // Bổ sung thông tin nhân viên từ lịch làm việc thực tế
        if (scheduleData) {
            const operationsData = JSON.parse(scheduleContent);

            // Lấy worker_types để bổ sung thông tin
            const workerTypes = getWorkerTypes(scheduleData, workersData);

            for (const operation of operationsData) {
                if (
                    operation.detailed_schedule &&
                    Array.isArray(operation.detailed_schedule)
                ) {
                    for (const shiftEntry of operation.detailed_schedule) {
                        if (shiftEntry.worker_id) {
                            const workerId = shiftEntry.worker_id;
                            if (!(workerId in workers)) {
                                workers[workerId] = {
                                    id: workerId,
                                    position:
                                        workerTypes[workerId] ||
                                        "Không xác định",
                                };
                            }
                        }
                    }
                }
            }
        }

        return workers;
    } catch (error) {
        console.log(`Lỗi khi đọc thông tin nhân viên: ${error.message}`);
        return {};
    }
}

/**
 * Đếm số ca làm việc của một nhân viên cụ thể từ lịch làm việc thực tế.
 *
 * @param {string} workerId - ID của nhân viên cần đếm ca làm việc
 * @param {string|null} schedulePath - Đường dẫn đến file schedule.json
 * @returns {number} Số ca làm việc
 */
function countWorkerShifts(workerId, scheduleData = null) {
    try {
        // Đọc lịch làm việc thực tế từ schedule.json
        if (scheduleData) {
            const operationsData = scheduleData;

            // Đếm số ca làm việc của nhân viên từ schedule.json
            let shiftCount = 0;
            for (const operation of operationsData) {
                if (
                    operation.detailed_schedule &&
                    Array.isArray(operation.detailed_schedule)
                ) {
                    for (const shiftEntry of operation.detailed_schedule) {
                        if (
                            shiftEntry.worker_id &&
                            shiftEntry.worker_id === workerId
                        ) {
                            shiftCount += 1;
                        }
                    }
                }
            }

            return shiftCount;
        } else {
            console.log(
                `Không tìm thấy file lịch làm việc tại ${schedulePath}`
            );
            return 0;
        }
    } catch (error) {
        console.log(`Lỗi: ${error.message}`);
        return 0;
    }
}

/**
 * Tính số ca làm việc của mỗi loại nhân viên theo requiredPosition và từng nhân viên cụ thể.
 * Tổng số ca làm việc của mỗi loại nhân viên được tính bằng time range union để tránh double-counting.
 *
 * @param {string|null} schedulePath - Đường dẫn đến file schedule.json
 * @param {string|null} workersPath - Đường dẫn đến file input có thông tin nhân viên (input6.json)
 * @param {boolean} includeUnassigned - Có hiển thị nhân viên chưa được gán việc hay không
 * @returns {Object} Object với key là loại nhân viên và value là object thống kê
 */
function countWorkerTypeShifts(
    scheduleData = null,
    workersData = null,
    includeUnassigned = true
) {
    try {
        // Đọc dữ liệu từ file schedule.json
        const operationsData = scheduleData;

        // Đọc dữ liệu từ file input9.json để lấy thông tin operations
        const inputData = workersData;

        // Tạo mapping từ operation id sang requiredPosition
        const operationToWorkerType = {};
        if (inputData.operations) {
            for (const op of inputData.operations) {
                operationToWorkerType[op.id] =
                    op.requiredPosition || "Không xác định";
            }
        }

        // Lấy thông tin loại nhân viên từ workers
        const workerTypes = getWorkerTypes(scheduleData, workersData);
        const allWorkers = includeUnassigned
            ? getAllWorkers(workersData, scheduleData)
            : {};

        // Tổng hợp dữ liệu theo requiredPosition
        const workerTypeStats = {};
        const workerTypeTimeRanges = {}; // Lưu time ranges cho mỗi worker type

        // Đếm số ca làm việc cho mỗi nhân viên và tổng hợp theo requiredPosition
        const workerShifts = {};

        for (const operation of operationsData) {
            const requiredPosition =
                operationToWorkerType[operation.id] || "Không xác định";

            if (
                operation.detailed_schedule &&
                Array.isArray(operation.detailed_schedule)
            ) {
                // Khởi tạo worker type stats nếu chưa có
                if (!workerTypeStats[requiredPosition]) {
                    workerTypeStats[requiredPosition] = {
                        total_workers: 0,
                        total_shifts: 0,
                        total_time_operations: 0,
                        max_shift_worker: "",
                        max_shifts: 0,
                        workers: {},
                    };
                    workerTypeTimeRanges[requiredPosition] = [];
                }

                // Thu thập time ranges cho worker type này
                for (const shiftEntry of operation.detailed_schedule) {
                    if (
                        shiftEntry.worker_id &&
                        shiftEntry.day &&
                        shiftEntry.shift
                    ) {
                        // Đếm shifts cho từng nhân viên cụ thể
                        workerShifts[shiftEntry.worker_id] =
                            (workerShifts[shiftEntry.worker_id] || 0) + 1;

                        // Thu thập time range cho worker type
                        workerTypeTimeRanges[requiredPosition].push({
                            day: shiftEntry.day,
                            shift: shiftEntry.shift,
                        });
                    }
                }
            }
        }

        // Tính total_time_operations cho mỗi worker type bằng time range union
        for (const [workerType, timeRanges] of Object.entries(
            workerTypeTimeRanges
        )) {
            workerTypeStats[workerType].total_time_operations =
                calculateTimeRangeUnion(timeRanges);
        }

        // Thêm tất cả nhân viên vào thống kê, nhóm theo worker type của chúng
        if (includeUnassigned) {
            for (const [workerId, workerInfo] of Object.entries(allWorkers)) {
                const actualWorkerType =
                    workerInfo.position ||
                    workerInfo.workerType ||
                    "Không xác định";

                // Tìm requiredPosition tương ứng với actualWorkerType này
                // Nếu không có operation nào yêu cầu loại nhân viên này, vẫn tạo entry
                if (!workerTypeStats[actualWorkerType]) {
                    workerTypeStats[actualWorkerType] = {
                        total_workers: 0,
                        total_shifts: 0,
                        total_time_operations: 0,
                        max_shift_worker: "",
                        max_shifts: 0,
                        workers: {},
                    };
                }

                if (!(workerId in workerShifts)) {
                    workerShifts[workerId] = 0; // Ghi nhận là có 0 ca làm việc
                }
            }
        }

        // Cập nhật thống kê cho từng nhân viên theo worker type thực tế của chúng
        for (const [workerId, shiftCount] of Object.entries(workerShifts)) {
            const actualWorkerType =
                allWorkers[workerId]?.position ||
                allWorkers[workerId]?.workerType ||
                workerTypes[workerId] ||
                "Không xác định";

            // Đảm bảo worker type này có trong stats
            if (!workerTypeStats[actualWorkerType]) {
                workerTypeStats[actualWorkerType] = {
                    total_workers: 0,
                    total_shifts: 0,
                    total_time_operations: 0,
                    max_shift_worker: "",
                    max_shifts: 0,
                    workers: {},
                };
            }

            // Cập nhật thông tin cho loại nhân viên này
            workerTypeStats[actualWorkerType].workers[workerId] = shiftCount;

            // Cập nhật số ca tối đa cho loại nhân viên
            if (shiftCount > workerTypeStats[actualWorkerType].max_shifts) {
                workerTypeStats[actualWorkerType].max_shifts = shiftCount;
                workerTypeStats[actualWorkerType].max_shift_worker = workerId;
            }

            // Cập nhật tổng số ca (sum của tất cả nhân viên)
            workerTypeStats[actualWorkerType].total_shifts += shiftCount;
        }

        // Tính tổng số nhân viên cho mỗi loại
        for (const workerType of Object.keys(workerTypeStats)) {
            workerTypeStats[workerType].total_workers = Object.keys(
                workerTypeStats[workerType].workers
            ).length;
        }

        return workerTypeStats;
    } catch (error) {
        console.log(`Lỗi: ${error.message}`);
        return {};
    }
}

/**
 * In ra thống kê về số ca làm việc của mỗi loại nhân viên và từng nhân viên cụ thể.
 *
 * @param {string|null} schedulePath - Đường dẫn đến file schedule.json
 * @param {string|null} workersPath - Đường dẫn đến file input có thông tin nhân viên (input6.json)
 * @param {boolean} includeUnassigned - Có hiển thị nhân viên chưa được gán việc hay không
 * @param {boolean} showZeroShifts - Có hiển thị các nhân viên có 0 ca làm việc hay không
 */
function printWorkerTypeStatistics(
    scheduleData = null,
    workersData = null,
    includeUnassigned = true,
    showZeroShifts = true
) {
    const stats = countWorkerTypeShifts(
        scheduleData,
        workersData,
        includeUnassigned
    );

    if (Object.keys(stats).length === 0) {
        console.log("Không có dữ liệu thống kê về nhân viên.");
        return;
    }
    console.log("\n===== THỐNG KÊ CA LÀM VIỆC THEO LOẠI NHÂN VIÊN =====\n");

    // Sắp xếp theo tổng số ca làm việc giảm dần
    const sortedStats = Object.entries(stats).sort(
        (a, b) => b[1].total_shifts - a[1].total_shifts
    ); // Chuyển đổi sang định dạng mong muốn với total_time_operations
    const formattedOutput = sortedStats.map(([workerTypeName, data]) => {
        // Tính số nhân viên idle (không có ca làm việc)
        const idleWorkers = Object.values(data.workers).filter(
            (shifts) => shifts === 0
        ).length;

        return {
            workerTypeName: workerTypeName,
            total_time_operations: data.total_time_operations || 0,
            total_workers: data.total_workers,
            total_shifts: data.total_shifts,
            max_shift_worker: data.max_shift_worker,
            workers: data.workers,
            idleWorkers: idleWorkers,
        };
    });

    return formattedOutput;
}

// Chạy trực tiếp để test
if (require.main === module) {
    // Ví dụ về thống kê theo loại máy
    const assets = printMachineTypeStatistics(
        scheduleData,
        assetsData,
        true,
        true
    );

    // Lưu vào file JSON với định dạng mới
    fs.writeFileSync(outputData1, JSON.stringify(assets, null, 2), "utf-8");

    console.log("=== THỐNG KÊ THEO LOẠI MÁY ===");
    console.log(assets);

    // Ví dụ về thống kê theo loại nhân viên
    const workers = printWorkerTypeStatistics(
        scheduleData,
        workersData,
        true,
        true
    );

    // Lưu vào file JSON với định dạng mới
    fs.writeFileSync(outputData2, JSON.stringify(workers, null, 2), "utf-8");

    console.log("=== THỐNG KÊ THEO LOẠI NHÂN VIÊN ===");
    console.log(workers);
}
