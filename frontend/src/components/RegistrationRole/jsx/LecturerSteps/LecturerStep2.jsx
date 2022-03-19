import React, {useEffect, useState} from 'react'
import {connect} from "react-redux";

import PhotoPreview from "../PhotoPreview";
import {
  UpdateDiplomaPhotos,
  UpdateEducation,
  UpdatePassportPhoto,
  UpdateSelfiePhoto
} from "../../redux/actions/registerRole";


function LecturerStep2(props) {
  let diplomaImage = props.store.registerRole.diploma_photos
  let passportImage = props.store.registerRole.passport_photo
  let selfieImage = props.store.registerRole.selfie_photo
  let education = props.store.registerRole.education

  
  return (
      <div className="step-block-wrapper">
        <div className='step-block margin-bottom-36 step-block__head-text'>
          <h2 className='step-block__left-part'>
            Ваши документы
          </h2>
          <p className="lecturer-right__header">
            Для дальнейшей работы необходимо загрузить документы,<br/>
            подтверждающие Ваш уровень образования и квалификацию.
          </p>
        </div>

        <div className="upload-photo__block">
          <div className="upload-photo__label">
            <p>
              Диплом о высшем образовании, диплом<br/>
              о переквалификации и/или иные сертификаты,<br/>
              подтверждающие Ваш профессиональный уровень:
            </p>
          </div>
          <PhotoPreview set={props.UpdateDiplomaPhotos} 
                        image={diplomaImage} 
                        list={true}/>
        </div>
        
        <div className="step-block-with-textarea margin-bottom-24">
          <p className="step-block__left-part left-part-with-textarea">
            Образование:
          </p>
          <textarea className="form__textarea textarea-height88" 
                    placeholder="Напишите о своём образовании в свободной форме" 
                    defaultValue={education}
                    onBlur={(e) => props.UpdateEducation(e.target.value)}>
          </textarea>
        </div>

        <div className="upload-photo__block">
          <div className="upload-photo__label">
            <p>Паспорт (первая страница):
              <span className="required-sign step-block__required-sign">*</span>
            </p>
          </div>
          <PhotoPreview set={props.UpdatePassportPhoto} 
                        image={passportImage}/>
        </div>

        <div className="upload-photo__block">
          <div className="upload-photo__label">
            <p>Ваше селфи с первой страницей паспорта:
              <span className="required-sign step-block__required-sign">*</span>
            </p>
          </div>
          <PhotoPreview set={props.UpdateSelfiePhoto} 
                        image={selfieImage} 
                        style={{marginBottom: 5}}/>
        </div>

        <div className="step-block">
          <div className="step-block__left-part"/>
          <p className="step-block__right-comment lecturer">
            Убедитесь, что фотография получилась чёткой и что все данные первого
            разворота паспорта хорошо видны. Лицо и паспорт должны полностью
            просматриваться (JPG/PNG размером не менее 800х600 px)
          </p>
        </div>
      </div>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    UpdateDiplomaPhotos: (photo) => dispatch(UpdateDiplomaPhotos(photo)),
    UpdatePassportPhoto: (photo) => dispatch(UpdatePassportPhoto(photo)),
    UpdateSelfiePhoto: (photo) => dispatch(UpdateSelfiePhoto(photo)),
    UpdateEducation: (education) => dispatch(UpdateEducation(education)),
  })
)(LecturerStep2)
