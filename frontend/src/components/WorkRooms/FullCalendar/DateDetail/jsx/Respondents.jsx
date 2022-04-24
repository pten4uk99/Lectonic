import React, { useEffect, useState } from 'react'
import { connect } from 'react-redux'

import PhotoName from "../../../../Utils/jsx/PhotoName";


function Respondents(props) {
  return (
    <div className='respondents__block'>
      {props.data.length > 0 ?
        <>
          <p className='respondents__text'>Откликнулись: </p>
          {props.data.map((elem, index) => {
            return <div className="respondent-photo" key={index}>
              <PhotoName firstName={elem.first_name} 
                         lastName={elem.last_name} 
                         size={28}/>
            </div>})}
        </> :
        <>
          <p className='respondents__text'>Ждём отклик</p>
        </>}
    </div>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
  })
)(Respondents)