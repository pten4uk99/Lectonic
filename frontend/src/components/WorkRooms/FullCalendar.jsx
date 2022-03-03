import React from 'react'
import { connect } from 'react-redux'
import Calendar from './Calendar/jsx/Calendar'
import DateDetail from './DateDetail/jsx/DateDetail'

function FullCalendar(props) {
  function clickHandler(e) {
    e.preventDefault();
    
    let formData = new FormData(e.target);
    console.dir(e.target)
    const HEADERS = {
  'Content-Type': 'application/json',
}
    const options = {
    method: 'POST',
    credentials: 'include',
      body: formData
  }
  fetch(
    `http://127.0.0.1:8000/api/workrooms/calendar/lecturer/`,
    options
  )
  }
  
  return (
    <div className='calendar__wrapper'>
      <form action="" onSubmit={(e) => clickHandler(e)}>
        <input type="file" name='picture'/>
        <input type="submit"/>
      </form>
      <Calendar />
      <DateDetail date={props.store.calendar.checkedDate} />
    </div>
  )
}

export default connect(
  state => ({ store: state }),
  dispatch => ({})
)(FullCalendar)
