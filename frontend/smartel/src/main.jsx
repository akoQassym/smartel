import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  useNavigate,
} from "react-router-dom";
import Home from "./routes/Home.jsx";
import Dashboard from "./routes/Dashboard.jsx";
import MedicalDocumentsPage from "./routes/MedicalDocumentsPage.jsx";
import AppointmentsPage from "./routes/AppointmentsPage.jsx";
import ConsultationReportsPage from "./routes/ConsultationReportsPage.jsx";
import CompletePatientProfile from "./routes/CompletePatientProfile.jsx";
import Profile from "./routes/Profile.jsx";
import PhysicianDashboard from "./routes/PhysicianDashboard.jsx";
import PhysicianConsultationGen from "./routes/PhysicianConsultationGen.jsx";
import PhysicianAppointments from "./routes/PhysicianAppointments.jsx";
import PhysicianProfile from "./routes/PhysicianProfile.jsx";
import CompletePhysicianProfile from "./routes/CompletePhysicianProfile.jsx";

// For Clerk Authentication
import { ClerkProvider, SignUp, SignIn } from "@clerk/clerk-react";
import ProtectedRoute from "./components/ProtectedRoute.jsx";
import SignInPage from "./routes/SignInPage.jsx";
import { userRoleLoader } from "./routes/Loaders.jsx";
const VITE_CLERK_PUBLISHABLE_KEY =
  "pk_test_ZW5qb3llZC1tYWxsYXJkLTM4LmNsZXJrLmFjY291bnRzLmRldiQ";

const ClerkWithRoutes = () => {
  const navigate = useNavigate();

  return (
    <ClerkProvider
      publishableKey={VITE_CLERK_PUBLISHABLE_KEY}
      navigate={(to) => navigate(to)}
    >
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/sign-in/*" element={<SignInPage />} />
        <Route
          path="/sign-up/*"
          element={<SignUp redirectUrl={"/"} routing="path" path="/sign-up" />}
        />
        <Route element={<ProtectedRoute />}>
          {/* Place all protected routes as children here */}
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/medicaldocs" element={<MedicalDocumentsPage />} />
          <Route path="/appointmentspage" element={<AppointmentsPage />} />
          <Route
            path="/consultationreports"
            element={<ConsultationReportsPage />}
          />
          <Route path="/patientProfile" element={<Profile />} />
          <Route
            path="/patientProfileCompletion"
            element={<CompletePatientProfile />}
          />
          {/*Physician portal routes below */}
          <Route path="/physicianDashboard" element={<PhysicianDashboard />} />
          <Route
            path="/physicianConsultationReports"
            element={<PhysicianConsultationGen />}
          />
          <Route
            path="/physicianAppointments"
            element={<PhysicianAppointments />}
          />
          <Route path="/physicianProfile" element={<PhysicianProfile />} />
          <Route
            path="/physicianProfileCompletion"
            element={<CompletePhysicianProfile />}
          />
        </Route>
      </Routes>
    </ClerkProvider>
  );
};

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Router>
      <ClerkWithRoutes />
    </Router>
  </React.StrictMode>
);
