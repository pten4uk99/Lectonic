//Осталось:
//Доделать отправку на сервер фотографии, её отображение
//Связка выбранного файла с аватаркой в хедере


import React, {useState} from "react";
import "../styles/ChangeAvatar.css";
import avatarDefault from "../img/avatar-default.svg";
import avatarFemale from "../img/avatar-fem.svg";
import avatarMale from "../img/avatar-male.svg";

export default function ChangeAvatar () {

    const [chosenFile, setChosenFile] = useState(null); //выбранный файл для отправки на сервер
    const [avatarUploaded, setAvatarUploaded] = useState(null); //загруженная картинка-аватарка

    const onChangeСhosenFile = e => {
        setChosenFile(e.target.files[0]);
        console.log("chosenFile: ", e.target.files[0]);
    }

//стейты и функции для контролирования отображения синего элипса на предвыбранном аватаре
//наверное можно уменьшить код через циклы (на потом)
    const [avatarUploadedClicked, setAvatarUploadedClicked] = useState(false);
    const [avatarMaleClicked, setAvatarMaleClicked] = useState(false);
    const [avatarFemaleClicked, setAvatarFemaleClicked] = useState(false);
    const [avatarDefaultClicked, setAvatarDefaultClicked] = useState(false);

    function selectAvatarUploaded() {
        setAvatarUploadedClicked(true);
        setAvatarMaleClicked(false);
        setAvatarFemaleClicked(false);
        setAvatarDefaultClicked(false);
    }

    function selectAvatarMale() {
        setAvatarUploadedClicked(false);
        setAvatarMaleClicked(true);
        setAvatarFemaleClicked(false);
        setAvatarDefaultClicked(false);
    }

    function selectAvatarFemale() {
        setAvatarUploadedClicked(false);
        setAvatarMaleClicked(false);
        setAvatarFemaleClicked(true);
        setAvatarDefaultClicked(false);
    }

    function selectAvatarDefault() {
        setAvatarUploadedClicked(false);
        setAvatarMaleClicked(false);
        setAvatarFemaleClicked(false);
        setAvatarDefaultClicked(true);
    }

    return (
        <div className="changeAvatar">
            <h2>Загрузка фотографии</h2>
            <p>Вы можете загрузить свою фотографию в формате JPG или PNG</p>
            <form encType="multipart/form-data">
                <label htmlFor="avatarUploaded">
                    <div className="btn changeAvatar__chooseFile">Выбрать файл</div>
                </label>
                <input type="file"
                       id="avatarUploaded"
                       accept="image/*"
                       onChange={onChangeСhosenFile}/>
            </form>

            {avatarUploaded &&
            <div className="changeAvatar__uploadedPic-wrapper avatar-wrapper"
                 onClick={selectAvatarUploaded}>
                <img className="changeAvatar__uploadedPic"
                     src={`тут будет путь к файлу`}
                     alt="ваше фото"/>
                <div className="chosenEllipse"
                     style={{display: avatarUploadedClicked ? "block" : "none"}}></div>
            </div> }

            <p className="changeAvatar__defaultPics-text">или<br/>выбрать из вариантов</p>
            <div className="changeAvatar__defaultPics">

                <div className="avatar-wrapper"
                     onClick={selectAvatarMale}>
                    <img src={avatarMale}/>
                    <div className="chosenEllipse"
                         style={{display: avatarMaleClicked ? "block" : "none"}}></div>
                </div>

                <div className="avatar-wrapper"
                     onClick={selectAvatarFemale}>
                    <img src={avatarFemale}/>
                    <div className="chosenEllipse"
                         style={{display: avatarFemaleClicked ? "block" : "none"}}></div>
                </div>

                <div className="avatar-wrapper"
                     onClick={selectAvatarDefault}>
                    <img src={avatarDefault}/>
                    <div className="chosenEllipse"
                         style={{display: avatarDefaultClicked ? "block" : "none"}}></div>
                </div>
            </div>
            <button className="btn"
                    type="submit"
                    disabled={!(avatarUploadedClicked || avatarMaleClicked || avatarFemaleClicked || avatarDefaultClicked)}>Сохранить изменения</button>
        </div>
    )
};