import React from "react";
import { Routes, Route } from "react-router-dom";
import Main from "./components/Main";
import VerifyEmail from "./components/VerifyEmail";
import ContinueRegistration from "./components/ContinueRegistration";
import PersonalDetailsForm from "./components/PersonalDetailsForm";
import NotFoundPage from "./components/NotFoundPage";
import Footer from "./components/Footer";
import UserProfile from "./components/UserProfile";
import ChangePassword from "./components/ChangePassword";
import ChooseRole from "./components/ChooseRole";
import ConfirmEmail from "./components/ConfirmEmail";



function App(){
  //   const isAuthentikated = !!token;

  return(
      <>
        <main>
          <Routes>
            <Route path ="/" element={<Main />} />
            <Route path ="/verify_email" element={<VerifyEmail />} />
            <Route path ="/confirm_email" element={<ConfirmEmail />} />
            <Route path ="/continue_registration" element={<ContinueRegistration />} />
            <Route path ="/user_basic-info" element={<PersonalDetailsForm />} />
            <Route path ="/user_choose-role" element={<ChooseRole />} />
            <Route path ="/user_profile" element={<UserProfile />} />
            <Route path ="/change_password" element={<ChangePassword />} />
            <Route path ="*" element={<NotFoundPage />} />
          </Routes>
        </main>
        <Footer />
      </>
  )
}

export default App;
