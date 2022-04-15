import React, {useEffect, useState} from 'react'
import {connect} from "react-redux";

import {getMonth} from "../../../WorkRooms/CreateEvent/jsx/CalendarModal";
import {DateTime} from "luxon";
import {UpdateLectureDetailChosenDates} from "../redux/actions/lectureDetail";
import {checkEqualDates} from "../../../WorkRooms/FullCalendar/Calendar/utils/date";


function LectureDates(props) {
  let [data, setData] = useState([])
  let [responseDates, setResponseDates] = useState([])
  let [rejectedDates, setRejectedDates] = useState([])
  let [canChoseDate, setCanChoseDate] = useState(false)
  
  let chosenDates = props.store.lectureDetail.chosenDates
  let today = props.store.calendar.today
  
  useEffect(() => {
    if (props.data) setData(getDates(props.data))
    if (props.responseDates) setResponseDates(props.responseDates)
  }, [props.data, props.responseDates])
  
  useEffect(() => {
    if (data.length === 1) {
      props.UpdateLectureDetailChosenDates([data[0].startDate])
    }
    if (responseDates.length > 0) {
      let dates = []
      let rejected = []
      for (let elem of responseDates) {
        let date = new Date(elem.date)
        if (elem.rejected) rejected.push(date)
        else {
          dates.push(date)
          setCanChoseDate(true)
        }
      }
      setRejectedDates(rejected)
      props.UpdateLectureDetailChosenDates(dates)
    }
  }, [data, responseDates])
  
  function handleClickDate(dateStart) {
    if (data.length === 1 || canChoseDate) return
    let newDates;
    if (checkDateInArr(dateStart, chosenDates) && !checkDateInArr(dateStart, rejectedDates)) {
      newDates = chosenDates.filter(elem => elem !== dateStart)
    }
    else if (dateStart < today || checkDateInArr(dateStart, rejectedDates)) return
    else newDates = [...chosenDates, dateStart]
    props.UpdateLectureDetailChosenDates(newDates)
  }
  
  return (
    <div className="lecture-dates__wrapper">
      <div className="dates__block">
        {data.map((elem, index) => {
          return <div className="date__wrapper" key={index} onClick={() => handleClickDate(elem.startDate)}>
            <div className={elem.startDate < today || checkDateInArr(elem.startDate, rejectedDates) ? 
                "date__block inactive" : checkDateInArr(elem.startDate, chosenDates) ? 
              "date__block active" : "date__block"}>
              <span className="date">
                {elem.startDate.getDate()} {getMonth(elem.startDate.getUTCMonth())}</span>
              <span className="time">
                {elem.startDate.getUTCHours().toString().padStart(2, '0')}:
                {elem.startDate.getUTCMinutes().toString().padStart(2, '0')}-
                {elem.endDate.getUTCHours().toString().padStart(2, '0')}:
                {elem.endDate.getUTCMinutes().toString().padStart(2, '0')}</span>
            </div>
          </div>
        })}

      </div>
      <div className="duration__block">
        <div className="text">Длительность лекции</div>
        <div className="duration">{data.length > 0 && getDuration(data[0].start, data[0].end)}</div>
      </div>
    </div>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    UpdateLectureDetailChosenDates: (dates) => dispatch(UpdateLectureDetailChosenDates(dates))
  })
)(LectureDates)


function getDates(str_dates) {
  let dates = []
  
  for (let date of str_dates) {
    let start = DateTime.fromISO(date.start, {zone: 'utc'})
    let end = DateTime.fromISO(date.end, {zone: 'utc'})
    dates.push({
      start: start,
      end: end,
      startDate: new Date(date.start),
      endDate: new Date(date.end),
    })
  }
  
  return dates
}

function getDuration(start, end) {
  let diff = end.diff(start, ['hours', 'minutes'])
  return diff.toFormat('hh:mm')
}

function checkDateInArr(checkDate, arr) {
  for (let date of arr) {
    if (checkEqualDates(checkDate, date)) return true
  }
  return false
}
