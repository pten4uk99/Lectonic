import React, {useEffect, useState} from 'react'
import {connect} from "react-redux";

import Calendar from "~@/WorkRooms/FullCalendar/Calendar/jsx/Calendar";
import {MONTHS} from "~@/WorkRooms/FullCalendar/Calendar/utils/calendar";
import {DeactivateModal} from "../../../Layout/redux/actions/header";


function CalendarModal(props) {
  let checkedDate = props.store.calendar.checkedDate
  
  return (
    <div className="calendar-modal__wrapper">
      <Calendar/>
      <div className="calendar-modal__right-block">
        <p className="calendar-modal__header">Выбор дат</p>
        <p className="calendar-modal__tooltip">
          Отметьте одну или несколько дат на календаре.
        </p>
        <div className="calendar-modal__dates-block">
          <span>Вы выбрали:</span>
          <div className="calendar-modal__dates-list">
            {checkedDate && 
              <div className="calendar-modal__date">
                {checkedDate.getDate()} {getMonth(checkedDate.getMonth())}
              </div>}
            
          </div>
        </div>
        <button className="btn calendar-modal__button" 
             onClick={props.DeactivateModal} 
                disabled={!Boolean(checkedDate)}>Подтвердить</button>
      </div>
    </div>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    DeactivateModal: () => dispatch(DeactivateModal())
  })
)(CalendarModal)


export function getMonth(monthId) {
  return MONTHS[monthId].substring(0, 3).toLowerCase()
}