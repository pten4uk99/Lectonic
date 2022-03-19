import React, {useState} from 'react'
import {connect} from "react-redux";

import addLinkIcon from '~/assets/img/addLink-icon.svg'
import addHoveredIcon from '~/assets/img/add-icon-hover.svg'


function LecturerLink(props) {
  let [numberLinks, setNumberLinks] = useState(props.links.length || 1)
  
  function getLinksArr() {
    let arr = []
    for (let i = 1; i <= numberLinks; i++) arr.push(i)
    return arr
  }
  
  function handleBlur(e) {
    props.blur(e.target.value, e.target.dataset.id)
  }
  
  return (
    <div className="lecturer-link__block">
      <p className="step-block__left-part">{props.label}</p>
      <div className="lecturer-link__input-list">
        {getLinksArr().map((elem, index) => (
          <div key={elem} className="lecturer-link__input">
            <input className='input__add-link' 
                   placeholder="https://" 
                   type="text"
                   data-id={index}
                   defaultValue={props.links[index]} 
                   onBlur={(e) => handleBlur(e)}/>
            <img src={addLinkIcon} 
                 alt="добавить ссылку" 
                 onClick={() => setNumberLinks(numberLinks + 1)}/>
          </div>))}
      </div>
    </div>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(LecturerLink)