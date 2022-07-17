import React, {useEffect} from 'react'
import {connect} from 'react-redux'
import {onlyNumber} from '../../services/utils'


function Listeners(props) {
  let role = props.role
  let requiredFields = props.requiredFields
  let setRequiredFields = props.setRequiredFields
  let errorMessages = props.errorMessages
  let listeners = props.lectureData?.listeners
  
  useEffect(() => {
    if (listeners) props.setRequiredFields({...props.requiredFields, listeners: listeners})
  }, [listeners])
  
  return (
    <>
      {role === 'customer' &&
        <>
          <div className='listeners-l label'>
            Количество слушателей:
            <span className="required-sign step-block__required-sign">*</span>
          </div>
          <div className='listeners flex'>
            <input name='listeners'
                   type='text'
                   className='text-input'
                   autoComplete='nope'
                   defaultValue={listeners}
                   onChange={(e) => {
                     setRequiredFields({...requiredFields, listeners: e.target.value})
                     onlyNumber(e, 5)
                   }}/>
          </div>
        </>}
      {errorMessages.listeners && (<div className='form__input-error'
                                        style={{
                                          gridArea: 'listeners',
                                          transform: 'translateY(25px)'
                                        }}>{errorMessages.listeners[0]}</div>)}
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(Listeners)
