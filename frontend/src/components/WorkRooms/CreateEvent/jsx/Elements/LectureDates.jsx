import React, {useEffect} from 'react'
import {connect} from 'react-redux'

import calendarIcon from '~/assets/img/event/calendar-icon.svg'
import CalendarModal, {getMonth} from '../CalendarModal'
import Modal from '../../../../Layout/jsx/Modal'
import {ActivateModal} from '../../../../Layout/redux/actions/header'
import {SwapModalChooseDates} from '../../../FullCalendar/Calendar/redux/actions/calendar'


function LectureDates(props) {
  let chooseDates = props.chooseDates
  let errorMessages = props.errorMessages
  let lectureData = props.lectureData

  useEffect(() => {
    if (lectureData) {
      let dates = []
      for (let date of lectureData.dates) {
        let newDate = new Date(date.start)
        dates.push(newDate)
      }
      props.SwapModalChooseDates(dates)
    }
  }, [lectureData])
  
  function handleCancelPress() {
    if (!lectureData) props.SwapModalChooseDates([])
  }

  return (
    <>
      <div className='date-l label'>
        Дата:
        <span className="required-sign step-block__required-sign">*</span>
      </div>
      <div className='date flex'>
        <div className='open-calendar' onClick={props.ActivateModal}>
          <img src={calendarIcon} alt=""/>
          {chooseDates.length > 0 ?
            chooseDates.map((elem, index) => (
              <div className="calendar-modal__date create-event ml-8" key={index}>
                {elem.getDate()} {getMonth(elem.getMonth())}
              </div>)) :
            <div className='date-link'>Открыть календарь</div>}

        </div>
        <Modal styleWrapper={{background: 'background: rgba(0, 5, 26, 1)'}}
               styleBody={{width: 1045, height: 681}}
               onCancel={handleCancelPress}>
          <CalendarModal/>
        </Modal>
      </div>
      {errorMessages.datetime && (<div className='form__input-error'
                                       style={{
                                         gridArea: 'date',
                                         transform: 'translateY(25px)'
                                       }}>{errorMessages.datetime[0]}</div>)}

    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    ActivateModal: () => dispatch(ActivateModal()),
    SwapModalChooseDates: (dates) => dispatch(SwapModalChooseDates(dates)),
  })
)(LectureDates)
