import React, {useEffect, useState} from 'react'
import {connect} from "react-redux";

import Modal from '~@/Layout/jsx/Modal'
import CreatePassword from './Elements/CreatePassword'
import {ActivateModal, DeactivateModal} from "../../Layout/redux/actions/header";
import {useLocation, useNavigate} from "react-router-dom";
import {reverse, reverseEqual} from "../../../ProjectConstants";
import Authorization from "./Authorization";


function AuthModal(props) {
  let location = useLocation()
  let navigate = useNavigate()
  
  let modalActive = props.store.header.modalActive
  let loggedIn = props.store.permissions.logged_in
  
  let emailConfirmed = reverseEqual('continue_signup', location.pathname)
  
  useEffect(() => {
    if (emailConfirmed) {
      props.ActivateModal()
      if (!location.state) {
        navigate(reverse('workroom'))
        props.DeactivateModal()
      }
    }
  }, [emailConfirmed])
  
  return (
    <>
      {!loggedIn && 
        <Modal isOpened={modalActive} 
               onModalClose={() => props.DeactivateModal()} 
               styleBody={{ width: 400, height: 460 }}>
          {emailConfirmed ?
            <CreatePassword email={location.state}/> :
            <Authorization/>
          }
        </Modal>
      }
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    ActivateModal: () => dispatch(ActivateModal()),
    DeactivateModal: () => dispatch(DeactivateModal())
  })
)(AuthModal)