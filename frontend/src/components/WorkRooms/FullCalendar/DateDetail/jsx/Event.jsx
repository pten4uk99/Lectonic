import React, { useEffect, useRef, useState } from 'react'
import { connect } from 'react-redux'

import lecturePhoto from '~/assets/img/TEST_PHOTO_LECTURE.svg'
import lecturerPhoto from '~/assets/img/TEST_PHOTO_LECTURER.svg'


function Event(props) {
  let [className, setClass] = useState('left-block')
  let eventInfo = useRef()
  let [dynamicCircleHeight, setCircleHeight] = useState(24)
  let [eventDetail, setEventDetail] = useState(false)
  let [eventDetailHeight, setEventHeight] = useState('0px')

  useEffect(() => {
    if (!props.status) setClass('left-block grey')
  }, [])

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
          <img src={lecturerPhoto} alt="инициалы создателя"/>
        </div>
        <div className="event-photo">
          <img src={lecturePhoto} alt="обложка"/>
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
        <div className='lecturer'>
          Лектор: <span>{props.lecturer}</span>
        </div>
        <div className='listener'>
          Слушатель: <span>{props.listener}</span>
        </div>
        <div className='address'>
          Место: <span>{props.address}</span>
        </div>
      </div>
      
      <div className='time-range'>
        <span className='start'>{props.timeStart}</span>
        <span className='end'>{props.timeEnd}</span>
      </div>
    </li>
  )
}

export default connect(
  state => ({ store: state.dateDetail }),
  dispatch => ({})
)(Event)
