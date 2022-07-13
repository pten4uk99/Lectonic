import React, {useEffect, useState} from 'react'
import {connect} from "react-redux";

import Calendar from "~@/WorkRooms/FullCalendar/Calendar/jsx/Calendar";
import {MONTHS} from "~@/WorkRooms/FullCalendar/Calendar/utils/calendar";
import {DeactivateModal} from "../../../Layout/redux/actions/header";
import DropDown from "../../../Utils/jsx/DropDown";
import {SwapChosenDuration, SwapModalChooseDates} from "../../FullCalendar/Calendar/redux/actions/calendar";
import {checkEqualDates} from "../../FullCalendar/Calendar/utils/date";
import {SetDropDownTimeStart} from "../../../Utils/redux/actions/dropdown";


function CalendarModal(props) {
  let chooseDates = props.store.calendar.modalChooseDates
  let duration = props.store.calendar.chosenDuration

  let [allTimeEqual, setAllTimeEqual] = useState(false)

  function handleChosenStartValue(date, value) {
    let [hours, minutes] = value.split(':')
    let newDates = chooseDates.map((elem) => {
      let newDate = new Date(
        elem.getFullYear(), elem.getMonth(), elem.getDate(),
        Number(hours), Number(minutes)
      )
      if (checkEqualDates(date, elem) || allTimeEqual) return newDate
      return elem
    })
    props.SwapModalChooseDates(newDates)
  }

  useEffect(() => {
    if (allTimeEqual) {
      if (chooseDates.length > 0) {
        for (let elem of chooseDates) {
          handleChosenStartValue(
            elem, [chooseDates[0].getHours(), chooseDates[0].getMinutes()].join(':')
          )
        }
      }
    }
  }, [allTimeEqual])

  useEffect(() => {
    if (allTimeEqual) {
      for (let elem of chooseDates) {
        handleChosenStartValue(
          elem, [chooseDates[0].getHours(), chooseDates[0].getMinutes()].join(':')
        )
      }
    }
  }, [chooseDates.length])

  function handleDisabledButton() {
    return chooseDates.length === 0
  }

  function handleConfirm() {
    props.DeactivateModal()
  }

  return (
    <div className="calendar-modal__wrapper">
      <Calendar/>

      <div className="calendar-modal__right-block">
        <p className="calendar-modal__header">Выбор дат</p>
        <p className="calendar-modal__tooltip">
          Укажите длительность лекции, а затем <br/>
          выберите одну или несколько дат в календаре <br/> 
          и укажите время начала лекции (лекций).
        </p>
        <div className="calendar-modal__duration">
          <span>Длительность: </span>
          <DropDown request={getDurationArr()}
                    onSelect={(value) => {
                      props.SwapChosenDuration(parseDuration(value));
                      props.SwapModalChooseDates([])
                    }}
                    defaultValue='01:00'/>
        </div>
        {chooseDates.length > 0 &&
          <div className="calendar-modal__dates-block">
            <div className="title">
              <span className="mr-5">Дата:</span> <span>Время начала:</span>
            </div>
            <div className="calendar-modal__dates-list">
              {chooseDates.map((elem, index) => (
                <div className="calendar-modal__date-wrapper" key={index}>
                  <div className="calendar-modal__date active">
                    {elem.getDate()} {getMonth(elem.getMonth())}
                  </div>
                  <div className="time-dropdown">
                    <DropDown request={getTimeArr(elem, duration)}
                              onSelect={(value) => handleChosenStartValue(elem, value)}
                              defaultValue={allTimeEqual ?
                                [chooseDates[0].getHours().toString().padStart(2, '0'),
                                  chooseDates[0].getMinutes().toString().padStart(2, '0')].join(':') :
                                [elem.getHours().toString().padStart(2, '0'),
                                  elem.getMinutes().toString().padStart(2, '0')].join(':')}
                              zIndex={chooseDates.length - index}/>
                  </div>
                </div>))}
            </div>
          </div>}
        {chooseDates.length > 0 &&
          <>
            {/*<div className="calendar-modal__time">*/}
            {/*  <span>Время начала:</span>*/}
            {/*  <div className="time-dropdown">*/}
            {/*    <DropDown request={getTimeArr(chosenDate, duration)} */}
            {/*              onSelect={(value) => handleChosenStartValue(value)} */}
            {/*              defaultValue='00:00' */}
            {/*              timeStart={true}/>*/}
            {/*  </div>*/}
            {/*</div>*/}
            <div className="auth__form__checkbox-wrapper">
              <input className="auth__form__checkbox-switch"
                     id="checkbox"
                     type="checkbox"
                     checked={allTimeEqual}
                     onChange={() => setAllTimeEqual(!allTimeEqual)}/>
              <label htmlFor="checkbox">
                Время начала лекции одинаковое для всех дат
              </label>
            </div>
          </>
        }

        <button className="btn calendar-modal__button"
                type="button"
                onClick={handleConfirm}
                disabled={handleDisabledButton()}>
          Выбрать
        </button>
      </div>
    </div>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    DeactivateModal: () => dispatch(DeactivateModal()),
    SetDropDownTimeStart: (time) => dispatch(SetDropDownTimeStart(time)),
    SwapChosenDuration: (duration) => dispatch(SwapChosenDuration(duration)),
    SwapModalChooseDates: (dates) => dispatch(SwapModalChooseDates(dates)),
  })
)(CalendarModal)


export function getMonth(monthId) {
  return MONTHS[monthId].substring(0, 3).toLowerCase()
}

function getTimeArr(date, duration) {
  let start = 0
  let now = new Date()
  if (checkEqualDates(date, now)) start = now.getHours() + 2

  let arr = []
  for (let i = start; i < 24; i++) {
    if (i * 60 + duration >= 24 * 60) break
    let hour = String(i)
    if (hour.length < 2) hour = '0' + hour
    arr.push(`${hour}:00`, `${hour}:30`)
  }
  return arr
}

function getDurationArr() {
  let arr = []
  for (let i = 0; i < 6; i++) {
    let hour = String(i)
    if (hour.length < 2) hour = '0' + hour
    if (i === 0) {
      arr.push(`${hour}:30`)
      continue
    }
    arr.push(`${hour}:00`, `${hour}:30`)
  }
  return arr
}

function parseDuration(time) {
  let [hourStr, minuteStr] = time.split(':')
  return Number(hourStr) * 60 + Number(minuteStr)
}