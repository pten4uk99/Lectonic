import React, {useEffect, useState} from 'react'
import {connect} from "react-redux";
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
import CreateEvent from "~@/WorkRooms/CreateEvent/jsx/CreateEvent"
import Header from "~@/Layout/jsx/Header"
import RolePage from "~@/Pages/RolePage/jsx/RolePage";
import Permissions from "./components/Authorization/jsx/Permissions";
import {hostURL, permissions, reverse} from "./ProjectConstants";
import {createNotificationsSocket} from "./webSocket";



// let chatSocket = new WebSocket(`ws://${hostURL}/connect/`);


function App(props) {
  let userId = props.store.permissions.user_id
  let [notificationsSocket, setNotificationsSocket] = useState(null)
  let [chatsSocket, setChatSocket] = useState(null)
  
  useEffect(() => {
    if (userId) createNotificationsSocket(setChatSocket, userId)
  }, [userId])
  
  return (
    <>
        <Header notificationsSocket={notificationsSocket}/>
          <main>
            <Permissions>
              <Routes>
                <Route path={reverse('index')} element={<Main/>}/>
                <Route path={reverse('verify_email')} element={<VerifyEmail />} />
                <Route path={reverse('confirm_email')} element={<ConfirmEmail />} />
                <Route path={reverse('continue_signup')} element={<ContinueRegistration />} />
                <Route path={reverse('create_profile')} element={<SetProfileInfo />}/>
                <Route path='/add_role/*' element={<RegistrationRole/>}/>
                <Route path={reverse('workroom')} element={<Workroom />}/>
                <Route path={reverse('create_event')} element={<CreateEvent/>}/>
                <Route path={reverse('change_password')} element={<ChangePassword />} />
                <Route path={reverse('role_page')} element={<RolePage />} />
                <Route path='*' element={<NotFoundPage/>}/>
              </Routes>
            </Permissions>
          </main>
        <Footer />
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(App)
