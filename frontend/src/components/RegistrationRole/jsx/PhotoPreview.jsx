import React, {useState} from 'react'
import {connect} from "react-redux";


function PhotoPreview(props) {
  
  function addPhotoHandler(inputEvent, UpdatePhoto) {
    if (props.role.diploma_photos.length >= 5) return
    let file = inputEvent.target.files[0]
    let reader = new FileReader()
    reader.readAsDataURL(file);
    
    reader.onload = () => {
      UpdatePhoto(reader.result)
    }
  }
  
  return (
    <>
      <div className="photo-preview__block">
        <label className="btn-file">
          Выбрать файл
          <input type="file"
                 accept="image/jpeg, image/png"
                 onChange={e => addPhotoHandler(e, props.set)}/>
        </label>
      </div>
      <div className="block-images" style={props.style}>
        {props.image && props.list ?
          props.image.map((src, index) => <img className="diploma-image" 
                                               key={index} 
                                               src={src} 
                                               alt="Фотография"/>) : 
          props.image && 
          <img className="diploma-image" src={props.image} alt="Фотография"/>
        }
      </div>
    </>

  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(PhotoPreview)

