import React, {useEffect} from 'react'
import {connect} from 'react-redux'
import {onlyNumber} from '../../services/utils'
import {SwapPayment} from '../../redux/actions/event'


function Price(props) {
  let payment = props.payment
  let lectureData = props.lectureData
  
  useEffect(() => {
    if (lectureData?.cost) props.SwapPayment(true)
  }, [lectureData])
  
  return (
    <>
      <div className='fee-l label'>Цена лекции:</div>
          <div className='fee'>
            <div className='flex'>
              <div className={payment ? 'pill pill-blue' : 'pill'}
                   onClick={() => props.SwapPayment(true)}>Платно
              </div>
              <div className={payment ? 'pill' : 'pill pill-blue'}
                   onClick={() => props.SwapPayment(false)}>Бесплатно
              </div>
            </div>
            {payment ? <><input name='cost'
                                className='text-input'
                                type='text'
                                placeholder='Укажите цену'
                                defaultValue={lectureData?.cost}
                                onChange={(e) => onlyNumber(e, 7)}/> <span>руб.</span></> :
              <></>}
          </div>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SwapPayment: (payment) => dispatch(SwapPayment(payment)),
  })
)(Price)
