import React, {useState} from 'react'
import {useNavigate} from 'react-router-dom'
import StepsBar from "../StepsBar";
import DropDownTest from "../../../UserArea/jsx/DropDownTest";
// import '~/styles/RegistrationRole.styl'

export default function LecturerStep2() {
  const navigate = useNavigate()
  
  /*загрузка файлов*/
  const [chosenFile, setChosenFile] = useState(null) //выбранный файл для отправки на сервер
  const [avatarUploaded, setAvatarUploaded] = useState(null)
  
  /*кнопка Следующий шаг*/
  function toLecturerStep3() {
    navigate("/register_lecturer3")
  }
  
  return (
    <>
      <StepsBar 
        style={{marginLeft: "33%"}}
        step2={{color: "var(--main-blue)"}}/>

      <div className="step-block-wrapper">
        <div className='step-block margin-bottom-36 step-block__head-text'>
          <h2 className='step-block__left-part'>
            Ваши документы
          </h2>
          <p>
            Для дальнейшей работы необходимо загрузить документы,
            <br/>
            подтверждающие Ваш уровень образования и квалификацию.
          </p>
        </div>

        <div className="step-block margin-bottom-24">
          <div className="step-block__left-part">
            <p>
              Диплом о высшем образовании, диплом 
              <br/>о переквалификации и/или иные сертификаты,
              <br/>подтверждающие Ваш профессиональный уровень:
            </p>
          </div>
          <button 
            className="btn-file"
            >Выбрать файл</button>
        </div>

        <div className="step-block-with-textarea margin-bottom-24">
          <p className="step-block__left-part left-part-with-textarea">
            Образование:
          </p>
          <textarea
            className="form__textarea textarea-height88"
            placeholder="Напишите о своём образовании в свободной форме">
          </textarea>
        </div>

        <div className="step-block margin-bottom-24">
          <div className="step-block__left-part step-block-required">
            <p className='step-block__right-part'>
              Паспорт (первая страница):
            </p>
            <span className="required-sign step-block__required-sign">*</span>
          </div>
          <button className="btn-file">Выбрать файл</button>
        </div>

        <div className="step-block">
          <div className="step-block__left-part step-block-required">
            <p>
              Ваше селфи с первой страницей паспорта:
            </p>
            <span className="required-sign step-block__required-sign">*</span>
          </div>
          <button className="btn-file">Выбрать файл</button>
        </div>

        <div className="step-block">
          <div className="step-block__left-part"></div>
          <p className="step-block__right-comment">
            Убедитесь, что фотография получилась чёткой и что все данные первого
            разворота паспорта хорошо видны. Лицо и паспорт должны полностью
            просматриваться (JPG/PNG размером не менее 800х600 px)
          </p>
        </div>
      </div>
      <div className="step-block steps__btn">
        <div className="step-block__left-part"></div>
        <button
          className="btn"
          onClick={toLecturerStep3}>Следующий шаг</button>
      </div>
    </>
  )
}
