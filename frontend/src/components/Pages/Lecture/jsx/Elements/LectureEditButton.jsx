import React from 'react'
import {connect} from 'react-redux'
import {useNavigate} from 'react-router-dom'

import edit from '~/assets/img/edit-purple.svg'
import editDisabled from '~/assets/img/edit-disabled.svg'
import {reverse} from '../../../../../ProjectConstants'
import Tooltip from "../../../../Utils/jsx/Tooltip";


function LectureEditButton(props) {
  let navigate = useNavigate()
  let lectureId = props.lectureId
  let creatorIsLecturer = props.creatorIsLecturer
  let role = creatorIsLecturer ? 'lecturer' : 'customer'

  function handleClick() {
    if (props.canEdit) {
      navigate(reverse('create_event', {role: role, edit: lectureId}))
    }
  }

  return (
    <>
      <img className='edit-lecture'
           src={props.canEdit ? edit : editDisabled}
           alt="назад"
           onClick={handleClick}/>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(LectureEditButton)

