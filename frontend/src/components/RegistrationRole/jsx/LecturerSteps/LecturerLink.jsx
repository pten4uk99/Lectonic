import React, {useEffect, useState} from 'react'
import {connect} from "react-redux";

import addLinkIcon from '~/assets/img/addLink-icon.svg'
import addHoveredIcon from '~/assets/img/add-icon-hover.svg'


function LecturerLink(props) {
  let [value, setValue] = useState('')
  let perf_links = props.store.addRole.lecturer.performances_links
  let pub_links = props.store.addRole.lecturer.publication_links
  let [correctInput, setCorrectInput] = useState(true)
  
  useEffect(() => {
    if (pub_links.length >= 5 || perf_links.length >= 5) setCorrectInput(false)
    else setCorrectInput(true)
  }, [perf_links, pub_links])
    
  function handleClick() {
    if (correctInput) {
      if (value) props.blur(value)
      setValue('')
    }
  }
  
  return (
    <div className="lecturer-link__block">
      <p className="step-block__left-part">{props.label}</p>
      <div className="lecturer-link__input-list">
        <div className="lecturer-link__input">
          <input className='input__add-link' 
                 placeholder="https://" 
                 type="text"
                 value={value}
                 onChange={(e) => setValue(e.target.value)}/>
          <img src={value && correctInput ? addHoveredIcon : addLinkIcon} 
               alt="добавить ссылку" 
               onClick={handleClick}/>
        </div>
        {props.links.map((elem, index) => (
          <div key={index} className="link-block">{elem}</div>
        ))}
      </div>
    </div>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(LecturerLink)