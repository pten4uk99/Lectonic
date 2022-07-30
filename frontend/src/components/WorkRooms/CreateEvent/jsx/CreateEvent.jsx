import React, {useEffect, useState} from 'react'
import {connect} from 'react-redux'
import {useNavigate, useSearchParams} from 'react-router-dom'


import backArrow from '~/assets/img/back-arrow.svg'
import {SwapModalChooseDates} from '../../FullCalendar/Calendar/redux/actions/calendar'
import {checkWorkroomPermissions} from '../services/permissions'
import {selectedDomainsRender, singleRender} from '../services/effects'
import {handleCreateEvent} from '../services/server'
import Header from './Elements/Header'
import Domain from './Elements/Domain'
import LectureName from './Elements/LectureName'
import LectureType from './Elements/LectureType'
import LectureDates from './Elements/LectureDates'
import Listeners from './Elements/Listeners'
import HallAddress from './Elements/HallAddress'
import Equipment from './Elements/Equipment'
import Description from './Elements/Description'
import Price from './Elements/Price'
import Submit from './Elements/Submit'


function CreateEvent(props) {
  let [responseLoaded, setResponseLoaded] = useState(true)
  let navigate = useNavigate()
  let [searchParams, setSearchParams] = useSearchParams()

  let perms = props.store.permissions
  let checkPerms = () => checkWorkroomPermissions(perms, navigate)

  useEffect(checkPerms, [perms.is_lecturer, perms.is_customer])

  let role = searchParams.get('role')
  let edit = searchParams.get('edit')
  let [lectureData, setLectureData] = useState(null)
  let calendar = props.store.calendar
  let event = props.store.event

  let chooseDates = calendar.modalChooseDates
  let duration = calendar.chosenDuration
  let selectedDomains = event.domain
  let eventType = event.type
  let place = event.place
  let equipment = event.equipment
  let payment = event.payment
  let [domainArray, setDomainArray] = useState([])
  let [lectureName, setLectureName] = useState('')


  let [requiredFields, setRequiredFields] = useState({
    name: lectureName,
    date: chooseDates,
  })

  let [errorMessages, setErrorMessages] = useState({
    name: '',
    datetime: '',
  })

  useEffect(() => {
    setRequiredFields({...requiredFields, date: chooseDates, name: lectureName})
  }, [chooseDates, lectureName])

  useEffect(() => singleRender(
    role, edit, props.SwapModalChooseDates, setRequiredFields, 
    requiredFields, setDomainArray, setLectureData), [])

  useEffect(() => selectedDomainsRender(selectedDomains, domainArray, setDomainArray), [selectedDomains])

  function submitFormHandler(e) {
    handleCreateEvent(
      e, setResponseLoaded, selectedDomains, chooseDates,
      eventType, duration, role, navigate, setErrorMessages, lectureData)
  }

  return (
    <>
      <div className="navigate-back__block" onClick={() => navigate(-1)}>
        <img src={backArrow} alt="назад"/>
        <span style={{marginLeft: 10, fontSize: 11}}>Назад</span>
      </div>

      <form onSubmit={(e) => submitFormHandler(e)}>
        <div className={`create-event__wrapper ${role === 'customer' && 'customer'}`}>
          <Header role={role} edit={edit}/>

          <Domain domainArray={domainArray}
                  setDomainArray={setDomainArray}
                  selectedDomains={selectedDomains}
                  lectureData={lectureData}/>
          <LectureName setLectureName={setLectureName}
                       errorMessages={errorMessages}
                       lectureData={lectureData}/>
          <LectureType eventType={eventType} lectureData={lectureData}/>
          <LectureDates chooseDates={chooseDates} errorMessages={errorMessages} lectureData={lectureData}/>
          <Listeners role={role}
                     requiredFields={requiredFields}
                     setRequiredFields={setRequiredFields}
                     errorMessages={errorMessages} 
                     lectureData={lectureData}/>
          <HallAddress place={place} lectureData={lectureData}/>
          <Equipment equipment={equipment} lectureData={lectureData}/>
          <Description lectureData={lectureData}/>
          <Price payment={payment} lectureData={lectureData}/>

          <Submit responseLoaded={responseLoaded} requiredFields={requiredFields} lectureData={lectureData}/>
        </div>
      </form>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SwapModalChooseDates: (dates) => dispatch(SwapModalChooseDates(dates)),
  })
)(CreateEvent)

