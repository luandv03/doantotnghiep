import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { Routes, Route, BrowserRouter } from "react-router-dom";
import App from "./App.jsx";
// import App2 from "./App2.jsx";
import Schedule from "./Schedule.jsx";
// import Schedule2 from "./Schedule2.jsx";
import KPI from "./KPI.jsx";
import MachineAnalysis from "./MachineAnalysis.jsx";
import WorkerAnalysis from "./WorkerAnalysis.jsx";

createRoot(document.getElementById("root")).render(
    <StrictMode>
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<App />} />
                {/* <Route path="/worst" element={<App2 />} /> */}
                <Route path="/schedule" element={<Schedule />} />
                {/* <Route path="/schedule_worst" element={<Schedule2 />} /> */}
                <Route path="/kpi" element={<KPI />} />
                <Route path="/machine_analysis" element={<MachineAnalysis />} />
                <Route path="/worker_analysis" element={<WorkerAnalysis />} />
                <Route path="*" element={<h1>Page Not Found</h1>} />
            </Routes>
        </BrowserRouter>
    </StrictMode>
);
