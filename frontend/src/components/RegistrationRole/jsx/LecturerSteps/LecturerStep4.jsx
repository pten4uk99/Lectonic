import React, {useState} from 'react'
import {useNavigate} from 'react-router-dom'
import StepsBar from "../StepsBar";
// import '~/styles/RegistrationRole.styl'

export default function LecturerStep4() {
  const navigate = useNavigate()
  
  /*согласие с условиями пользовательского соглашения*/
  const [isAgreed, setAgreed] = useState(false)
  function changeAgreement() {
    setAgreed(!isAgreed)
  }
  
  return (
    <>
      <StepsBar 
        style={{marginLeft: "75%"}}
        step4={{color: "var(--main-blue)"}}/>

      <div className="step-block-wrapper">
        <div className='step-block margin-bottom-36 step-block__head-text'>
          <h2 className='step-block__left-part'>
            Платёжная<br/>информация
          </h2>
          <p>
            В целях правильного формирования счёта на оплату, пожалуйста, укажите
            <br/>
            реквизиты так, как они указаны в Вашем платёжном документе.
          </p>
        </div>

        <div className="step-block-with-textarea margin-bottom-24">
          <div className="step-block__left-part left-part-with-textarea step-block-required">
            <p>
              Реквизиты счёта:
            </p>
            <span className="required-sign step-block__required-sign">*</span>
          </div>
          <textarea
            className="form__textarea textarea-height178"
            placeholder="Введите реквизиты вашего счёта">
          </textarea>
        </div>

        {/*тут нужно переписать классы, чтоб был общий элемент*/}
        <div className="step-block">
          <div className="step-block__left-part"></div>
          <div>
            <div className="auth__form__checkbox-wrapper">
              <input
                className="auth__form__checkbox-switch"
                id="checkbox"
                type="checkbox"
                checked={isAgreed}
                onChange={changeAgreement}
              />
              <label htmlFor="checkbox">
                Я ознакомился и соглашаюсь с условиями пользовательского соглашения
              </label>
            </div>
            <p className="step-block__user-agreement">Условия пользовательского соглашения</p>
          </div>
        </div>
      </div>
      <div className="steps__btns">
        <button className="btn-outline margin-right-12">Продолжить позже</button>
        <button
          className="btn"
          disabled={!isAgreed}>Следующий шаг</button>
      </div>
    </>
  )
}
