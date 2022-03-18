import React, { useState } from 'react'
import {useNavigate} from 'react-router-dom'

import {connect} from "react-redux";
import {SwapSelectedRole, SwapStep} from "../../redux/actions/registerRole";
import LecturerStep1 from "./LecturerStep1";
import LecturerStep2 from "./LecturerStep2";
import LecturerStep3 from "./LecturerStep3";
import {createLecturer} from "../../ajax";


function LecturerSteps(props) {
  let currentStep = props.store.registerRole.step
  
  function handleSubmit(e) {
    e.preventDefault()
    let formData = new FormData(e.target)
    createLecturer(formData)
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.log(error))
  }

  return (
    <form onSubmit={(e) => handleSubmit(e)}>
      {currentStep === 0 ? 
        <></> :
        currentStep === 1 ?
        <LecturerStep1/> :
          currentStep === 2 ?
        <LecturerStep2/> : 
            currentStep === 3 ? 
              <LecturerStep3/> : 
              <></>}
    </form>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SwapSelectedRole: (role) => dispatch(SwapSelectedRole(role)),
    SwapStep: (step) => dispatch(SwapStep(step))
  })
)(LecturerSteps)