import React, { useEffect, useState } from 'react'
import { connect } from 'react-redux'

import PhotoName from "../../../../Utils/jsx/PhotoName";
import {useNavigate} from "react-router-dom";
import {reverse} from "../../../../../ProjectConstants";


function Respondents(props) {
  let navigate = useNavigate()
  
  function handleClickRespondent(respondentId) {
    let creatorIsLecturer = props.creator_is_lecturer
    let to
    if (creatorIsLecturer) to = 'customer'
    else to = 'lecturer'
    
    navigate(reverse('role_page', {[to]: respondentId}))
  }
  return (
    <div className='respondents__block'>
      {props.data.length > 0 ?
        <>
          <p className='respondents__text'>Откликнулись: </p>
          {props.data.map((elem, index) => {
            return <div className="respondent-photo" 
                        key={index} 
                        onClick={() => handleClickRespondent(elem.id)}>
              <PhotoName firstName={elem.first_name} 
                         lastName={elem.last_name} 
                         size={28} 
                         colorNumber={elem.bgc_number}/>
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