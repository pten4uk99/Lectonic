import React from 'react'
import {connect} from 'react-redux'
import {checkRequiredFields} from '../../services/utils'
import Loader from '../../../../Utils/jsx/Loader'


function Submit(props) {
  let responseLoaded = props.responseLoaded
  let requiredFields = props.requiredFields
  let lectureData = props.lectureData
  
  let buttonText = lectureData ? 'Сохранить' : 'Создать'
  
  return (
    <>
      <div className='submit'>
        <button className='btn big-button'
                type='submit'
                disabled={checkRequiredFields(requiredFields, props)}>
          {!responseLoaded ?
            <Loader size={20} left="50%" top="50%" tX="-50%" tY="-50%"/> : 
            buttonText}
        </button>
      </div>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(Submit)
