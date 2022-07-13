import React, {useState} from 'react'
import {connect} from "react-redux";

import backArrow from "~/assets/img/back-arrow.svg"
import {UpdateEquipment, UpdateHallAddress} from "../../redux/actions/lecturer";
import {SwapAddRoleStep} from "../../redux/actions/main";


function LecturerStep3(props) {
  let address = props.store.addRole.lecturer.hall_address
  let equipment = props.store.addRole.lecturer.equipment
  
  /*переключение блоков Да/Нет*/
  const [yesSelected, setYesSelected] = useState(false);
  const [noSelected, setNoSelected] = useState(true);
  const [yesSelectedEquip, setYesSelectedEquip] = useState(false);
  const [noSelectedEquip, setNoSelectedEquip] = useState(true);
 
  function saysYes() {
    setYesSelected(true);
    setNoSelected(false);
  }
  
  function saysNo() {
    setYesSelected(false);
    setNoSelected(true);
  }

  function saysYesEquip() {
    setYesSelectedEquip(true);
    setNoSelectedEquip(false);
  }
  
  function saysNoEquip() {
    setYesSelectedEquip(false);
    setNoSelectedEquip(true);
  }

  /*согласие с условиями пользовательского соглашения*/
  const [isAgreed, setAgreed] = useState(false)
  function changeAgreement() {
    setAgreed(!isAgreed)
  }
  
  return (
    <>
      <div className="step-block-wrapper">
        <div className='step-block margin-bottom-36 step-block__head-text'>
          <h2 className='step-block__left-part'>
            Дополнительная<br/>
            информация
          </h2>
          <p className="lecturer-right__header">
            Если у Вас имеется помещение и/или оборудование, которые Вы хотитe<br/>
            использовать для проведения лекций, пожалуйста, заполните поля ниже.
          </p>
        </div>

        <div className="step-block margin-bottom-12">
          <p className="step-block__left-part">Помещение для лекций:</p>
          <button className={`${yesSelected ? "btn-role-selected" : "btn-role"} margin-right-12`} 
                  type='button'
                  onClick={saysYes}>Есть</button>
          <button className={`${noSelected ? "btn-role-selected" : "btn-role"}`} 
                  type='button'
                  onClick={saysNo}>Нет</button>
        </div>
        
        <div className="step-block-with-textarea margin-bottom-24">
          <p className="step-block__left-part left-part-with-textarea" 
             style={{color: noSelected ? "var(--add-darkGrey)" : ""}}>
            Адрес:
          </p>
          <textarea className={`form__textarea textarea-height88 ${noSelected && 'disabled'}`}
                    placeholder="Введите адрес помещения для лекций" 
                    readOnly={noSelected}
                    defaultValue={address}
                    onBlur={(e) => props.UpdateHallAddress(e.target.value)}>
          </textarea>
        </div>

        <div className="step-block margin-bottom-12">
          <p className="step-block__left-part">Оборудование:</p>
          <button className={`${yesSelectedEquip ? "btn-role-selected" : "btn-role"} margin-right-12`} 
                  type='button'
                  onClick={saysYesEquip}>Есть</button>
          <button className={`${noSelectedEquip ? "btn-role-selected" : "btn-role"}`} 
                  type='button'
                  onClick={saysNoEquip}>Нет</button>
        </div>

        <div className="step-block-with-textarea margin-bottom-24">
        <p className="step-block__left-part left-part-with-textarea" 
             style={{color: noSelectedEquip ? "var(--add-darkGrey)" : ""}}>
               Список оборудования:
          </p>
          <textarea className={`form__textarea textarea-height88 ${noSelectedEquip && 'disabled'}`}
                    placeholder="Перечислите имеющееся для лекций оборудование" 
                    readOnly={noSelectedEquip}
                    defaultValue={equipment}
                    onBlur={(e) => props.UpdateEquipment(e.target.value)}>
          </textarea>
        </div>
        
      <div className="step-block">
        <div className="step-block__left-part"/>
        <div>
          <div className="auth__form__checkbox-wrapper">
            <input className="auth__form__checkbox-switch" 
                   id="checkbox" 
                   type="checkbox" 
                   checked={isAgreed} 
                   onChange={changeAgreement}/>
            <label htmlFor="checkbox">
              Я ознакомился и соглашаюсь с условиями пользовательского соглашения
            </label>
          </div>
          <p className="step-block__user-agreement">Условия пользовательского соглашения</p>
        </div>
      </div>
      </div>
      
      <div className="steps__underline"/>
      <div className="step-block steps__btn mb-148">
          <div className="link-to-back" onClick={() => props.SwapAddRoleStep(2)}>
            <img src={backArrow} alt="предыдущий шаг"/>
            <span>Предыдущий шаг</span>
          </div>
        <button className="btn" type="submit" disabled={!isAgreed}>Завершить регистрацию</button>
      </div>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SwapAddRoleStep: (step) => dispatch(SwapAddRoleStep(step)),
    UpdateHallAddress: (address) => dispatch(UpdateHallAddress(address)),
    UpdateEquipment: (equipment) => dispatch(UpdateEquipment(equipment)),
  })
)(LecturerStep3)