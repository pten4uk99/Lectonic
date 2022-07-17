import React from 'react'
import {connect} from 'react-redux'
import Loader from '../../../../Utils/jsx/Loader'
import {onResponseButtonClick} from '../../services/server'
import {RemoveNotification} from '../../../../Layout/redux/actions/notifications'
import {UpdateLectureDetailChosenDates} from '../../redux/actions/lectureDetail'
import {useNavigate} from 'react-router-dom'


function LectureResponseButton(props) {
  let navigate = useNavigate()
  let isCreator = props.isCreator
  let confirmedRespondent = props.confirmedRespondent
  let lectureId = props.lectureId
  let responseLoaded = props.responseLoaded
  let setResponseLoaded = props.setResponseLoaded
  let lectureData = props.lectureData
  
  function checkDisabledButton() {
    if (props.store.lectureDetail.chosenDates.length < 1 || confirmedRespondent) return true
  }
  
  function handleResponse(e) {
    onResponseButtonClick(e, lectureId, responseLoaded, 
      setResponseLoaded, props.store.lectureDetail.chosenDates, 
      lectureData, props.UpdateLectureDetailChosenDates, 
      props.RemoveNotification, navigate)
  }
  
  return !isCreator && (
    <button className="btn btn-response"
            disabled={checkDisabledButton()}
            onClick={(e) => handleResponse(e)}>
      {!responseLoaded ?
        <Loader size={20}
                left="50%"
                top="50%"
                tX="-50%" tY="-50%"/> :
        confirmedRespondent ? 'Лекция подтверждена' :
          lectureData?.can_response ?
            'Откликнуться' : 'Отменить отклик'}
    </button>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    RemoveNotification: (data) => dispatch(RemoveNotification(data)),
    UpdateLectureDetailChosenDates: (dates) => dispatch(UpdateLectureDetailChosenDates(dates)),
  })
)(LectureResponseButton)

