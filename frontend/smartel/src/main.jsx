import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./routes/Home.jsx";
import Dashboard from "./routes/Dashboard.jsx";
import MedicalDocumentsPage from "./routes/MedicalDocumentsPage.jsx";
import AppointmentsPage from "./routes/AppointmentsPage.jsx";
import ConsultationReportsPage from "./routes/ConsultationReportsPage.jsx";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/medicaldocs" element={<MedicalDocumentsPage />} />
        <Route path="/appointmentspage" element={<AppointmentsPage />} />
        <Route
          path="/consultationreports"
          element={<ConsultationReportsPage />}
        />
      </Routes>
    </Router>
  </React.StrictMode>
);
