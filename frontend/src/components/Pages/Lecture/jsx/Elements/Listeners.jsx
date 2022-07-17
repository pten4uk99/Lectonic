import React from 'react'
import {connect} from 'react-redux'
import DataBlock from '../DataBlock'


function Listeners(props) {
  let data = props.data
  return !data?.creator_is_lecturer ? (
    <DataBlock header='Количество слушателей:' text={data?.listeners}/>
  ) : <></>
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(Listeners)

