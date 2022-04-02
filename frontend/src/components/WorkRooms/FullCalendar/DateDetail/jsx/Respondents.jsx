import React, { useEffect, useState } from 'react'
import { connect } from 'react-redux'

import lecturerPhoto from '~/assets/img/TEST_PHOTO_LECTURER.svg'


function Respondents(props) {
  return (
    <div className='respondents__block'>
      {props.data.length > 0 ?
        <>
          <p className='respondents__text'>Откликнулись: </p>
          {props.data.map(() => {
            return <div className="respondent-photo">
              <img src={lecturerPhoto} alt="инициалы откликнувшегося"/>
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