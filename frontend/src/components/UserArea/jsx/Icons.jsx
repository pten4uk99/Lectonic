import React, { useState } from 'react'
// import '~/styles/Icons.styl'

export default function Icons(props) {
  
  return (
    <div className={`icon-wrapper ${props.className}`} onClick={props.onClick}>
      <img className='icon-normal' src={props.srcNormal} alt={props.alt} />
      <img className='icon-hovered' src={props.srcHovered} alt={props.alt}/>
    </div>
  )
}
