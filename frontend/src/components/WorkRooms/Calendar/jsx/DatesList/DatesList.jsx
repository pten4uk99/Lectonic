import React from 'react'
import { connect } from 'react-redux'

import { getCalendar } from '../utils/calendar'
import Date from './Date'

function DatesList(props) {
  let year = props.store.currentDate.getFullYear()
  let month = props.store.currentDate.getMonth()
  let calendar = getCalendar(year, month)

  return (
    <section className='dates__list'>
      {calendar.map((date, index) => {
        return <Date key={index} date={date} />
      })}
      <div className='dates__underlines'>
        {getUnderlines().map(index => (
          <div key={index} className='dates__underline' />
        ))}
      </div>
    </section>
  )
}

export default connect(
  state => ({ store: state.calendar }),
  dispatch => ({})
)(DatesList)

function getUnderlines() {
  return [1, 2, 3, 4, 5]
}
