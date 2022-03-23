import React, { useEffect, useState } from 'react'
import { connect } from 'react-redux'
import {
  SwapMonthToNext,
  SwapMonthToPrev,
} from '~@/WorkRooms/FullCalendar/Calendar/redux/actions/calendar'
import { MONTHS } from '~@/WorkRooms/FullCalendar/Calendar/utils/calendar'
import {getEventsForMonth} from "../ajax/dateDetail";
import {UpdateEvents} from "../../DateDetail/redux/actions/dateDetail";


function MonthNav(props) {
  let currentMonth = props.store.calendar.currentDate.getMonth()
  let currentYear = props.store.calendar.currentDate.getFullYear()
  
  function updateEvents(year, month) {
    if (!props.store.header.modalActive) {
      getEventsForMonth(year, month + 1)
        .then(response => response.json())
        .then(data => props.UpdateEvents(data.data))
        .catch(error => console.log('Ошибка при получении данных календаря (MonthNav: 21):', error))
    }
  }
  
  useEffect(() => {
    updateEvents(currentYear, currentMonth)
  }, [props.store.header.modalActive, props.store.calendar.currentDate])

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
    SwapMonthToNext: () => dispatch(SwapMonthToNext()),
    SwapMonthToPrev: () => dispatch(SwapMonthToPrev()),
    UpdateEvents: (events) => dispatch(UpdateEvents(events))
  })
)(MonthNav)

function getMonth(monthId) {
  return MONTHS[monthId]
}
