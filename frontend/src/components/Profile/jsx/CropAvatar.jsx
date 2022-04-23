//в принципе можно сделать без этой обёртки

import React from 'react'
import ImageCropper from "../../Utils/jsx/ImageEditor/ImageCropper"

function CropAvatar(props) {

  return (
    <>
      <div className="edit-avatar">
        <ImageCropper 
            img={props.img} 
            updateFileImg={props.updateFileImg} 
        />
      </div>
    </>
   
  )
}
export default CropAvatar