const fs = require("fs");
const path = require("path");

// Define path to JSON file
const filePath = path.resolve(__dirname, "../data/test.json");

// Function to limit machine types to 7 machines each
function limitMachineTypes(filePath, maxMachinesPerType = 5) {
    try {
        // Read and parse the JSON file
        const data = JSON.parse(fs.readFileSync(filePath, "utf8"));

        // Group assets by machine type
        const groupedByType = {};
        data.assets.forEach((asset) => {
            if (!groupedByType[asset.machineType]) {
                groupedByType[asset.machineType] = [];
            }
            groupedByType[asset.machineType].push(asset);
        });

        // Create a new array with limited machines per type
        const limitedAssets = [];
        let removedCount = 0;

        for (const machineType in groupedByType) {
            const machines = groupedByType[machineType];
            if (machines.length > maxMachinesPerType) {
                console.log(
                    `Machine type "${machineType}" has ${machines.length} machines, reducing to ${maxMachinesPerType}`
                );
                removedCount += machines.length - maxMachinesPerType;
                limitedAssets.push(...machines.slice(0, maxMachinesPerType));
            } else {
                limitedAssets.push(...machines);
            }
        }

        // Sort assets by ID to maintain original ordering
        limitedAssets.sort((a, b) => a.id.localeCompare(b.id));

        // Update the data with limited assets
        data.assets = limitedAssets;

        // Write the updated data back to the file
        fs.writeFileSync(filePath, JSON.stringify(data, null, 4), "utf8");

        console.log(
            `Process complete. Removed ${removedCount} machines to limit each type to ${maxMachinesPerType}.`
        );
    } catch (error) {
        console.error("Error processing the file:", error);
    }
}

// Execute the function
limitMachineTypes(filePath);
