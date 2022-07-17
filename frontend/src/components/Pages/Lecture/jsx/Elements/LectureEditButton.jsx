import React from 'react'
import {connect} from 'react-redux'

import {useNavigate} from 'react-router-dom'
import edit from '~/assets/img/edit-purple.svg'
import {reverse} from '../../../../../ProjectConstants'


function LectureEditButton(props) {
  let navigate = useNavigate()
  let lectureId = props.lectureId
  let creatorIsLecturer = props.creatorIsLecturer
  let role = creatorIsLecturer ? 'lecturer' : 'customer'
  
  return (
    <img className='edit-lecture'
         src={edit}
         alt="назад"
         onClick={() => navigate(reverse('create_event', {role: role, edit: lectureId}))}/>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(LectureEditButton)

