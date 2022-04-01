import React, {useEffect, useState} from 'react'
import { Link } from 'react-router-dom'
import {connect} from "react-redux";

import logo from '~/assets/img/header_logo.svg'
import iconChat from '~/assets/img/chat-icon.svg'
import burgerMenu from "~/assets/img/burger-menu.svg";
import profileSelected from '~/assets/img/header_profile-selected.svg'
import profile from '~/assets/img/header_profile.svg'
import Modal from "./Modal";
import Authorization from "../../Authorization/jsx/Authorization";
import {ActivateModal, ActiveProfileDropdown, DeactivateModal} from "../redux/actions/header";
import ProfileDropDown from "./ProfileDropDown";
import ErrorMessage from "../../Utils/jsx/ErrorMessage";
import ChatDropdown from "./Notifications/ChatDropdown";
import {getNotificationsList} from "../ajax";
import {AddNotifications, RemoveNotification, UpdateNotifications} from "../redux/actions/notifications";


function Header(props) {
  let profileDropDownActive = props.store.header.profileDropDownActive
  let loggedIn = props.store.permissions.logged_in
  
  let [chatActive, setChatActive] = useState(false)
  let [chatUnread, setChatUnread] = useState(false)
  let [chatSocket, setChatSocket] = useState(null)
  
  useEffect(() => {
    getNotificationsList()
      .then(r => r.json())
      .then(data => props.UpdateNotifications(data.data))
  }, [])
  
  useEffect(() => {
    if (chatSocket && !chatActive) chatSocket.close()
  }, [chatActive])
  
  useEffect(() => {
    let need_read = false
    for (let elem of props.store.notifications) {
      if (elem?.need_read) {
        need_read = true
        break
      }
    }
    setChatUnread(need_read)
  }, [props.store.notifications])
  
  useEffect(() => {
    props.notificationsSocket?.addEventListener('message', (e) => {
      let data = JSON.parse(e.data)
      if (data.type === 'new_respondent') props.AddNotifications(data)
      if (data.type === 'remove_respondent') props.RemoveNotification(data.id)
    })
  }, [props.notificationsSocket])
  
  return (
    <>
      <header className="header">
        <Link to="/">
          <img className="header-logo" src={logo} alt="логотип" />
        </Link>
  
        <nav className="header__nav">
          <img className="header__nav-search is-desktop"
               src={iconChat}
               alt="чат" 
               onClick={() => setChatActive(!chatActive)}/>
          {chatUnread && <div className="need-read"/>}

          {loggedIn ?
            <div className="header__profile-photo-block" 
                 onClick={() => props.ActiveProfileDropdown(!profileDropDownActive)}>
              <img className="header__nav-profile-photo is-desktop" 
                   src={props.store.profile.photo} 
                   alt="меню"/>
            </div> : 
            <img className="header__nav-profile is-desktop" 
                 src={props.store.header.modalActive ? profileSelected : profile} 
                 alt="меню" 
                 onClick={props.ActivateModal}/>}
  
          {/*бургер под мобильные*/}
          <img className="header__nav-burger is-mobile" 
               src={burgerMenu} 
               alt="меню"/>
        </nav>
      </header>
      <Modal isOpened={props.store.header.modalActive} 
             onModalClose={() => props.DeactivateModal()} 
             styleBody={{ width: '400px' }}>
        <Authorization />
      </Modal>
      <ProfileDropDown/>
      {chatActive && <ChatDropdown notificationsSocket={props.notificationsSocket} 
                                   chatSocket={chatSocket} 
                                   setChatSocket={setChatSocket}/>}
      {props.store.header.errorMessage && <ErrorMessage/>}
    </>
  );
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    ActivateModal: () => dispatch(ActivateModal()),
    UpdateNotifications: (data) => dispatch(UpdateNotifications(data)),
    AddNotifications: (data) => dispatch(AddNotifications(data)),
    RemoveNotification: (chat_id) => dispatch(RemoveNotification(chat_id)),
    DeactivateModal: () => dispatch(DeactivateModal()),
    ActiveProfileDropdown: 
      (active) => dispatch(ActiveProfileDropdown(active)),
  })
)(Header)

