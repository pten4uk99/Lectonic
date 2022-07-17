import React from 'react'
import {connect} from 'react-redux'


function DataBlock(props) {
  let className = `data ${props.classNameModifier}`
  let data = props.data
  let text = props?.text
  return (
    <div className={className}>
      <div className="header">{props.header}</div>
      <div className="content">{props.children || text}</div>
    </div>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(DataBlock)

