import React, {useEffect, useState} from 'react'
import { Link } from 'react-router-dom'
import {connect} from "react-redux";

import logo from '~/assets/img/header_logo.svg'
import iconChat from '~/assets/img/chat-icon.svg'
import burgerMenu from "~/assets/img/burger-menu.svg";
import profileSelected from '~/assets/img/header_profile-selected.svg'
import profile from '~/assets/img/header_profile.svg'
import {ActivateModal, ActiveProfileDropdown, DeactivateModal, SetSelectedChat} from "../redux/actions/header";
import ProfileDropDown from "./ProfileDropDown";
import ChatDropdown from "./Notifications/ChatDropdown";
import {getNotificationsList} from "../ajax";
import {AddNotifications, RemoveNotification, SetNeedRead, UpdateNotifications} from "../redux/actions/notifications";
import PhotoName from "../../Utils/jsx/PhotoName";
import AuthModal from "../../Authorization/jsx/AuthModal";
import {SetNotifyConn} from "../redux/actions/ws";
import ErrorMessage from "../../Utils/jsx/ErrorMessage";


function Header(props) {
  let profileDropDownActive = props.store.header.profileDropDownActive
  let permissions = props.store.permissions
  let loggedIn = permissions.logged_in
  let isCustomer = permissions.is_customer
  let isLecturer = permissions.is_lecturer
  
  let [chatActive, setChatActive] = useState(false)
  let [chatUnread, setChatUnread] = useState(false)
  let [headerIconsVisible, setIconsVisible] = useState(false)
  let [chatSocket, setChatSocket] = useState(null)
  let selectedChatId = props.store.header.selectedChatId
  
  useEffect(() => {
    if (isCustomer || isLecturer) setIconsVisible(true)
    else setIconsVisible(false)
  }, [permissions])
  
  useEffect(() => {
    if ((isLecturer || isCustomer) && !props.store.ws.notifyConnFail) {
      getNotificationsList()
        .then(r => r.json())
        .then(data => props.UpdateNotifications(data.data))
    }
  }, [isLecturer, isCustomer, props.store.ws.notifyConnFail])
  
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
    props.SetNotifyConn(Boolean(props.notificationsSocket))
    
    let chatId = props.store.header.selectedChatId
    let eventFunction = (e) => {
      let data = JSON.parse(e.data)
      if (data.type === 'new_respondent') props.AddNotifications(data)
      if (data.type === 'remove_respondent') props.RemoveNotification(data.id)
      if (data.type === 'new_message') {
        if (chatId !== data.chat_id) props.SetNeedRead(data.chat_id, true)
      }
      if (data.type === 'read_reject_chat') {
        if (data.response === 'deleted') chatSocket.close()
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
              {headerIconsVisible &&
                <>
                  <img className="header__nav-search is-desktop" 
                       src={iconChat} 
                       alt="чат" 
                       onClick={() => setChatActive(!chatActive)}/>
                  {chatUnread && <div className="need-read"/>}
                </>
              }

              {headerIconsVisible ? 
                <div className="header__profile-photo-block"
                     onClick={() => props.ActiveProfileDropdown(!profileDropDownActive)}>
                  {props.store.profile.photo ?
                    <img className="header__nav-profile-photo is-desktop"
                         src={props.store.profile.photo}
                         alt="меню"/> :
                    <PhotoName firstName={props.store.profile.first_name} 
                               lastName={props.store.profile.last_name} 
                               size={32}/>
                  }
                </div> : 
                <img className="header__nav-profile is-desktop"
                     src={profileSelected} 
                     alt="меню" 
                     onClick={() => props.ActiveProfileDropdown(!profileDropDownActive)}/>
              }
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

      {!loggedIn && <AuthModal/>}
      <ProfileDropDown/>
      {chatActive && (isLecturer || isCustomer) && 
        <ChatDropdown notificationsSocket={props.notificationsSocket} 
                      chatSocket={chatSocket} 
                      setChatSocket={setChatSocket}/>}
      {props.store.ws.notifyConnFail && <ErrorMessage msg="Соединение разорвано. Повторное подключение..."/>}
    </>
  );
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    ActivateModal: () => dispatch(ActivateModal()),
    SetNotifyConn: (connected) => dispatch(SetNotifyConn(connected)),
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

