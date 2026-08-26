import { Routes, Route } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";
import HomePage from "./pages/HomePage.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import RegisterPage from "./pages/RegisterPage.jsx";
import UploadPage from "./pages/UploadPage.jsx";
import DashboardPage from "./pages/DashboardPage.jsx";
import NotFoundPage from "./pages/NotFoundPage.jsx";

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/upload" element={<ProtectedRoute><UploadPage /></ProtectedRoute>} />
        <Route path="/dashboard/:id" element={<DashboardPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </AuthProvider>
  );
}

export default App;
