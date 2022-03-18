import React, {useState} from 'react'
import {connect} from "react-redux";

import addLinkIcon from '~/assets/img/addLink-icon.svg'
import addHoveredIcon from '~/assets/img/add-icon-hover.svg'
import {addPhotoHandler} from "../../CreateEvent/jsx/CreateEvent";


function PhotoPreview(props) {
  return (
    <>
      <div className="photo-preview__block">
        <label className="btn-file">
          Выбрать файл
          <input type="file" 
                 accept="image/*" 
                 onChange={e => addPhotoHandler(e, props.set)}/>
      </label>
      </div>
      <div className="block-images">
        {props.image && 
          <img className="diploma-image" src={props.image} alt="Фотография"/>}
      </div>
    </>

  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(PhotoPreview)