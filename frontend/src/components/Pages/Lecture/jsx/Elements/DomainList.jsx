import React from 'react'
import {connect} from 'react-redux'


function DomainList(props) {
  let lectureData = props.lectureData
  return (
    <div className="block__domains">
      {lectureData?.domain && lectureData.domain.map((elem, index) => {
        return <div className="domain" key={index}>{elem}</div>
      })}
    </div>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(DomainList)

