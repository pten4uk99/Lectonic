import React from 'react'
import { connect } from 'react-redux'
import Calendar from './Calendar/jsx/Calendar'
import DateDetail from './DateDetail/jsx/DateDetail'

function FullCalendar(props) {
  return (
    <div className="calendar__block">
      <div className="workroom__block-header"><span>Календарь лектора</span></div>
      <div className='calendar__wrapper'>
        <Calendar/>
        <DateDetail date={props.store.calendar.checkedDate} />
      </div>
      <div className="workroom__block-underline"/>
    </div>
  )
}

export default connect(
  state => ({ store: state }),
  dispatch => ({})
)(FullCalendar)
