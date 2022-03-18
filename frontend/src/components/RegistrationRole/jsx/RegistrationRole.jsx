import React, { useState } from 'react'
import {useNavigate} from 'react-router-dom'

import LecturerStep1 from './LecturerSteps/LecturerStep1'
import LecturerStep2 from './LecturerSteps/LecturerStep2'
import LecturerStep3 from './LecturerSteps/LecturerStep3'
import LecturerStep4 from './LecturerSteps/LecturerStep4'
import ChooseRole_Customer_step1 from './IndividualSteps/ChooseRole_Customer_step1'
import ChooseRole_Customer_step2 from './IndividualSteps/ChooseRole_Customer_step2'
import ChooseRole_Customer_step3 from './IndividualSteps/ChooseRole_Customer_step3'
import ChooseRole_Customer_step4 from './IndividualSteps/ChooseRole_Customer_step4'
import profileSelected from '~/assets/img/header_profile-selected.svg'
import StepsBar from "./StepsBar";
import {SwapSelectedRole, SwapStep} from "../redux/actions/registerRole";
import {connect} from "react-redux";
import LecturerSteps from "./LecturerSteps/LecturerSteps";


function RegistrationRole(props) {
  let selectedRole = props.store.registerRole.selectedRole
  let currentStep = props.store.registerRole.step
  const navigate = useNavigate()
  
  function handleChooseRole(to) {
    props.SwapSelectedRole(to)
    props.SwapStep(1)
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
            <p>
              Выберите Вашу основную роль на платформе:
              <br/>
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

        {selectedRole === 'lecturer' && <LecturerSteps/>}
      </div>
      
      <div className="step-block steps__btn" style={currentStep > 2 ? {display: "none"} : {}}>
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