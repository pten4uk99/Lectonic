import React, {useEffect, useState} from 'react'
import { Link, useLocation } from 'react-router-dom'
import {connect} from "react-redux";

import logo from '~/assets/img/header_logo.svg'
import iconChat from '~/assets/img/chat-icon.svg'
import burgerMenu from "~/assets/img/burger-menu.svg";
import profileSelected from '~/assets/img/header_profile-selected.svg'
import profile from '~/assets/img/header_profile.svg'
import {
  ActivateModal,
  ActiveChatDropdown,
  ActiveProfileDropdown,
  DeactivateModal,
  SetSelectedChat
} from "../redux/actions/header";
import ProfileDropDown from "./ProfileDropDown";
import ChatDropdown from "./Notifications/ChatDropdown";
import {AddNotifications, RemoveNotification, SetNeedRead, UpdateNotifications} from "../redux/actions/notifications";
import PhotoName from "../../Utils/jsx/PhotoName";
import AuthModal from "../../Authorization/jsx/AuthModal";
import {SetNotifyConnFail} from "../redux/actions/ws";
import ErrorMessage from "../../Utils/jsx/ErrorMessage";
import {getProfileInfo} from "../../WorkRooms/WorkRoom/ajax/workRooms";
import {UpdateProfile} from "../../Profile/redux/actions/profile";


function Header(props) {
  let profileDropDownActive = props.store.header.profileDropDownActive
  let permissions = props.store.permissions
  let loggedIn = permissions.logged_in
  let isCustomer = permissions.is_customer
  let isLecturer = permissions.is_lecturer
  let {pathname} = useLocation();
  let chatActive = props.store.header.chatDropdownActive
  let [chatUnread, setChatUnread] = useState(false)
  let [headerIconsVisible, setIconsVisible] = useState(false)
  
  useEffect(() => {
    if (isCustomer || isLecturer) setIconsVisible(true)
    else setIconsVisible(false)
  }, [permissions, props.store.ws.notifyConnFail])
  
  useEffect(() => {
    if (props.store.permissions.is_person && props.store.permissions.logged_in) {
     getProfileInfo()
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          props.UpdateProfile(data.data[0])
        }
      })
      .catch(error => console.log(error))     
    }
  }, [props.store.permissions.is_person, props.store.permissions.logged_in])
  

  useEffect(() => {
    if (!chatActive) {
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
  
  return (
    <>
      <header className="header" style={{position: (pathname === '/workroom') ? 'fixed' : 'relative'}}>
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
                       onClick={() => {props.ActiveChatDropdown(!chatActive)}}/>
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
                               size={32} 
                               colorNumber={props.store.profile.bgc_number}/>
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
        
        {!loggedIn && <AuthModal/>}
        <ProfileDropDown/>
        {chatActive && (isLecturer || isCustomer) && 
          <ChatDropdown socket={props.socket}/>}
        {props.store.ws.notifyConnFail && <ErrorMessage msg="Соединение разорвано. Повторное подключение..."/>}
            
      </header>
    </>
  );
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    ActivateModal: () => dispatch(ActivateModal()),
    UpdateProfile: (data) => dispatch(UpdateProfile(data)),
    ActiveChatDropdown: (active) => dispatch(ActiveChatDropdown(active)),
    SetNotifyConnFail: (connected) => dispatch(SetNotifyConnFail(connected)),
    SetSelectedChat: (chat_id) => dispatch(SetSelectedChat(chat_id)),
    SetNeedRead: (chat_id, need_read) => dispatch(SetNeedRead(chat_id, need_read)),
    UpdateNotifications: (data) => dispatch(UpdateNotifications(data)),
    AddNotifications: (data) => dispatch(AddNotifications(data)),
    RemoveNotification: (chat_id) => dispatch(RemoveNotification(chat_id)),
    DeactivateModal: () => dispatch(DeactivateModal()),
    ActiveProfileDropdown: (active) => dispatch(ActiveProfileDropdown(active)),
  })
)(Header)

