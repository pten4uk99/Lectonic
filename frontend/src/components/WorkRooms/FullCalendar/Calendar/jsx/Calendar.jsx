import React, { useEffect, useState } from 'react'

import MonthNav from './MonthNav'
import DaysOfWeek from './DaysOfWeek'
import { connect } from 'react-redux'
import DatesListSwappable from './Date/DatesListSwappable'
import {SetCheckedDate, SetHoverDate} from "../redux/actions/calendar";

function Calendar(props) {
  
  useEffect(() => {
    if (!props.store.header.modalActive) {
      props.SetHoverDate(props.store.calendar.currentDate)
      props.SetCheckedDate(props.store.calendar.currentDate)
    }
  }, [props.store.header.modalActive])
  return (
    <div className='calendar__container'>
      <div className='inside__container'>
        <MonthNav />
        <DaysOfWeek />
        <DatesListSwappable />
      </div>
    </div>
  )
}

export default connect(
  state => ({ store: state }),
  dispatch => ({
    SetHoverDate: (date) => dispatch(SetHoverDate(date)),
    SetCheckedDate: (date) => dispatch(SetCheckedDate(date)),
  })
)(Calendar)
