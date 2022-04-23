import React, {useState, useCallback, useEffect} from 'react'
import Cropper from 'react-easy-crop'
import getCroppedImg from "./defaultForCropper"
import '../../styles/ImageCropper.styl'
import rotateLeft from '~/assets/img/rotate-icon-left.svg'
import rotateRight from '~/assets/img/rotate-icon-right.svg'
import closeIcon from '~/assets/img/close-cropper-icon.svg'


function ImageCropper(props) {
  let currentImage = props.img;
  const [crop, setCrop] = useState({ x: 0, y: 0 })
  const [zoom, setZoom] = useState(1) //number between minZoom(1) and maxZoom(3)
  const [rotation, setRotation] = useState(0) //number in degree 
  const [croppedAreaPixels, setCroppedAreaPixels] = useState(null)
  const [croppedImage, setCroppedImage] = useState(null)
  //отступ для дива с кнопками управления редактором (.controls)
  const [controlsMargin, setControlsMargin] = useState(null)


  const onZoomChange = (zoom) => {
    setZoom(zoom)
  }

  const rotateToLeft = () => {
    setRotation(rotation - 90)
  }

  const rotateToRight = () => {
    setRotation(rotation + 90)
  }

  const onCropComplete = useCallback((croppedArea, croppedAreaPixels) => {
    setCroppedAreaPixels(croppedAreaPixels)
  }, [])


  const saveCroppedImage = useCallback(async () => {
    try {
      const croppedImage = await getCroppedImg( currentImage, croppedAreaPixels, rotation)
      console.log('croppedImage: ', { croppedImage })
      setCroppedImage(croppedImage);
      props.updateFileImg(croppedImage, null); //передаём значения в ChooseAvatar
    } catch (e) {
      console.error(e)
    }
  }, [croppedAreaPixels, rotation])
  
  //margin-top для controls зависит от высоты окна рабочей области редактора
  useEffect(() => {
    let cropAreaHeight = document.querySelector(".reactEasyCrop_Container").clientHeight
    setControlsMargin( cropAreaHeight + 20);
  })
  
  return(
    <>
      <div className="cropper-wrapper">
        <img
          className="cropper-close-icon"
          src={closeIcon}
          onClick={() => props.updateFileImg(null, null)}/>
        <Cropper
          image={currentImage}
          crop={crop}
          zoom={zoom}
          aspect={1}
          rotation={rotation}
          cropShape="round"
          showGrid={false}
          onCropChange={setCrop}
          onZoomChange={setZoom}
          onRotationChange={setRotation}
          onCropComplete={onCropComplete}
          disableAutomaticStylesInjection={true}
          zoomWithScroll={false}
        />
      </div>
      <div className="controls"
           style={{marginTop: `${controlsMargin}px`}}>
        <div className="control-area rotation-area">
          <img
            src={rotateLeft}
            onClick={rotateToLeft}/>
          <img
            src={rotateRight}
            onClick={rotateToRight}/>
        </div>
        <div className="control-area">
          <input
            className="slider"
            type="range"
            value={zoom}
            min={1}
            max={3}
            step={0.1}
            aria-labelledby="Zoom"
            onChange={(e) => {onZoomChange(e.target.value)}}
          />
        </div>
        <div className="control-area">
          <button
            className="btn"
            onClick={saveCroppedImage}>Сохранить изменения</button>
        </div>
      </div>
    </>
  )
};

export default ImageCropper