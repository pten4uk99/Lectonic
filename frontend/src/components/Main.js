import React, {useState} from "react";
import Header from "./Header";
import Modal from "./Modal";
import Authorization from "./Authorization";
import profileSelected from "../img/header_profile-selected.svg";
import profile from "../img/header_profile.svg";
import mainIllustration from "../img/main-illustration.svg";
import "../styles/Main.css";


function Main(){

    const [open, setOpen] = useState(false); //открыто модальное окно или нет

    return(
        <>
            <Header
                src={open ? profileSelected : profile}
                onOpenAuth={() => setOpen(true)}/>
            <Modal
                isOpened={open}
                onModalClose={() => setOpen(false)}
                styleBody={{width: "432px"}}>
                <Authorization />
            </Modal>
            <div className="main">
                <p className="main__text-header">Платформа для лекторов<br/>и не только!</p>
                <p className="main__text">Мы работаем, чтобы слушатели и лекторы<br/>могли легко взаимодействовать</p>
                <button className="btn"
                        onClick={() => setOpen(true)}>Присоединиться</button>
                <img className="main__illustration"
                     src={mainIllustration}
                     alt="Иллюстрация"/>
            </div>
        </>
    )
}

export default Main;