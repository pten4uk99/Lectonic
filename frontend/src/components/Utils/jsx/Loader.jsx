import React, {useEffect} from "react";

import loadingIcon from '~/assets/img/loading-icon.svg'


function Loader(props) {
  let className = "loader__icon";
  if (props.main) className = "loader__icon main-loader"
  
  let position = props?.position
  let size = props?.size || 96
  let top = props.top
  let left = props.left
  let right = props.right
  let tX = props?.tX
  let tY = props?.tY
  
  return (
    <div className={className} style={{
      position: position,
      width: size,
      height: size,
      top: top,
      left: left,
      right: right,
      transform: `translateX(${tX}) translateY(${tY})`,
    }}>
      <img src={loadingIcon} alt="загрузка"/>
    </div>
  )
}

export default Loader