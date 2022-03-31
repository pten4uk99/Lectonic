import React, {useState} from 'react'
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


function Header(props) {
  let profileDropDownActive = props.store.header.profileDropDownActive
  let loggedIn = props.store.permissions.logged_in
  
  let [chatActive, setChatActive] = useState(false)
  
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
      {chatActive && <ChatDropdown notificationsSocket={props.notificationsSocket}/>}
      {props.store.header.errorMessage && <ErrorMessage/>}
    </>
  );
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    ActivateModal: () => dispatch(ActivateModal()),
    DeactivateModal: () => dispatch(DeactivateModal()),
    ActiveProfileDropdown: 
      (active) => dispatch(ActiveProfileDropdown(active)),
  })
)(Header)

