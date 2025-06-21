/**
 * This script extracts all unique employee positions and machine types
 * from the operations section of the input3.json file
 * It also filters workers and machines based on required positions and types
 */

const fs = require("fs");
const path = require("path");

// Path to the input file
const inputFilePath = path.join(
    __dirname,
    "..",
    "..",
    "thuat-toan",
    "data-2",
    "input9.json"
);

// Function to extract unique positions and machine types
function extractPositionsAndMachines(jsonData) {
    // Initialize sets to store unique values
    const positions = new Set();
    const machineTypes = new Set();

    // Check if operations array exists
    if (jsonData && jsonData.operations && Array.isArray(jsonData.operations)) {
        // Loop through each operation
        jsonData.operations.forEach((operation) => {
            // Add the required position if it exists
            if (operation.requiredPosition) {
                positions.add(operation.requiredPosition);
            }

            // Add the required machine type if it exists
            if (operation.requiredMachineType) {
                machineTypes.add(operation.requiredMachineType);
            }
        });
    } else {
        console.error("No operations array found in the data");
    }

    // Generate random salaries for workers based on KPIs
    if (jsonData && jsonData.workers && Array.isArray(jsonData.workers)) {
        jsonData.workers.forEach((worker) => {
            // Base salary between 15 and 20
            const baseSalary = 15 + Math.random() * 5;

            // Productivity bonus: Higher productivity leads to higher salary
            const productivityFactor = (worker.productivityKPI || 30) / 50; // Normalize to a 0-1+ scale

            // Quality bonus: Higher quality leads to higher salary
            const qualityFactor = (worker.qualityKPI || 0.5) * 1.5; // Multiply by 1.5 to give more weight

            // Calculate total salary with some randomness
            let totalSalary =
                baseSalary *
                (0.7 + 0.3 * productivityFactor + 0.4 * qualityFactor);

            // Add a small random variation (±10%)
            const variation = 0.9 + Math.random() * 0.2;

            // Set the final salary (rounded to 2 decimal places)
            worker.salaryPerHour = Math.floor(
                Math.round(totalSalary * variation * 100) / 100
            );
        });
    }

    // Convert sets to sorted arrays
    return {
        positions: Array.from(positions).sort(),
        machineTypes: Array.from(machineTypes).sort(),
    };
}

/**
 * Filter workers based on required positions
 * @param {Object} jsonData - The input JSON data
 * @param {Array} requiredPositions - The list of required positions
 * @returns {Array} - Filtered list of workers
 */
function filterWorkersByPosition(jsonData, requiredPositions) {
    if (!jsonData || !jsonData.workers || !Array.isArray(jsonData.workers)) {
        console.error("No workers array found in the data");
        return [];
    }

    const filteredWorkers = jsonData.workers.filter((worker) => {
        // If worker has a position and it's in the required positions list, keep it
        return worker.position && requiredPositions.includes(worker.position);
    });

    console.log(
        `Filtered workers: ${filteredWorkers.length} out of ${jsonData.workers.length}`
    );
    return filteredWorkers;
}

/**
 * Filter machines based on required types
 * @param {Object} jsonData - The input JSON data
 * @param {Array} requiredMachineTypes - The list of required machine types
 * @returns {Array} - Filtered list of machines
 */
function filterMachinesByType(jsonData, requiredMachineTypes) {
    if (!jsonData || !jsonData.assets || !Array.isArray(jsonData.assets)) {
        console.error("No machines array found in the data");
        return [];
    }

    console.log(
        `Filtering machines based on types: ${requiredMachineTypes.join(", ")}`
    );

    const filteredMachines = jsonData.assets.filter((machine) => {
        // If machine has a type and it's in the required types list, keep it
        return (
            machine.machineType &&
            requiredMachineTypes.includes(machine.machineType)
        );
    });

    console.log(
        `Filtered machines: ${filteredMachines.length} out of ${jsonData.assets.length}`
    );
    return filteredMachines;
}

// Main function
function main() {
    try {
        // Read the JSON file
        const rawData = fs.readFileSync(inputFilePath, "utf8");
        const jsonData = JSON.parse(rawData);

        // Extract unique positions and machine types
        const { positions, machineTypes } =
            extractPositionsAndMachines(jsonData);

        // Output the results to console
        console.log("Unique Employee Positions:", positions);
        console.log(`Total: ${positions.length} positions`);
        console.log("\nUnique Machine Types:", machineTypes);
        console.log(`Total: ${machineTypes.length} machine types`);

        // Write results to output files
        const positionsOutput = path.join(__dirname, "employee_positions.json");
        const machinesOutput = path.join(__dirname, "machine_types.json");

        fs.writeFileSync(positionsOutput, JSON.stringify(positions, null, 2));
        fs.writeFileSync(machinesOutput, JSON.stringify(machineTypes, null, 2));

        console.log(
            `\nResults saved to ${positionsOutput} and ${machinesOutput}`
        );

        // Filter workers and machines based on required positions and types
        const filteredWorkers = filterWorkersByPosition(jsonData, positions);
        const filteredMachines = filterMachinesByType(jsonData, machineTypes);

        // Write filtered data to output files
        const filteredWorkersOutput = path.join(
            __dirname,
            "filtered_workers.json"
        );
        const filteredMachinesOutput = path.join(
            __dirname,
            "filtered_machines.json"
        );

        fs.writeFileSync(
            filteredWorkersOutput,
            JSON.stringify(filteredWorkers, null, 2)
        );
        fs.writeFileSync(
            filteredMachinesOutput,
            JSON.stringify(filteredMachines, null, 2)
        );

        console.log(
            `\nFiltered data saved to ${filteredWorkersOutput} and ${filteredMachinesOutput}`
        );

        // Create a new filtered data object
        const filteredData = {
            ...jsonData,
            workers: filteredWorkers,
            machines: filteredMachines,
        };

        // Write the complete filtered data to an output file
        const filteredDataOutput = path.join(__dirname, "filtered_input.json");
        fs.writeFileSync(
            filteredDataOutput,
            JSON.stringify(filteredData, null, 2)
        );
        console.log(`\nComplete filtered data saved to ${filteredDataOutput}`);
    } catch (error) {
        console.error("Error processing file:", error);
    }
}

// Execute the main function
main();
