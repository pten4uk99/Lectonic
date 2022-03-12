import React, { useState } from 'react'
import {useNavigate} from 'react-router-dom'
import Header from '~@/Layout/jsx/Header'
// import '~/styles/RegistrationRole.styl'
// import DropDownElement from '~@/UserArea/jsx/DropdownElement'
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

export default function RegistrationRole() {
  const navigate = useNavigate()
  
  /*переключение блоков Лектор/Заказчик*/
  const [lecturerSelected, setLecturerSelected] = useState(false);
  const [customerSelected, setCustomerSelected] = useState(false);

  function saysLecturer() {
    setLecturerSelected(true);
    setCustomerSelected(false);
  }

  function saysCustomer() {
    setLecturerSelected(false);
    setCustomerSelected(true);
  }
  
  /*кнопка Следующий шаг*/
  function toLecturerStep2() {
    navigate("/register_lecturer2")
  }

  return (
    <>
      <Header src={profileSelected} />
      <StepsBar
        step1={{color: "var(--main-blue)"}}/>

      <div className="step-block-wrapper">
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
            <p>
              Кто вы?
            </p>
            <span className="required-sign step-block__required-sign">*</span>
          </div>
          <button
            className={`${lecturerSelected ? "btn-role-selected" : "btn-role"} margin-right-12`}
            onClick={saysLecturer}>Лектор</button>
          <button
            className={`${customerSelected ? "btn-role-selected" : "btn-role"}`}
            onClick={saysCustomer}>Заказчик</button>
        </div>

        {lecturerSelected && <LecturerStep1 />}
        
      </div>
      <div className="step-block steps__btn">
        <div className="step-block__left-part"></div>
        <button
          className="btn"
          onClick={toLecturerStep2}
          disabled={!lecturerSelected && !customerSelected}>Следующий шаг</button>
      </div>
    </>
  )
}
