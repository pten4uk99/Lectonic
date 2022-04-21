import React, { useEffect, useRef, useState } from 'react'
import { connect } from 'react-redux'

import Respondents from "./Respondents";
import PhotoName from "../../../../Utils/jsx/PhotoName";
import {getLecturePhoto} from "../../../../../ProjectConstants";


function Event(props) {
  let [className, setClass] = useState('left-block')
  let eventInfo = useRef()
  let [dynamicCircleHeight, setCircleHeight] = useState(24)
  let [eventDetail, setEventDetail] = useState(false)
  let [eventDetailHeight, setEventHeight] = useState('0px')

  useEffect(() => {
    if (!props.status) setClass('left-block grey')
    else setClass('left-block blue')
  }, [props.status])
  
  useEffect(() => {
    setEventDetail(false)
  }, [props.store.calendar.checkedDate])

  useEffect(() => {
    if (!eventDetail) {
      setEventHeight('42px')
      setCircleHeight(40)
    } else {
      setEventHeight(`${eventInfo.current.scrollHeight}px`)
      setCircleHeight(eventInfo.current.scrollHeight - 13.4)
    }
  }, [eventDetail])

  return (
    <li className='date-detail__event'>
      <div className={className}>
        <div className='circle'/>
        <div className='dynamic-circle' style={{ height: dynamicCircleHeight }}/>
      </div>
      
      <div className="date-detail__event-photo-block">
        <div className="lecturer-photo">
          <PhotoName firstName={props.creator[0]} 
                     lastName={props.creator[1]} 
                     size={32}/>
        </div>
        <div className="event-photo">
          <img src={getLecturePhoto(props.photo)} alt="обложка"/>
        </div>
      </div>
      
      <div className='event-info' 
           ref={eventInfo} 
           style={{ height: eventDetailHeight }}>
        <div className='header' onClick={() => setEventDetail(!eventDetail)}>
          {props.header}
        </div>
        <div className='theme'>
          Тема: <span>{props.name}</span>
        </div>
        {props.lecturer &&
          <div className='lecturer'>
            Лектор: <span>{props.lecturer[0]} {props.lecturer[1]} {props.lecturer[2]}</span>
          </div>}
        {props.customer && 
          <div className='lecturer'>
            Заказчик: <span>{props.customer[0]} {props.customer[1]} {props.customer[2]}</span>
          </div>}
        {props.address && 
          <div className='address'>
            Место: <span>{props.address}</span>
          </div>}
        <Respondents data={props.respondents}/>
      </div>
      
      <div className='time-range'>
        <span className='start'>{props.timeStart}</span>
        <span className='end'>{props.timeEnd}</span>
      </div>
    </li>
  )
}

export default connect(
  state => ({ store: state }),
  dispatch => ({})
)(Event)
