import React, {useEffect} from 'react'
import {connect} from 'react-redux'
import {SwapEquipment} from '../../redux/actions/event'


function Equipment(props) {
  let equipment = props.equipment
  let lectureData = props.lectureData
  
  useEffect(() => {
    if (lectureData?.equipment) props.SwapEquipment(true)
  }, [lectureData])

  return (
    <>
      <div className='workspace-2 label'>Оборудование:</div>
      <div className='workspace-btn flex'>
        <div className={equipment ? 'pill pill-blue' : 'pill'}
             onClick={() => props.SwapEquipment(true)}>Есть
        </div>
        <div className={equipment ? 'pill' : 'pill pill-blue'}
             onClick={() => props.SwapEquipment(false)}>Нет
        </div>
      </div>

      <div className={equipment ? 'equip-l label' : 'equip-l label disabled'}>Список оборудования:</div>
      <div className='equip flex'>
            <textarea name='equipment'
                      className={`text-area ${!equipment && 'disabled'}`}
                      rows='4'
                      defaultValue={lectureData?.equipment}
                      placeholder='Перечислите имеющееся для лекции оборудование'
                      readOnly={!equipment}/>
      </div>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SwapEquipment: (equipment) => dispatch(SwapEquipment(equipment)),
  })
)(Equipment)
