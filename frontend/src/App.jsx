import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Main from '~@/Layout/jsx/Main'
import Footer from '~@/Layout/jsx/Footer'
import NotFoundPage from '~@/Layout/jsx/NotFoundPage'
import VerifyEmail from '~@/Authorization/jsx/VerifyEmail'
import ChangePassword from '~@/Authorization/jsx/ChangePassword'
import ContinueRegistration from '~@/Authorization/jsx/ContinueRegistration'
import ConfirmEmail from '~@/Authorization/jsx/ConfirmEmail'
import SetProfileInfo from '~@/Profile/jsx/SetProfileInfo'
import RegistrationRole from '~@/RegistrationRole/jsx/RegistrationRole'
import Workroom from "~@/WorkRooms/Workroom"
import Header from "~@/Layout/jsx/Header"
import CreateEvent from "~@/CreateEvent/jsx/CreateEvent"
import Permissions from "./components/Authorization/jsx/Permissions";
import {permissions} from "./ProjectConstants";


function App() {
  return (
    <>
        <Header/>
          <main>
            <Routes>
              <Route path='/' element={<Main/>}/>
              <Route path='/verify_email' element={<VerifyEmail />} />
              <Route path='/confirm_email' element={<ConfirmEmail />} />
              <Route path='/continue_registration' element={<ContinueRegistration />} />
              <Route path='/create_profile' element={
                <Permissions check={permissions.isAuthenticated}>
                  <SetProfileInfo />
                </Permissions>
              }/>
              <Route path='/add_role' element={
                <Permissions check={permissions.isAuthenticated}>
                  <RegistrationRole/>
                </Permissions>
                  } />
              <Route path='/workroom' element={
                <Permissions check={permissions.isAuthenticated}>
                  <Workroom />
                </Permissions>
              }/>
              <Route path='/create_event' element={
                <Permissions check={permissions.isAuthenticated}>
                  <CreateEvent/>
                </Permissions>
                  }/>
              <Route path='/change_password' element={<ChangePassword />} />
              <Route path='*' element={<NotFoundPage />} />
            </Routes>
          </main>
        <Footer />
    </>
  )
}

export default App
