import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Main from '~@/Layout/jsx/Main'
import Footer from '~@/Layout/jsx/Footer'
import NotFoundPage from '~@/Layout/jsx/NotFoundPage'
import VerifyEmail from '~@/Authorization/jsx/VerifyEmail'
import ChangePassword from '~@/Authorization/jsx/ChangePassword'
import ContinueRegistration from '~@/Authorization/jsx/ContinueRegistration'
import ConfirmEmail from '~@/Authorization/jsx/ConfirmEmail'
import UserBasicInfo from '~@/UserArea/jsx/UserBasicInfo'
import ChooseRole from '~@/RegistrationRole/jsx/RegistrationRole'
import Lecturer from '~@/WorkRooms/Lecturer/jsx/Lecturer'
import RegistrationRole from '~@/RegistrationRole/jsx/RegistrationRole'
import LecturerStep2 from '~@/RegistrationRole/jsx/LecturerSteps/LecturerStep2'
import LecturerStep3 from '~@/RegistrationRole/jsx/LecturerSteps/LecturerStep3'
import LecturerStep4 from '~@/RegistrationRole/jsx/LecturerSteps/LecturerStep4'



function App() {
  //   const isAuthentikated = !!token;

  return (
    <>
      <main>
        <Routes>
          <Route path='/' element={<Main />} />
          <Route path='/verify_email' element={<VerifyEmail />} />
          <Route path='/confirm_email' element={<ConfirmEmail />} />
          <Route
            path='/continue_registration'
            element={<ContinueRegistration />}
          />
          <Route path='/user_basic-info' element={<UserBasicInfo />} />
          <Route path='/register_choose-role' element={<RegistrationRole />} />
          <Route path='/register_lecturer2' element={<LecturerStep2 />} />
          <Route path='/register_lecturer3' element={<LecturerStep3 />} />
          <Route path='/register_lecturer4' element={<LecturerStep4 />} />
          <Route path='/user_profile' element={<Lecturer />} />
          <Route path='/change_password' element={<ChangePassword />} />
          <Route path='*' element={<NotFoundPage />} />
        </Routes>
      </main>
      <Footer />
    </>
  )
}

export default App
