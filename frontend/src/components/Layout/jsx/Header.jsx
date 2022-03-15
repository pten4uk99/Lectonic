import React, {useState} from 'react'
import { Link } from 'react-router-dom'
import logo from '~/assets/img/header_logo.svg'
import iconSearch from '~/assets/img/icon-search.svg'
import burgerMenu from "~/assets/img/burger-menu.svg";
import profileSelected from '~/assets/img/header_profile-selected.svg'
import profile from '~/assets/img/header_profile.svg'
import Modal from "./Modal";
import Authorization from "../../Authorization/jsx/Authorization";
import {ActivateModal, DeactivateModal} from "../redux/actions/header";
import {connect} from "react-redux";


function Header(props) {
  return (
    <>
      <header className="header">
        <Link to="/">
          <img className="header-logo" src={logo} alt="логотип" />
        </Link>
  
        <nav className="header__nav">
          <img className="header__nav-search is-desktop"
               src={iconSearch}
               alt="поиск" />
  
          <img
            className="header__nav-profile is-desktop"
            src={props.store.header.modalActive ? profileSelected : profile}
            alt="меню"
            onClick={props.ActivateModal}
          />
  
          {/*бургер под мобильные*/}
          <img
            className="header__nav-burger is-mobile"
            src={burgerMenu}
            alt="меню"
          />
        </nav>
      </header>
      <Modal
        isOpened={props.store.header.modalActive}
        onModalClose={() => props.DeactivateModal()}
        styleBody={{ width: '400px' }}>
        <Authorization />
      </Modal>
    </>
  );
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    ActivateModal: () => dispatch(ActivateModal()),
    DeactivateModal: () => dispatch(DeactivateModal())
  })
)(Header)