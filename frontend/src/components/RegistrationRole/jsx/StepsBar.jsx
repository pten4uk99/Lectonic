import React, {useState} from 'react'
// import '~/styles/RegistrationRole.styl'

export default function StepsBar(props) {
  
  return (
    <div className='role-steps'>
      <div className="role-steps__text">
        <h2 style={props.step1}>Шаг 1</h2>
        <h2 style={props.step2}>Шаг 2</h2>
        <h2 style={props.step3}>Шаг 3</h2>
      </div>
      <div className='role-steps__bar'>
        <div
          className='role-steps__bar-current'
          style={props.style}
        ></div>
      </div>
    </div>
  )
}