import React, {useEffect, useState} from 'react'
import {connect} from "react-redux";

import Calendar from "~@/WorkRooms/FullCalendar/Calendar/jsx/Calendar";
import {MONTHS} from "~@/WorkRooms/FullCalendar/Calendar/utils/calendar";
import {DeactivateModal} from "../../../Layout/redux/actions/header";
import DropDown from "../../../Utils/jsx/DropDown";
import {SwapModalChooseDates} from "../../FullCalendar/Calendar/redux/actions/calendar";
import {checkEqualDates} from "../../FullCalendar/Calendar/utils/date";


function CalendarModal(props) {
  let chooseDates = props.store.calendar.modalChooseDates
  let [chosenDate, setChosenDate] = useState(null)
  
  function handleChosenStartValue(value) {
    let [hours, minutes] = value.split(':')
    let oldDates = chooseDates
    oldDates.map((elem) => {
      if (checkEqualDates(chosenDate, elem)) {
        return new Date(elem.getFullYear(), elem.getMonth(), elem.getDate(), Number(hours), Number(minutes))
      }
    })
    props.SwapModalChooseDates(oldDates)
  }
  
  function activeDate(date) {
    let className = 'calendar-modal__date'
    if (checkEqualDates(date, chosenDate)) return className + ' active'
    return className
  }
  
  return (
    <div className="calendar-modal__wrapper">
      <Calendar/>
      
      <div className="calendar-modal__right-block">
        <p className="calendar-modal__header">Выбор дат</p>
        <p className="calendar-modal__tooltip">
          Отметьте одну или несколько дат на календаре<br/>
          и укажите продолжительность лекции.
        </p>
        <div className="calendar-modal__dates-block">
          <span>Дата:</span>
          <div className="calendar-modal__dates-list">
            {chooseDates.map((elem, index) => (
              <div className={activeDate(elem)} key={index} onClick={() => setChosenDate(elem)}>
                {elem.getDate()} {getMonth(elem.getMonth())}
              </div>))}
          </div>
        </div>
        <div className="calendar-modal__time">
          <span>Время:</span>
          <div className="time-dropdown">
            <span>c <DropDown request={getTimeArr()} 
                              onSelect={(value) => handleChosenStartValue(value)}/></span>
            <span>до <DropDown request={getTimeArr()}/></span>
          </div>
        </div>
        <button className="btn calendar-modal__button" 
             onClick={props.DeactivateModal} 
                disabled={!Boolean(chooseDates.length > 0)}>Подтвердить</button>
      </div>
    </div>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    DeactivateModal: () => dispatch(DeactivateModal()),
    SwapModalChooseDates: (dates) => dispatch(SwapModalChooseDates(dates)),
  })
)(CalendarModal)


export function getMonth(monthId) {
  return MONTHS[monthId].substring(0, 3).toLowerCase()
}

function getTimeArr() {
  let arr = []
  for (let i = 0; i < 24; i++) {
    let hour = String(i)
    if (hour.length < 2) hour = '0' + hour
    arr.push(`${hour}:00`, `${hour}:30`)
  }
  return arr
}