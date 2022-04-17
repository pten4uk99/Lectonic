import React, { useEffect, useState } from 'react'

import MonthNav from './MonthNav'
import DaysOfWeek from './DaysOfWeek'
import { connect } from 'react-redux'
import DatesListSwappable from './Date/DatesListSwappable'
import {SetCheckedDate, SetHoverDate} from "../redux/actions/calendar";
import Loader from "../../../../Utils/jsx/Loader";

function Calendar(props) {
  let [isLoaded, setIsLoaded] = useState(false)
  useEffect(() => {
    if (!props.store.header.modalActive) {
      props.SetHoverDate(props.store.calendar.currentDate)
      props.SetCheckedDate(props.store.calendar.currentDate)
    }
  }, [props.store.header.modalActive])
  return (
    <div className='calendar__container'>
      {!isLoaded && <Loader size={15} right={15} top={15} position={'absolute'}/>}
      <div className='inside__container'>
        <MonthNav isMyLectures={props.isMyLectures} setIsLoaded={setIsLoaded}/>
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
