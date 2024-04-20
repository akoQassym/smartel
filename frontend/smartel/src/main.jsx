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
import PhysicianDashboard from "./routes/PhysicianDashboard.jsx";

// For Clerk Authentication
import { ClerkProvider, SignUp, SignIn } from "@clerk/clerk-react";
import ProtectedRoute from "./components/ProtectedRoute.jsx";
import SignInPage from "./routes/SignInPage.jsx";
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
          {/*Physician portal routes below */}
          <Route path="/physicianDashboard" element={<PhysicianDashboard />} />
        </Route>
      </Routes>
    </ClerkProvider>
  );
};

// ReactDOM.createRoot(document.getElementById("root")).render(
//   <React.StrictMode>
//     <Router>
//       <Routes>
//         <Route path="/" element={<Home />} />
//         <Route path="/dashboard" element={<Dashboard />} />
//         <Route path="/medicaldocs" element={<MedicalDocumentsPage />} />
//         <Route path="/appointmentspage" element={<AppointmentsPage />} />
//         <Route
//           path="/consultationreports"
//           element={<ConsultationReportsPage />}
//         />
//       </Routes>
//     </Router>
//   </React.StrictMode>
// );

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Router>
      <ClerkWithRoutes />
    </Router>
  </React.StrictMode>
);
