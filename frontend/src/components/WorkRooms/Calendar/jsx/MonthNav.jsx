import React, { useEffect, useState } from 'react'
import { connect } from 'react-redux'
import {
  SwapMonthToNext,
  SwapMonthToPrev,
} from '~@/WorkRooms/Calendar/redux/actions/calendar'
import { MONTHS } from '~@/WorkRooms/Calendar/utils/calendar'
import {getEventsForMonth} from "../ajax/dateDetail";
import {UpdateEvents} from "../../DateDetail/redux/actions/dateDetail";

function MonthNav(props) {
  let currentMonth = props.store.currentDate.getMonth()
  let currentYear = props.store.currentDate.getFullYear()
  
  function updateEvents(year, month) {
    getEventsForMonth(year, month + 1)
      .then(response => response.json())
      .then(data => props.UpdateEvents(data.data))
      .catch(error => console.log('Ошибка при получении данных календаря (MonthNav: 21):', error))
  }
  useEffect(() => {
    updateEvents(currentYear, currentMonth)
  }, [])

  return (
    <nav className='month-nav'>
      <div onClick={() => {props.SwapMonthToPrev(); updateEvents(currentYear, currentMonth - 1)}}>
        <button className='left' />
      </div>
      <span>
        {getMonth(currentMonth)} {currentYear}
      </span>
      <div onClick={() => {props.SwapMonthToNext(); updateEvents(currentYear, currentMonth + 1)}}>
        <button className='right' />
      </div>
    </nav>
  )
}

export default connect(
  state => ({ store: state.calendar }),
  dispatch => ({
    SwapMonthToNext: () => dispatch(SwapMonthToNext()),
    SwapMonthToPrev: () => dispatch(SwapMonthToPrev()),
    UpdateEvents: (events) => dispatch(UpdateEvents(events))
  })
)(MonthNav)

function getMonth(monthId) {
  return MONTHS[monthId]
}
