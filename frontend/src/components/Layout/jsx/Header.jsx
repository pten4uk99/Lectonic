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
import {ActivateModal, ActiveProfileDropdown, DeactivateModal, SetSelectedChat} from "../redux/actions/header";
import ProfileDropDown from "./ProfileDropDown";
import ErrorMessage from "../../Utils/jsx/ErrorMessage";
import ChatDropdown from "./Notifications/ChatDropdown";
import {getNotificationsList} from "../ajax";
import {AddNotifications, RemoveNotification, SetNeedRead, UpdateNotifications} from "../redux/actions/notifications";


function Header(props) {
  let profileDropDownActive = props.store.header.profileDropDownActive
  let loggedIn = props.store.permissions.logged_in
  
  let [chatActive, setChatActive] = useState(false)
  let [chatUnread, setChatUnread] = useState(false)
  let [chatSocket, setChatSocket] = useState(null)
  let selectedChatId = props.store.header.selectedChatId
  
  useEffect(() => {
    getNotificationsList()
      .then(r => r.json())
      .then(data => props.UpdateNotifications(data.data))
  }, [])
  
  useEffect(() => {
    if (chatSocket && !chatActive) {
      chatSocket.close()
      props.SetSelectedChat(null)
    }
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
    let chatId = props.store.header.selectedChatId
    let eventFunction = (e) => {
      let data = JSON.parse(e.data)
      if (data.type === 'new_respondent') props.AddNotifications(data)
      if (data.type === 'remove_respondent') props.RemoveNotification(data.id)
      if (data.type === 'new_message') {
        if (chatId !== data.chat_id) props.SetNeedRead(data.chat_id, true)
      }
    }
    props.notificationsSocket?.addEventListener('message', eventFunction)
    return () => props.notificationsSocket?.removeEventListener('message', eventFunction)
  }, [props.notificationsSocket, selectedChatId])
  
  return (
    <>
      <header className="header">
        <Link to="/">
          <img className="header-logo" src={logo} alt="логотип" />
        </Link>
  
        <nav className="header__nav">
          {loggedIn ? 
            <>
              <img className="header__nav-search is-desktop" 
                   src={iconChat} 
                   alt="чат" 
                   onClick={() => setChatActive(!chatActive)}/>
              {chatUnread && <div className="need-read"/>}
              
              <div className="header__profile-photo-block" 
                   onClick={() => props.ActiveProfileDropdown(!profileDropDownActive)}>
                <img className="header__nav-profile-photo is-desktop" 
                     src={props.store.profile.photo} 
                     alt="меню"/>
              </div>
            </> : 
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
    SetSelectedChat: (chat_id) => dispatch(SetSelectedChat(chat_id)),
    SetNeedRead: (chat_id, need_read) => dispatch(SetNeedRead(chat_id, need_read)),
    UpdateNotifications: (data) => dispatch(UpdateNotifications(data)),
    AddNotifications: (data) => dispatch(AddNotifications(data)),
    RemoveNotification: (chat_id) => dispatch(RemoveNotification(chat_id)),
    DeactivateModal: () => dispatch(DeactivateModal()),
    ActiveProfileDropdown: 
      (active) => dispatch(ActiveProfileDropdown(active)),
  })
)(Header)

