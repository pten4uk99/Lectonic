import React, {useEffect, useState} from 'react'
import Modal from '~@/Layout/jsx/Modal'
import AuthSignUpPassword from './AuthSignUpPassword'
import {connect} from "react-redux";
import {ActivateModal, DeactivateModal} from "../../Layout/redux/actions/header";
import {useLocation} from "react-router-dom";

function ContinueRegistration(props) {
  let location = useLocation()

  useEffect(() => {
    props.ActivateModal()
    window.localStorage.setItem('email', 'admin@admin.ru')
  }, [])
  
  return (
    <div>
      <Modal styleBody={{ width: '400px' }}>
        <AuthSignUpPassword email={location.state}/>
      </Modal>
      <div className="continue-register-main"/>
    </div>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    ActivateModal: () => dispatch(ActivateModal()),
    DeactivateModal: () => dispatch(DeactivateModal())
  })
)(ContinueRegistration)