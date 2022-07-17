import React, {useEffect} from 'react'
import {connect} from 'react-redux'
import {SwapPlace} from '../../redux/actions/event'


function HallAddress(props) {
  let place = props.place
  let lectureData = props.lectureData
  
  useEffect(() => {
    if (lectureData?.hall_address) props.SwapPlace(true)
    else props.SwapPlace(false)
  }, [lectureData])

  return (
    <>
      <div className='workspace-l label'>Помещение для лекции:</div>
      <div className='workspace flex'>
        <div className={place ? 'pill pill-blue' : 'pill'}
             onClick={() => props.SwapPlace(true)}>Есть
        </div>
        <div className={place ? 'pill' : 'pill pill-blue'}
             onClick={() => props.SwapPlace(false)}>Нет
        </div>
      </div>
      <div className={place ? 'address-l label' : 'address-l label disabled'}>Адрес:</div>
      <div className='address flex'>
            <textarea name='hall_address'
                      className={`text-area ${!place && 'disabled'}`}
                      placeholder='Введите адрес помещения для лекций'
                      defaultValue={lectureData?.hall_address}
                      rows='4'
                      readOnly={!place}/>
      </div>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SwapPlace: (place) => dispatch(SwapPlace(place)),
  })
)(HallAddress)
