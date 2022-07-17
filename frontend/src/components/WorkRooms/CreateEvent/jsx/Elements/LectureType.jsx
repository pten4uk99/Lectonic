import React, {useEffect} from 'react'
import {connect} from 'react-redux'
import {SwapEventType} from '../../redux/actions/event'
import {EVENT_TYPES, EVENT_TYPES_RUS} from '../../services/constants'


function LectureType(props) {
  let eventType = props.eventType
  let lectureData = props.lectureData
  
  useEffect(() => {
    if (lectureData) props.SwapEventType(EVENT_TYPES_RUS[lectureData.lecture_type])
  }, [lectureData])
  
  return (
    <>
      <div className='type-l label'>Тип лекции:</div>
      <div className='type flex'>
        <div className={eventType !== 'online' ? 'pill' : 'pill pill-blue'}
             onClick={() => props.SwapEventType('online')}>{EVENT_TYPES.online}
        </div>
        <div className={eventType !== 'offline' ? 'pill' : 'pill pill-blue'}
             onClick={() => props.SwapEventType('offline')}>{EVENT_TYPES.offline}
        </div>
        <div className={eventType !== 'hybrid' ? 'pill' : 'pill pill-blue'}
             onClick={() => props.SwapEventType('hybrid')}>{EVENT_TYPES.hybrid}
        </div>
      </div>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SwapEventType: (type) => dispatch(SwapEventType(type)),
  })
)(LectureType)
