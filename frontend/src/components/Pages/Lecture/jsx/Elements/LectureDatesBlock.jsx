import React from 'react'
import {connect} from 'react-redux'
import LectureDates from '../LectureDates'
import DataBlock from '../DataBlock'


function LectureDatesBlock(props) {
  let data = props.data
  let lecturerText = 'Лектор готов провести лекцию:'
  let customerText = 'Заказчик готов послушать лекцию:'
  
  return (
    <DataBlock header={data?.creator_is_lecturer ? lecturerText : customerText}>
      <LectureDates data={data?.dates} responseDates={data?.response_dates}/>
    </DataBlock>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(LectureDatesBlock)

