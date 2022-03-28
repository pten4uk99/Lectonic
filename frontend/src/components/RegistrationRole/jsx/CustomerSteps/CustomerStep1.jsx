import React, {useEffect, useState} from 'react'
import {connect} from "react-redux";
import PhotoPreview from "../PhotoPreview";
import {getDomainArray} from "../../../WorkRooms/CreateEvent/ajax/event";
import {domainSelectHandler} from "../../../WorkRooms/CreateEvent/jsx/CreateEvent";
import {UpdateDomain} from "../../../WorkRooms/CreateEvent/redux/actions/event";
import {UpdatePassportPhoto, UpdateSelfiePhoto} from "../../redux/actions/lecturer";


function CustomerStep1(props) {
  let selectedDomains = props.store.event.domain
  let passportImage = props.store.addRole.lecturer.passport_photo
  let selfieImage = props.store.addRole.lecturer.selfie_photo
  
  let [domainArray, setDomainArray] = useState(null)
  
  useEffect(() => {
    getDomainArray()
      .then(response => response.json())
      .then(data => setDomainArray(data.data))
      .catch(error => console.log(error))
  }, [])
  
  useEffect(() => {
    if (selectedDomains.length > 0 && domainArray) {
      let newDomainArray
      newDomainArray = domainArray.filter(elem => !selectedDomains.includes(elem.name))
      setDomainArray(newDomainArray)
    }
  }, [selectedDomains])
  
  return (
    <div className="customer-step1">
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
      
      <div className="step-block mt-24">
        <p className="step-block__left-part">
          Тематика лекций:
          <span className="required-sign step-block__required-sign">*</span>
        </p>
        <div className='domain-list flex'>
            <select className='selector'
                    onChange={e => domainSelectHandler(e, props)}>
              <option value='' disabled selected>Выберите тематику</option>
              {domainArray ? domainArray.map((elem) => {
                return <option key={elem.id} value={elem.id}>{elem.name}</option>
              }): <></>}
            </select>
            {selectedDomains.map((domain, index) => {
              return <div key={index} className='pill pill-grey'>{domain}</div>
            })}
          </div>
      </div>
    </div>
  )
}


export default connect(
  state => ({store: state}),
  dispatch => ({
    UpdateDomain: (domain) => dispatch(UpdateDomain(domain)),
    UpdatePassportPhoto: (photo) => dispatch(UpdatePassportPhoto(photo)),
    UpdateSelfiePhoto: (photo) => dispatch(UpdateSelfiePhoto(photo)),
  })
)(CustomerStep1);