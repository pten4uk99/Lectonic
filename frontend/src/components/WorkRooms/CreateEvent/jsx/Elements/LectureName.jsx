import React, {useEffect} from 'react'
import {connect} from 'react-redux'


function LectureName(props) {
  let requiredFields = props.requiredFields
  let setLectureName = props.setLectureName
  let errorMessages = props.errorMessages
  let lecture_name = props.lectureData?.name

  useEffect(() => {
    if (lecture_name) {
      setLectureName(lecture_name)
    }
  }, [lecture_name])

  return (
    <>
      <div className='topic-l label'>
        Тема лекции:
        <span className="required-sign step-block__required-sign">*</span>
      </div>
      <div className='topic flex'>
        <input name='name'
               type='text'
               className='text-input'
               defaultValue={lecture_name}
               autoComplete='none'
               onChange={(e) => setLectureName(e.target.value)}/>
      </div>

      {errorMessages.name && (<div className='form__input-error'
                                   style={{
                                     gridArea: 'topic',
                                     transform: 'translateY(25px)'
                                   }}>{errorMessages.name[0]}</div>)}
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(LectureName)
