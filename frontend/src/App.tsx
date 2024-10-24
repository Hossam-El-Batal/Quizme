import React, { useEffect, useState } from "react";
import ForgotPassword from "./components/authentication/ForgotPassword.tsx";
import ChangePassword from "./components/authentication/ResetPassword.tsx";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import AllQuestionsPage from "./components/Viewers/ExamPage/AllQuestionsPage.tsx";
import ExamCreationForm from "./components/Forms/ExamCreationForm";
import QuestionBank from "./components/Viewers/QuestionBank";
import Login from "./components/authentication/Login.tsx";
import Profile from "./components/authentication/Profile.tsx";
import RegisterForm from "./components/authentication/Register.tsx";
import WebcamMonitorWrapper from "./components/Wrappers/WebcamMonitorWrapper.tsx";
import Dashboard from "./components/dashboard/Dashboard.tsx";
import HomeLayout from "./layouts/HomeLayout.tsx";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Landing from "./components/Landing/LandingPage.tsx";
import AttemptView from "./components/Viewers/AttemptView.tsx";
import ExamAllStudent from "./components/ExamResults/ExamAllStudent.tsx";
import AllExams from "./components/ExamResults/AllExams.tsx";
import { UserProvider } from "../context/UserContext.tsx";
import ModelAnswersPage from "./components/Viewers/ModelAnswerPage.tsx";
import ExamEntry from "./components/Viewers/EnterExam.tsx";
import ForbiddenPage from "./components/Viewers/PermissionDenied.tsx";
import NotFoundPage from "./components/Viewers/NotFound.tsx";
import ProtectedRoute from "./components/authentication/ProtectedRoute.tsx";
import StudentExamEntry from "./components/Viewers/ExamEntryNavigator.tsx";
import ActivityMonitorWrapper from "./components/Wrappers/ActivityMonitorWrapper.tsx";
import ExamResult from "./components/Viewers/Results.tsx";
import TermsAndConditions from "./components/Viewers/Terms.tsx";
import StudentAnswer from "./components/ExamResults/StudentAnswers.tsx";
// import StudentAnswer from "./components/ExamResults/StudentAnswers.tsx";
import EmailVerification from "./components/authentication/EmailVerification.tsx";
import ActivityTimeline from "./components/ExamLogs/ExamLogs.tsx";
import LoginModal from "./components/authentication/LoginModal.tsx";
import PayPalSubscriptionPage from "./components/Viewers/PayPal/Paypal.tsx";

const App: React.FC = () => {
  const [isLoginModalVisible, setIsLoginModalVisible] = useState(false);

  useEffect(() => {
    // Event listener for showing login modal when 401 error occurs
    const handleShowLoginModal = () => {
      console.log("Event received: Showing login modal"); // Add log to verify

      setIsLoginModalVisible(true);
    };

    window.addEventListener("showLoginModal", handleShowLoginModal);

    // Cleanup the event listener on component unmount
    return () => {
      window.removeEventListener("showLoginModal", handleShowLoginModal);
    };
  }, []);
  return (
    <UserProvider>
      <Router>
        <HomeLayout>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<RegisterForm />} />
            <Route path="/exam-finished/:examCode" element={<ExamResult />} />
            <Route path="/" element={<Landing />} />
            <Route path="/permission-denied" element={<ForbiddenPage />} />
            <Route path="/Forgot-password" element={<ForgotPassword />} />
            <Route path="/exam-logs" element={<ActivityTimeline />} />
            <Route
              path="/reset-password/:uidb64/:token"
              element={<ChangePassword />}
            />
            <Route path="/api/v1/auth/verify-email/:uid/:token" element={<EmailVerification />} />
            <Route
              path="/subscribe/:planId"
              element={<ProtectedRoute element={<PayPalSubscriptionPage />} />}
            />

            <Route
              path="/create-exam"
              element={<ProtectedRoute element={<ExamCreationForm />} />}
            />
            <Route
              path="/profile"
              element={<ProtectedRoute element={<Profile />} />}
            />
            <Route
              path="/dashboard"
              element={<ProtectedRoute element={<Dashboard />} />}
            />
            <Route path="/enter-exam/:examCode" element={<ExamEntry />} />
            <Route
              path="/attempt/:examCode/:attemptId"
              element={<ProtectedRoute element={<StudentAnswer />} />}
            />
            <Route path="/enter" element={<StudentExamEntry />} />
            <Route
              path="/exam/:examCode"
              element={
                <WebcamMonitorWrapper>
                  <ActivityMonitorWrapper>
                    <AllQuestionsPage />
                  </ActivityMonitorWrapper>
                </WebcamMonitorWrapper>
              }
            />
            <Route
              path="/question-bank"
              element={<ProtectedRoute element={<QuestionBank />} />}
            />
            <Route
              path="/exam-result/:examCode"
              element={<ProtectedRoute element={<ExamAllStudent />} />}
            />
            <Route path="/terms" element={<TermsAndConditions />} />
            <Route
              path="/answer/:examCode"
              element={<ProtectedRoute element={<ModelAnswersPage />} />}
            />
            <Route
              path="/exams"
              element={<ProtectedRoute element={<AllExams />} />}
            />
            <Route
              path="/attempt/:attempt_id"
              element={<ProtectedRoute element={<AttemptView />} />}
            />
            <Route path="/not-found" element={<NotFoundPage />} />
            {/* Catch-all route for 404 */}
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
          <ToastContainer position="bottom-right" />
        </HomeLayout>
        <LoginModal
          isModalVisible={isLoginModalVisible}
          setIsModalVisible={setIsLoginModalVisible}
        />
      </Router>
    </UserProvider>
  );
};

export default App;
