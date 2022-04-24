import React, {useEffect, useState} from 'react'
import CropAvatar from "./CropAvatar";
import Modal from "../../Layout/jsx/Modal";
import {connect} from "react-redux";
import {DeactivateModal} from "../../Layout/redux/actions/header";


function ChooseAvatar(props) {
  //выбранный файл для редактирования
  const [chosenFile, setChosenFile] = useState(null)
  //уже обрезанное фото, значение придёт из ImageCropper 
  const [finalCroppedImg, setFinalCroppedImg] = useState(null)
  
  const onFileChange = async (e) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0]
      let imageDataUrl = await readFile(file)
      setChosenFile(imageDataUrl);
    }
  }

  function readFile(file) {
    return new Promise((resolve) => {
      const reader = new FileReader()
      reader.addEventListener('load', () => resolve(reader.result), false)
      reader.readAsDataURL(file)
    })
  }

  function updateFileImg(imgValue, clearState) {
    setChosenFile(clearState); //меняем стейт на null, чтоб исчез редактор фото
    setFinalCroppedImg(imgValue);
  }
  
  function handleConfirm() {
    props.onConfirm(finalCroppedImg)
    props.DeactivateModal()
  }
  
  //блоки убираются при отображении редактора, чтоб было чище
  //вроде и без этого работает, надо проверить на большом экране
useEffect(() => {
      if (chosenFile) {
        document.body.style.overflowY = "";
        document.querySelector(".userInfo").style.display = "none";
        document.querySelector(".navigate-back__block").style.display = "none";
      } else if (chosenFile === null) {
        document.querySelector(".userInfo").style.display = "";
        document.querySelector(".navigate-back__block").style.display = "";
      }
  }, [chosenFile])

  return (
    <>
      {chosenFile ? (
        <CropAvatar img={chosenFile} updateFileImg={updateFileImg}/>
      ) : (
        <Modal styleBody={{ width: '616px' }}>
          <div className="choose-avatar">
            <p className="choose-avatar__text">Загрузка фотографии</p>
            <p className="choose-avatar__sub-text">Вы можете загрузить свою фотографию в формате JPG или PNG</p>
            <form encType='multipart/form-data'>
              <label htmlFor='choose-avatar__file'>
                <div className='btn-outline choose-avatar__btn'>Выбрать файл</div>
              </label>
              <input type='file' 
                     id='choose-avatar__file' 
                     accept='image/jpeg, image/png' 
                     onChange={onFileChange}/>
            </form>
            <div className="blue-circle-avatar" style={{display: finalCroppedImg ? "" : "none"}}>
              <img className="chosen-avatar" src={finalCroppedImg} alt="аватар"/>
            </div>
            <button className="btn"
                    disabled={!finalCroppedImg}
                    onClick={handleConfirm}>
              Сохранить изменения
            </button>
          </div>
        </Modal>
      )}
    </>

  )
}

export default connect(
  state => ({}), 
  dispatch => ({
    DeactivateModal: () => dispatch(DeactivateModal())
  })
)(ChooseAvatar)