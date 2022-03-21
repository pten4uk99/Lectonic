import React, {useState} from 'react'
import {connect} from "react-redux";

import Calendar from "../../WorkRooms/FullCalendar/Calendar/jsx/Calendar";


function CalendarModal(props) {
  return (
    <div className="calendar-modal">
      <Calendar/>
    </div>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(CalendarModal)