import React, { useEffect, useState } from 'react'
import { connect } from 'react-redux'
import {
  SwapMonthToNext,
  SwapMonthToPrev,
} from '~@/WorkRooms/Calendar/redux/actions/calendar'
import { MONTHS } from '~@/WorkRooms/Calendar/utils/calendar'
// import { getEventsForMonth } from '~@/WorkRooms/Calendar/ajax/dateDetail'

function MonthNav(props) {
  let currentMonth = props.store.currentDate.getMonth()
  let currentYear = props.store.currentDate.getFullYear()

  let [events, setEvents] = useState(null)
  /*
   * Working example start
   */
  // const [apiData, setApiData] = useState([])

  // const api = {
  //   baseurl: 'https://jsonplaceholder.typicode.com/users',
  //   apiurl: 'api/',
  // }

  // const getApiData = () => {
  //   fetch(api.baseurl)
  //     .then(response => response.json())
  //     .then(data => {
  //       setApiData(data)
  //       window.localStorage.setItem('dataSet', JSON.stringify(data))
  //     })

  //     .catch(err => {
  //       console.log(err)
  //     })
  // }

  // useEffect(() => {
  //   getApiData()
  // }, [])
  // console.log(apiData)

  /*
   * Working example end
   */

  // useEffect(() => {
  //     getEventsForMonth()
  //       .then(response => response.json())
  //       .then(data => setEvents(data))
  //       .catch(error => console.log('Ошибка при получении данных:', error))
  // }, [])
  //
  // console.log(events)
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
  state => ({ store: state.calendar }),
  dispatch => ({
    SwapMonthToNext: () => dispatch(SwapMonthToNext()),
    SwapMonthToPrev: () => dispatch(SwapMonthToPrev()),
  })
)(MonthNav)

function getMonth(monthId) {
  return MONTHS[monthId]
}
