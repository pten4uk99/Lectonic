import React, {useState} from "react";
import Header from "./Header";
import "../styles/UserProfile.css";
import avatarDefault from "../img/avatar-default.svg";
import photoIcon from "../img/photo-icon.svg";
import photoIconHover from "../img/photo-icon-hover.svg";
import roleIcon from "../img/role-icon.svg";
import Icons from "./Icons";
import AddRole from "./AddRole";
import additionalIcon from "../img/additional-icon.svg";
import additionalIconHover from "../img/additional-icon-hover.svg";
import Modal from "./Modal";
import ChangeAvatar from "./ChangeAvatar";

function UserProfile(){

    const [openChangeAvatar, setOpenChangeAvatar] = useState(false); //открытие модального окна для загрузки фото

    function openModalChangeAvatar() {
        setOpenChangeAvatar(true)
    }


    return(
       <div>
           <Header />
           <div className="profile">
               <div className="profile__up">
                   <div className="profile__up__avatar-wrapper">
                       <img className="profile__up__avatar"
                            src={avatarDefault}/>
                       <Icons className="profile__up__avatar-photoIcon"
                              srcNormal={photoIcon}
                              srcHovered={photoIconHover}
                              onClick={openModalChangeAvatar}/>
                   </div>
                   <div className="profile__up__name-wrapper">
                       <h1>Имя</h1>
                       <h1>Фамилия</h1>
                       <h1>Отчество</h1>
                   </div>
               </div>
               <div className="profile__middle">
                   <img src={roleIcon}
                        alt="иконка"/>
                   <p className="role-text">Слушатель</p>
                   <AddRole />
               </div>
               <div className="profile__bottom">
                   <Icons srcNormal={additionalIcon}
                          srcHovered={additionalIconHover}/>
                   <p className="additional-text">Дополнительная информация</p>
               </div>
           </div>
           <Modal
               isOpened={openChangeAvatar}
               onModalClose={() => setOpenChangeAvatar(false)}
               styleBody={{width: "654px"}}>
               <ChangeAvatar />
           </Modal>
       </div>
    )
};

export default UserProfile;