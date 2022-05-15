import React, {useState} from 'react'
import {useNavigate} from 'react-router-dom'
import {connect} from "react-redux";

import backArrow from "~/assets/img/back-arrow.svg"
import {SwapStep, UpdateEquipment, UpdateHallAddress} from "../../redux/actions/registerRole";


function LecturerStep3(props) {
  let address = props.store.registerRole.hall_address
  let equipment = props.store.registerRole.equipment
  
  /*переключение блоков Да/Нет*/
  const [yesSelected, setYesSelected] = useState(false);
  const [noSelected, setNoSelected] = useState(true);
 
  function saysYes() {
    setYesSelected(true);
    setNoSelected(false);
  }
  
  function saysNo() {
    setYesSelected(false);
    setNoSelected(true);
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
             style={{color: noSelected ? "var(--add-darkGrey" : ""}}>
            Адрес:
          </p>
          <textarea className="form__textarea textarea-height88" 
                    placeholder="Введите адрес помещения для лекций" 
                    readOnly={noSelected}
                    defaultValue={address}
                    onBlur={(e) => props.UpdateHallAddress(e.target.value)}>
          </textarea>
        </div>

        <div className="step-block-with-textarea margin-bottom-24">
          <p className="step-block__left-part left-part-with-textarea">Оборудование:</p>
          <textarea className="form__textarea textarea-height88" 
                    placeholder="Перечислите имеющееся для лекций оборудование" 
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
      
      <div className="step-block steps__btn mb-148">
          <div className="link-to-back" onClick={() => props.SwapStep(2)}>
            <img src={backArrow} alt="предыдущий шаг"/>
            <span>Предыдущий шаг</span>
          </div>
        <div className="step-block__left-part"/>
        <button className="btn" type="submit">Завершить регистрацию</button>
      </div>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SwapStep: (step) => dispatch(SwapStep(step)),
    UpdateHallAddress: (address) => dispatch(UpdateHallAddress(address)),
    UpdateEquipment: (equipment) => dispatch(UpdateEquipment(equipment)),
  })
)(LecturerStep3)