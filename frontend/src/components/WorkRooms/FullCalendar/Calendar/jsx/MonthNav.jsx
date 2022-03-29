import React, { useEffect, useState } from 'react'
import { connect } from 'react-redux'
import {
  SwapMonthToNext,
  SwapMonthToPrev,
} from '~@/WorkRooms/FullCalendar/Calendar/redux/actions/calendar'
import { MONTHS } from '~@/WorkRooms/FullCalendar/Calendar/utils/calendar'
import {getEventsForCustomerMonth, getEventsForLecturerMonth} from "../ajax/dateDetail";
import {UpdateEvents} from "../../DateDetail/redux/actions/dateDetail";
import {SetErrorMessage} from "../../../../Layout/redux/actions/header";


function MonthNav(props) {
  let currentMonth = props.store.calendar.currentDate.getMonth()
  let currentYear = props.store.calendar.currentDate.getFullYear()
  
  function updateEvents(year, month) {
    if (!props.store.header.modalActive) {
      if (props.store.profile.is_lecturer && props.store.permissions.is_lecturer) {
        getEventsForLecturerMonth(year, month + 1)
          .then(response => response.json())
          .then(data => props.UpdateEvents(data.data))
          .catch(error => props.SetErrorMessage('lecturer_calendar'))
      } else if (props.store.profile.is_customer && props.store.permissions.is_customer) {
        getEventsForCustomerMonth(year, month + 1)
          .then(response => response.json())
          .then(data => props.UpdateEvents(data.data))
          .catch(error => props.SetErrorMessage('customer_calendar'))
      }
    }
  }
  
  useEffect(() => {
    updateEvents(currentYear, currentMonth)
  }, [props.store.header.modalActive, props.store.calendar.currentDate, props.store.profile])

  return (
    <nav className='month-nav'>
      <div onClick={props.SwapMonthToPrev}>
        <button className='left' />
      </div>
      <span>
        {getMonth(currentMonth)} {currentYear}
      </span>
      <div onClick={props.SwapMonthToNext}>
        <button className='right' />
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
