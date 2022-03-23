import React, {useEffect, useState} from 'react'
import Modal from '~@/Layout/jsx/Modal'
import AuthSignUpPassword from './AuthSignUpPassword'
import {connect} from "react-redux";
import {ActivateModal, DeactivateModal} from "../../Layout/redux/actions/header";
import {useLocation, useNavigate} from "react-router-dom";
import {reverse} from "../../../ProjectConstants";

function ContinueRegistration(props) {
  let location = useLocation()
  let navigate = useNavigate()

  useEffect(() => {
    props.ActivateModal()
    if (!location.state) {
      navigate(reverse('workroom'))
      props.DeactivateModal()
    }
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