import React, {useState} from 'react'


export default function StepsBar(props) {
  let style = {color: "var(--main-blue)"}
  
  function getStyleUnderline() {
    if (props.step in [0, 1]) return {marginLeft: 0}
    else if (props.step === 2) return {marginLeft: '33%'}
    else if (props.step === 3) return {marginLeft: '67%'}
  }
  
  return (
    <div className='role-steps'>
      <div className="role-steps__text">
        <h2 style={props.step in [0, 1] ? style : {}}>Шаг 1</h2>
        <h2 style={props.step === 2 ? style : {}}>Шаг 2</h2>
        <h2 style={props.step === 3 ? style : {}}>Шаг 3</h2>
      </div>
      <div className='role-steps__bar'>
        <div className='role-steps__bar-current' style={getStyleUnderline()}/>
      </div>
    </div>
  )
}