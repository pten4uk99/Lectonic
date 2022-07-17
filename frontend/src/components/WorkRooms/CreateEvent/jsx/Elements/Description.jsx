import React from 'react'
import {connect} from 'react-redux'


function Description(props) {
  let lectureData = props.lectureData
  
  return (
    <>
      <div className='desc-l label'>Описание:</div>
      <div className='desc flex'>
            <textarea name='description'
                      className='text-area'
                      rows='5'
                      defaultValue={lectureData?.description}
                      placeholder='Опишите лекцию'/>
      </div>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(Description)
