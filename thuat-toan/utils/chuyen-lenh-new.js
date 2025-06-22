const fs = require("fs");
const path = require("path");

// Dữ liệu mẫu
const schedule = require("../out/out3/input9_2/schedule.json");

const outputData = "thuat-toan/out/out3/input9_2/machine_command_switches.json";

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

// Convert json structure
function saveResultToJson(scheduleData) {
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

    return jsonResult;
}

const savedResult = saveResultToJson(schedule);

// Lưu vào file JSON với định dạng mới
fs.writeFileSync(outputData, JSON.stringify(savedResult, null, 2), "utf-8");

console.log(savedResult);
