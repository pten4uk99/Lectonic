import React, {useEffect, useState} from 'react'
import {connect} from "react-redux";
import {getMonth} from "../../CreateEvent/jsx/CalendarModal";
import {DateTime} from "luxon";
import {UpdateLectureDetailChosenDates} from "../redux/actions/lectureDetail";


function LectureDates(props) {
  let [data, setData] = useState([])
  let chosenDates = props.store.lectureDetail.chosenDates
  
  useEffect(() => {
    if (props.data) setData(getDates(props.data))
  }, [props.data])
  
  useEffect(() => {
    if (data.length === 1) {
      props.UpdateLectureDetailChosenDates([data[0].start])
    }
  }, [data])
  
  
  
  function handleClickDate(dateStart) {
    if (data.length === 1) return
    let newDates;
    if (checkDateInArr(dateStart, chosenDates)) newDates = chosenDates.filter(elem => elem !== dateStart)
    else newDates = [...chosenDates, dateStart]
    props.UpdateLectureDetailChosenDates(newDates)
  }
  
  return (
    <div className="lecture-dates__wrapper">
      <div className="dates__block">
        {data.map((elem, index) => {
          return <div className="date__wrapper" key={index} onClick={() => handleClickDate(elem.start)}>
            <div className={checkDateInArr(elem.start, chosenDates) ? 
              "date__block active" : "date__block"}>
              <span className="date">{elem.start.day} {getMonth(elem.start.month - 1)}</span>
              <span className="time">{elem.start.toFormat('hh:mm')}-{elem.end.toFormat('hh:mm')}</span>
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
    dates.push({
      start: DateTime.fromISO(date.start), 
      end: DateTime.fromISO(date.end)
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
    if (date === checkDate) return true
  }
  return false
}