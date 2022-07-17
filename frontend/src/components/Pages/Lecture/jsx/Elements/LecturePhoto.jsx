import React from 'react'
import {connect} from 'react-redux'
import {getLecturePhoto} from '../../../../../ProjectConstants'


function LecturePhotoBlock(props) {
  let data = props.data
  return (
    <>
      <div className="lecture-photo"><img src={getLecturePhoto(data?.svg)} alt=""/></div>
      <div className="subheader">
        <div className="type blue">{data?.creator_is_lecturer ? 'Лекция' : 'Запрос на лекцию'}</div>
        <div className="type">{data?.lecture_type}</div>
      </div>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(LecturePhotoBlock)

