// Dữ liệu mẫu
const schedule = require("../out/schedule.json");

function calculateMachineCommandSwitches(schedule) {
    // Tạo một mảng chứa tất cả các hoạt động của máy móc theo thời gian
    const machineActivities = [];

    // Duyệt qua tất cả các operations
    schedule.forEach((operation) => {
        operation.detailed_schedule.forEach((detail) => {
            machineActivities.push({
                asset_id: detail.asset_id,
                commandId: operation.commandId,
                day: detail.day,
                shift: detail.shift,
                timestamp: new Date(detail.day).getTime() + detail.shift * 1000, // Tạo timestamp để sắp xếp
            });
        });
    });

    // Sắp xếp theo máy móc và thời gian
    machineActivities.sort((a, b) => {
        if (a.asset_id !== b.asset_id) {
            return a.asset_id.localeCompare(b.asset_id);
        }
        if (a.day !== b.day) {
            return new Date(a.day) - new Date(b.day);
        }
        return a.shift - b.shift;
    });

    // Tính toán số lần chuyển lệnh cho mỗi máy
    const machineStats = {};

    machineActivities.forEach((activity) => {
        const assetId = activity.asset_id;

        if (!machineStats[assetId]) {
            machineStats[assetId] = {
                commands: new Set(),
                switches: 0,
                lastCommand: null,
                activities: [],
            };
        }

        // Thêm command vào set để đếm số lệnh tham gia
        machineStats[assetId].commands.add(activity.commandId);
        machineStats[assetId].activities.push(activity);

        // Kiểm tra chuyển lệnh
        if (
            machineStats[assetId].lastCommand &&
            machineStats[assetId].lastCommand !== activity.commandId
        ) {
            machineStats[assetId].switches++;
        }

        machineStats[assetId].lastCommand = activity.commandId;
    });

    return machineStats;
}

// Test với dữ liệu mẫu
const result = calculateMachineCommandSwitches(schedule);

console.log("=== KẾT QUẢ THỐNG KÊ MÁY MÓC ===\n");

Object.keys(result).forEach((assetId) => {
    const stats = result[assetId];
    console.log(`Máy ${assetId}:`);
    console.log(`  - Số lệnh tham gia: ${stats.commands.size}`);
    console.log(`  - Các lệnh: [${Array.from(stats.commands).join(", ")}]`);
    console.log(`  - Số lần chuyển lệnh: ${stats.switches}`);

    console.log(`  - Chi tiết hoạt động:`);
    stats.activities.forEach((activity, index) => {
        console.log(
            `    ${index + 1}. ${activity.day} ca ${activity.shift}: ${
                activity.commandId
            }`
        );
    });
    console.log("");
});

// Hàm để test với dữ liệu khác (ví dụ có chuyển lệnh)
function testWithCommandSwitching() {
    const testData = [
        {
            commandId: "LSX0001",
            id: "OP001",
            detailed_schedule: [
                { day: "2025-04-01", shift: 1, asset_id: "A001" },
                { day: "2025-04-01", shift: 2, asset_id: "A001" },
            ],
        },
        {
            commandId: "LSX0002",
            id: "OP002",
            detailed_schedule: [
                { day: "2025-04-01", shift: 3, asset_id: "A001" },
            ],
        },
        {
            commandId: "LSX0001",
            id: "OP003",
            detailed_schedule: [
                { day: "2025-04-01", shift: 4, asset_id: "A001" },
            ],
        },
    ];

    console.log("=== TEST VÍ DỤ CÓ CHUYỂN LỆNH ===\n");
    const testResult = calculateMachineCommandSwitches(testData);

    Object.keys(testResult).forEach((assetId) => {
        const stats = testResult[assetId];
        console.log(`Máy ${assetId}:`);
        console.log(`  - Số lệnh tham gia: ${stats.commands.size}`);
        console.log(`  - Các lệnh: [${Array.from(stats.commands).join(", ")}]`);
        console.log(`  - Số lần chuyển lệnh: ${stats.switches}`);
        console.log(
            `  - Lịch sử: LSX0001 -> LSX0002 -> LSX0001 (2 lần chuyển)`
        );
        console.log("");
    });
}

// Chạy test
testWithCommandSwitching();

// Hàm để lưu kết quả vào file JSON (cho Node.js)
function saveResultToJson(scheduleData, filename = "machine_statistics.json") {
    const fs = require("fs");
    const path = require("path");

    const stats = calculateMachineCommandSwitches(scheduleData);

    // Chuyển đổi Set thành Array và format lại dữ liệu cho JSON
    const jsonResult = {
        summary: {
            total_machines: Object.keys(stats).length,
            generated_at: new Date().toISOString(),
        },
        machines: {},
    };

    Object.keys(stats).forEach((assetId) => {
        const machineStats = stats[assetId];
        jsonResult.machines[assetId] = {
            asset_id: assetId,
            total_commands_participated: machineStats.commands.size,
            commands: Array.from(machineStats.commands),
            command_switches: machineStats.switches,
            activities: machineStats.activities.map((activity) => ({
                day: activity.day,
                shift: activity.shift,
                command_id: activity.commandId,
            })),
        };
    });

    // Tạo đường dẫn đầy đủ
    const fullPath = path.resolve(filename);

    try {
        // Ghi file JSON
        const jsonString = JSON.stringify(jsonResult, null, 2);
        fs.writeFileSync(fullPath, jsonString, "utf8");

        console.log(`✅ Đã lưu kết quả vào file: ${fullPath}`);
        console.log("📊 Cấu trúc file JSON:");
        console.log(JSON.stringify(jsonResult, null, 2));

        return jsonResult;
    } catch (error) {
        console.error(`❌ Lỗi khi lưu file: ${error.message}`);
        return null;
    }
}

// Hàm async để lưu file (sử dụng promises)
async function saveResultToJsonAsync(
    scheduleData,
    filename = "machine_statistics.json"
) {
    const fs = require("fs").promises;
    const path = require("path");

    const stats = calculateMachineCommandSwitches(scheduleData);

    // Chuyển đổi Set thành Array và format lại dữ liệu cho JSON
    const jsonResult = {
        summary: {
            total_machines: Object.keys(stats).length,
            generated_at: new Date().toISOString(),
        },
        machines: {},
    };

    Object.keys(stats).forEach((assetId) => {
        const machineStats = stats[assetId];
        jsonResult.machines[assetId] = {
            asset_id: assetId,
            total_commands_participated: machineStats.commands.size,
            commands: Array.from(machineStats.commands),
            command_switches: machineStats.switches,
            activities: machineStats.activities.map((activity) => ({
                day: activity.day,
                shift: activity.shift,
                command_id: activity.commandId,
            })),
        };
    });

    // Tạo đường dẫn đầy đủ
    const fullPath = path.resolve(filename);

    try {
        // Ghi file JSON async
        const jsonString = JSON.stringify(jsonResult, null, 2);
        await fs.writeFile(fullPath, jsonString, "utf8");

        console.log(`✅ Đã lưu kết quả vào file: ${fullPath}`);
        console.log("📊 Cấu trúc file JSON:");
        console.log(JSON.stringify(jsonResult, null, 2));

        return jsonResult;
    } catch (error) {
        console.error(`❌ Lỗi khi lưu file: ${error.message}`);
        return null;
    }
}

// Lưu kết quả từ dữ liệu gốc (sync)
console.log("\n=== LƯU KẾT QUẢ VÀO FILE JSON (SYNC) ===");
const savedResult = saveResultToJson(
    schedule,
    "./out/machine_command_switches.json"
);

// Ví dụ sử dụng async version
console.log("\n=== LƯU KẾT QUẢ VÀO FILE JSON (ASYNC) ===");
(async () => {
    try {
        await saveResultToJsonAsync(
            schedule,
            "./out/machine_command_switches_async.json"
        );

        console.log("🎉 Hoàn thành lưu file async!");
    } catch (error) {
        console.error("❌ Lỗi async:", error);
    }
})();
