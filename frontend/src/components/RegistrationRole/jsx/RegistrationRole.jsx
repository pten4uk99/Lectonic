import React, { useState } from 'react'
import {Routes, Route, useNavigate} from 'react-router-dom'
import {connect} from "react-redux";

import backArrow from "~/assets/img/back-arrow.svg"
import StepsBar from "./StepsBar";
import {SwapSelectedRole, SwapStep} from "../redux/actions/registerRole";
import LecturerSteps from "./LecturerSteps/LecturerSteps";
import Permissions from "../../Authorization/jsx/Permissions";
import {permissions, reverse} from "../../../ProjectConstants";


function RegistrationRole(props) {
  let navigate = useNavigate()
  
  let selectedRole = props.store.registerRole.selectedRole
  let currentStep = props.store.registerRole.step
  
  function handleChooseRole(to) {
    props.SwapSelectedRole(to)
    navigate(reverse('create_lecturer'))
  }

  return (
    <>
      <StepsBar step={currentStep}/>

      <div className="step-block-wrapper">
        <div className="choose-role__block" 
             style={currentStep > 1 ? {display: "none"} : {}}>
          <div className='step-block margin-bottom-36 step-block__head-text'>
            <h2 className='step-block__left-part'>
              Выбор роли
            </h2>
            <p className="lecturer-right__header">
              Выберите Вашу основную роль на платформе:<br/>
              лектор или заказчик лекции.
            </p>
          </div>
  
          <div className="step-block margin-bottom-36">
            <div className="step-block__left-part step-block-required">
              <p>Кто вы?</p>
              <span className="required-sign step-block__required-sign">*</span>
            </div>
            <button className={`${selectedRole === 'lecturer' ? "btn-role-selected" : "btn-role"} margin-right-12`} 
                    onClick={() => handleChooseRole('lecturer')}>Лектор</button>
            <button className={`${selectedRole === 'customer' ? "btn-role-selected" : "btn-role"}`} 
                    style={{cursor: 'not-allowed'}} 
                    onClick={() => {
                      // props.SwapSelectedRole('customer')
                    }}>Заказчик</button>
          </div>
        </div>
        <Routes>
          <Route path='lecturer' element={<LecturerSteps/>}/>
        </Routes>
      </div>
      
      <div className="step-block steps__btn mb-148" style={currentStep > 2 ? {display: "none"} : {}}>
        {currentStep > 1 && 
          <div className="link-to-back" onClick={() => props.SwapStep(currentStep - 1)}>
            <img src={backArrow} alt="предыдущий шаг"/>
            <span>Предыдущий шаг</span>
          </div>}
        
        <div className="step-block__left-part"/>
        <button className="btn" 
                onClick={() => props.SwapStep(currentStep + 1)} 
                disabled={!selectedRole}>Следующий шаг</button>
      </div>
    </>
  )
}


export default connect(
  state => ({store: state}),
  dispatch => ({
    SwapSelectedRole: (role) => dispatch(SwapSelectedRole(role)),
    SwapStep: (step) => dispatch(SwapStep(step))
  })
)(RegistrationRole)