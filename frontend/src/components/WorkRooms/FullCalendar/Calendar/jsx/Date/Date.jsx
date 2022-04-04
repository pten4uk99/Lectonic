import React, { useEffect, useState } from 'react'
import { connect } from 'react-redux'
import {
  SetCheckedDate,
  SetHoverDate,
  SwapMonthToNext,
  SwapMonthToPrev,
} from '~@/WorkRooms/FullCalendar/Calendar/redux/actions/calendar'
import {
  checkEqualDates,
  checkNeedSwapToNextMonth,
  checkNeedSwapToPrevMonth,
} from '~@/WorkRooms/FullCalendar/Calendar/utils/date'
import Events from './Events/Events'
import {SwapModalChooseDates} from "../../redux/actions/calendar";


function Date(props) {
  let [hover, setHover] = useState(false)
  let [active, setActive] = useState(false)
  let [events, setEvents] = useState(null)

  useEffect(() => {
    let currentEvents = props.store.dateDetail.filter(value => {
      return checkEqualDates(value.date, props.date)
    })
    if (currentEvents.length > 0) setEvents(currentEvents[0].events)
    else setEvents(null)
    
    if (!props.store.header.modalActive) {
      if (checkEqualDates(props.store.calendar.checkedDate, props.date))
        setActive(true)
      else setActive(false)      
    } else setActive(false)
  }, [props.store.dateDetail])

  useEffect(() => {
    if (!props.store.header.modalActive) {
      if (checkEqualDates(props.store.calendar.hoverDate, props.date))
        setHover(true)
      else setHover(false)
    } else setHover(false)
  }, [props.store.calendar.hoverDate])

  return (
    <div className={getClassName(props)} 
         onClick={() => clickHandler(props)} 
         onMouseEnter={() => {hoverHandler(props, true)}} 
         onMouseLeave={() => {hoverHandler(props, false)}}>
      <span>{props.date.getDate()}</span>
      
      {!props.store.header.modalActive && 
        <Events events={events} dateHover={hover} dateActive={active}/>}
    </div>
  )
}

export default connect(
  state => ({ store: state }),
  dispatch => ({
    SetCheckedDate: date => dispatch(SetCheckedDate(date)),
    SwapMonthToNext: () => dispatch(SwapMonthToNext()),
    SwapMonthToPrev: () => dispatch(SwapMonthToPrev()),
    SetHoverDate: date => dispatch(SetHoverDate(date)),
    SwapModalChooseDates: dates => dispatch(SwapModalChooseDates(dates)),
    
  })
)(Date)


function getClassName(props) {
  if (props.store.header.modalActive) {
    let choseDates = props.store.calendar.modalChooseDates
    for (let date of choseDates) {
      if (checkEqualDates(props.date, date)) return "calendar-date active"
    }
  } 
  
  let className = 'calendar-date'

  if (props.store.calendar.currentDate.getMonth() !== props.date.getMonth() || 
    props.date - props.store.calendar.today <= - 1000 * 60 * 60 * 24 ||
    props.date - props.store.calendar.today >= 1000 * 60 * 60 * 24 * 365
  ) return 'calendar-date inactive'

  if (checkEqualDates(props.date, props.store.calendar.today))
    className += ' today'
  if (checkEqualDates(props.date, props.store.calendar.hoverDate))
    className += ' active'

  return className
}

function clickHandler(props) {
  let modal = props.store.header.modalActive
  
  if (checkNeedSwapToNextMonth(
    props.date, props.store.calendar.currentDate, props.store.calendar.today)) {
    props.SwapMonthToNext()
    modal && SwapChooseDates(props)
  } else if (checkNeedSwapToPrevMonth(
    props.date, props.store.calendar.currentDate, props.store.calendar.today)) {
    props.SwapMonthToPrev()
    modal && SwapChooseDates(props)
  } else if (!(props.date - props.store.calendar.today <= - 1000 * 60 * 60 * 24) &&
    !(props.date - props.store.calendar.today >= 1000 * 60 * 60 * 24 * 365)
  ) {
    !modal && props.SetCheckedDate(props.date)
    modal && SwapChooseDates(props)
  }
}

function hoverHandler(props, enter) {
  if (props.store.calendar.currentDate.getMonth() !== props.date.getMonth()) {
    return props.SetHoverDate(props.store.calendar.checkedDate)
  }

  enter
    ? props.SetHoverDate(props.date)
    : props.SetHoverDate(props.store.calendar.checkedDate)
}


function SwapChooseDates(props) {
  let choseDates = props.store.calendar.modalChooseDates
  let newDates = []
  let contains = false
  
  for (let date of choseDates) {
    if (!checkEqualDates(props.date, date)) {
      newDates.push(date)
    } else contains = true
  }
  if (!contains) newDates.push(props.date)
  
  props.SwapModalChooseDates(newDates)
}