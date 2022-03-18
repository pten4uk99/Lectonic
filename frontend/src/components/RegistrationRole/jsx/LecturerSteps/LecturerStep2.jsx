import React, {useState} from 'react'
import {connect} from "react-redux";
import {addPhotoHandler} from "../../../CreateEvent/jsx/CreateEvent";
import PhotoPreview from "../PhotoPreview";


function LecturerStep2() {
  let [diplomaImage, setDiplomaImages] = useState('')
  let [passportImage, setPassportImage] = useState('')
  let [selfieImage, setSelfieImage] = useState('')
  
  return (
    <>
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

        <div className="diploma__block">
          <div className="diploma-photo__label">
            <p>
              Диплом о высшем образовании, диплом 
              <br/>о переквалификации и/или иные сертификаты,
              <br/>подтверждающие Ваш профессиональный уровень:
            </p>
          </div>
          <PhotoPreview set={setDiplomaImages} image={diplomaImage}/>
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
          <label className="btn-file">
            Выбрать файл
            <input type="file" 
                   accept="image/*" 
                   onChange={e => addPhotoHandler(e, setPassportImage)}/>
          </label>
        </div>

        <div className="step-block">
          <div className="step-block__left-part step-block-required">
            <p>
              Ваше селфи с первой страницей паспорта:
            </p>
            <span className="required-sign step-block__required-sign">*</span>
          </div>
          <label className="btn-file">
            Выбрать файл
            <input type="file" 
                   accept="image/*" 
                   onChange={e => addPhotoHandler(e, setSelfieImage)}/>
          </label>
        </div>

        <div className="step-block">
          <div className="step-block__left-part"/>
          <p className="step-block__right-comment">
            Убедитесь, что фотография получилась чёткой и что все данные первого
            разворота паспорта хорошо видны. Лицо и паспорт должны полностью
            просматриваться (JPG/PNG размером не менее 800х600 px)
          </p>
        </div>
      </div>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(LecturerStep2)
