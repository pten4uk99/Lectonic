import React, {useEffect, useState} from 'react'
import {connect} from "react-redux";
import { Routes, Route} from 'react-router-dom'

import Index from '~@/Layout/jsx/Index'
import Footer from '~@/Layout/jsx/Footer'
import NotFoundPage from '~@/Layout/jsx/NotFoundPage'
import VerifyEmail from '~@/Layout/jsx/VerifyEmail'
import ChangePassword from '~@/Layout/jsx/ChangePassword'
import ConfirmEmail from '~@/Authorization/jsx/ConfirmEmail'
import SetProfileInfo from '~@/Profile/jsx/SetProfileInfo'
import RegistrationRole from '~@/RegistrationRole/jsx/RegistrationRole'
import Workroom from "~@/WorkRooms/Workroom"
import CreateEvent from "~@/WorkRooms/CreateEvent/jsx/CreateEvent"
import Header from "~@/Layout/jsx/Header"
import RolePage from "~@/Pages/RolePage/jsx/RolePage";
import Permissions from "./components/Authorization/jsx/Permissions";
import {reverse} from "./ProjectConstants";
import Lecture from "./components/Pages/Lecture/jsx/Lecture";
import {ActiveChatDropdown, ActiveProfileDropdown} from "./components/Layout/redux/actions/header";
import WebSocket from "./components/Layout/jsx/WebSocket";


function App(props) {
  let [socket, setSocket] = useState(null)

  useEffect(() => {
    if (props.store.header.modalActive) document.body.style.overflowY = 'hidden'
    else document.body.style = null
  }, [props.store.header.modalActive])
  
  return (
    <>
      <Header socket={socket}/>
      <WebSocket setSocket={setSocket} socket={socket}/>
        <main onClick={() => {props.ActiveProfileDropdown(false); props.ActiveChatDropdown(false)}}>
          <Permissions>
            <Routes>
              <Route path={reverse('index')} element={<Index/>}/>
              <Route path={reverse('verify_email')} element={<VerifyEmail />} />
              <Route path={reverse('confirm_email')} element={<ConfirmEmail />} />
              <Route path={reverse('continue_signup')} element={<></>} />
              <Route path={reverse('create_profile')} element={<SetProfileInfo />}/>
              <Route path={reverse('set_profile')} element={<SetProfileInfo />}/>
              <Route path='/add_role/*' element={<RegistrationRole/>}/>
              <Route path={reverse('workroom')} element={<Workroom />}/>
              <Route path={reverse('create_event')} element={<CreateEvent/>}/>
              <Route path={reverse('change_password')} element={<ChangePassword />} />
              <Route path={reverse('role_page')} element={<RolePage />} />
              <Route path={reverse('lecture')} element={<Lecture/>} />
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
  dispatch => ({
    ActiveChatDropdown: (active) => dispatch(ActiveChatDropdown(active)),
    ActiveProfileDropdown: (active) => dispatch(ActiveProfileDropdown(active)),
  })
)(App)
