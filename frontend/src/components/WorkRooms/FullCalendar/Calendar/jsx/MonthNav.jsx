import React, { useEffect, useState } from 'react'
import { connect } from 'react-redux'

import {
  SwapMonthToNext,
  SwapMonthToPrev,
} from '~@/WorkRooms/FullCalendar/Calendar/redux/actions/calendar'
import { MONTHS } from '~@/WorkRooms/FullCalendar/Calendar/utils/calendar'
import {
  getEventsForCustomerMonth,
  getEventsForCustomerResponsesMonth,
  getEventsForLecturerMonth, getEventsForLecturerResponsesMonth
} from "../ajax/dateDetail";
import {UpdateEvents} from "../../DateDetail/redux/actions/dateDetail";
import {SetErrorMessage} from "../../../../Layout/redux/actions/header";
import leftArrow from '~/assets/img/left-arrow.svg'
import disabledLeftArrow from '~/assets/img/disabled-left-arrow.svg'
import rightArrow from '~/assets/img/right-arrow.svg'


function MonthNav(props) {
  let currentMonth = props.store.calendar.currentDate.getMonth()
  let currentYear = props.store.calendar.currentDate.getFullYear()
  
  let canNotNextSwap = (currentYear === props.store.calendar.today.getFullYear() + 1 && 
    currentMonth === props.store.calendar.today.getMonth())
  let canNotPrevSwap = (currentYear === props.store.calendar.today.getFullYear() && 
      currentMonth === props.store.calendar.today.getMonth())
  
  function updateEvents(year, month) {
    if (!props.store.header.modalActive) {
      if (props.store.profile.is_lecturer && props.store.permissions.is_lecturer) {
        if (!props.isMyLectures) {
          getEventsForLecturerResponsesMonth(year, month + 1)
            .then(response => response.json())
            .then(data => props.UpdateEvents(data.data))
            .catch(error => console.log(error))
        } else {
          getEventsForLecturerMonth(year, month + 1)
            .then(response => response.json())
            .then(data => props.UpdateEvents(data.data))
            .catch(error => console.log(error))
        }
      } else if (props.store.profile.is_customer && props.store.permissions.is_customer) {
        if (!props.isMyLectures) {
          getEventsForCustomerResponsesMonth(year, month + 1)
            .then(response => response.json())
            .then(data => props.UpdateEvents(data.data))
            .catch(error => console.log(error))
        } else {
          getEventsForCustomerMonth(year, month + 1)
            .then(response => response.json())
            .then(data => props.UpdateEvents(data.data))
            .catch(error => console.log(error))
        }
      }
    }
  }
  
  useEffect(() => {
    updateEvents(currentYear, currentMonth)
  }, [
    props.store.header.modalActive, 
    props.store.calendar.currentDate, 
    props.store.profile,
    props.isMyLectures
  ])

  return (
    <nav className='month-nav'>
      <div onClick={() => {if (!canNotPrevSwap) {props.SwapMonthToPrev()}}}>
        <img src={canNotPrevSwap ? disabledLeftArrow: leftArrow} alt=""/>
      </div>
      <span>
        {getMonth(currentMonth)} {currentYear}
      </span>
      <div onClick={() => {if (!canNotNextSwap) props.SwapMonthToNext()}}>
        <img src={rightArrow} alt=""/>
      </div>
    </nav>
  )
}

export default connect(
  state => ({ store: state }),
  dispatch => ({
    SetErrorMessage: (message) => dispatch(SetErrorMessage(message)),
    SwapMonthToNext: () => dispatch(SwapMonthToNext()),
    SwapMonthToPrev: () => dispatch(SwapMonthToPrev()),
    UpdateEvents: (events) => dispatch(UpdateEvents(events))
  })
)(MonthNav)

function getMonth(monthId) {
  return MONTHS[monthId]
}
