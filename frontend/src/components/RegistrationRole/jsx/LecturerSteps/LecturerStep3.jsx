import React, {useState} from 'react'
import {useNavigate} from 'react-router-dom'
import StepsBar from "../StepsBar";
// import '~/styles/RegistrationRole.styl'

export default function LecturerStep3() {
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

  /*кнопка Следующий шаг*/
  function toLecturerStep4() {
    navigate("/register_lecturer4")
  }
  
  return (
    <>
      <StepsBar 
        style={{marginLeft: "50%"}}
        step3={{color: "var(--main-blue)"}}/>
      
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
        
        <div className="step-block margin-bottom-24">
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

        <div className="step-block margin-bottom-24">
          <p className="step-block__left-part left-part-with-textarea">Оборудование:</p>
          <textarea
            className="form__textarea textarea-height88"
            placeholder="Перечислите имеющееся для лекций оборудование">
          </textarea>
        </div>
      </div>
      <div className="steps__btns">
        <button className="btn-outline margin-right-12">Продолжить позже</button>
        <button
          className="btn"
          onClick={toLecturerStep4}>Следующий шаг</button>
      </div>
    </>
  )
}