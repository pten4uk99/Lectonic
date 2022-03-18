import React, {useState} from 'react'
import {useNavigate} from 'react-router-dom'
import {connect} from "react-redux";


function LecturerStep3() {
  const navigate = useNavigate()

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

  /*кнопка Следующий шаг*/
  function toLecturerStep4() {
    navigate("/register_lecturer4")
  }
  
  return (
    <>
      <div className="step-block-wrapper">
        <div className='step-block margin-bottom-36 step-block__head-text'>
          <h2 className='step-block__left-part'>
            Дополнительная<br/>информация
          </h2>
          <p>
            Если у Вас имеется помещение и/или оборудование, которые Вы хотитe
            <br/>
            использовать для проведения лекций, пожалуйста, заполните поля ниже.
          </p>
        </div>

        <div className="step-block margin-bottom-12">
          <p className="step-block__left-part">Помещение для лекций:</p>
          <button 
            className={`${yesSelected ? "btn-role-selected" : "btn-role"} margin-right-12`}
            onClick={saysYes}>Есть</button>
          <button
            className={`${noSelected ? "btn-role-selected" : "btn-role"}`}
            onClick={saysNo}>Нет</button>
        </div>
        
        <div className="step-block-with-textarea margin-bottom-24">
          <p 
            className="step-block__left-part left-part-with-textarea"
            style={{color: noSelected ? "var(--add-darkGrey" : ""}}>
            Адрес:
          </p>
          <textarea
            className="form__textarea textarea-height88"
            placeholder="Введите адрес помещения для лекций"
            disabled={noSelected}>
          </textarea>
        </div>

        <div className="step-block-with-textarea margin-bottom-24">
          <p className="step-block__left-part left-part-with-textarea">Оборудование:</p>
          <textarea
            className="form__textarea textarea-height88"
            placeholder="Перечислите имеющееся для лекций оборудование">
          </textarea>
        </div>
        
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
      
      <div className="step-block steps__btn">
        <div className="step-block__left-part"/>
        <button className="btn" type="submit">Завершить регистрацию</button>
      </div>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(LecturerStep3)