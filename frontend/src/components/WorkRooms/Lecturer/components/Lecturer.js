import React, {useEffect, useRef, useState} from "react";
import {connect} from "react-redux";
import bg from "../img/bg.svg"
import photo_profile from "../img/profile_photo.png"
import additional from "../img/additional.svg"
import empty_card from "../img/empty_card.svg"
import edit_photo from "../img/edit_photo.svg"
import card1 from "../img/potential1.svg"
import card2 from "../img/potential2.svg"
import card3 from "../img/potential3.svg"
import card4 from "../img/potential4.svg"
import card5 from "../img/potential5.svg"

import mini_photo from '../img/mini_photo.svg'

import LectureCard from "./LectureCard";
import PotentialCard from "./PotentialCard";
import Calendar from "../../Calendar/components/Calendar";
import DateDetail from "../../DateDetail/components/DateDetail";
import Customer from "./Customer";
import Header from "../../../Header";
import {Link} from "react-router-dom";
import logo from "../../../../img/header_logo.svg";
import iconSearch from "../../../../img/icon-search.svg";
import iconChat from "../img/chat.svg"
import instagram from "../../../../img/footer-instagram.svg";
import vk from "../../../../img/footer-vkontakte.svg";
import fb from "../../../../img/footer-facebook.svg";
import history from "../img/history.svg"

import chatLecturer from "../img/chat_lecturer_temporary.svg";
import chatCustomer from "../img/chat_customer_temporary.svg";
import PopUpChat from "./PopUpChat";

function Lecturer(props) {
    /*работа с чатом*/
    //const [isChatOpen, setChatOpen] = useState(false);
    const [open, setOpen] = useState(false); //открыто модальное окно или нет


    let [lecturer, swapLecturer] = useState(true);
    let l_profile = useRef();
    let c_profile = useRef();

    useEffect(() => {
        activateLecturer();
    }, [])

    function activateLecturer() {
        swapLecturer(true);
        l_profile.current.classList.add("active")
        c_profile.current.classList.remove("active")
    }
    function activateCustomer() {
        swapLecturer(false);
        c_profile.current.classList.add("active")
        l_profile.current.classList.remove("active")
    }


    return (
        <>
            <header className="profile__header">
              <Link to="/">
                  <img className="header-logo" src={logo} alt="логотип" />
              </Link>

              <nav className="header__nav">
                  <img className="header__nav-search"
                       src={iconSearch}
                       alt="поиск" />
                  <img className="header__nav-chat"
                       src={iconChat}
                       alt="чат"
                  onClick={() => setOpen(true)}/>

                  <img className="header__nav-profile"
                       src={mini_photo}
                       alt="ваш профиль"
                       onClick={props.onOpenAuth} />
              </nav>
            </header>

            {/*Чат-картинка открывается в модальном окне*/}
            <PopUpChat isOpened={open}
                   onModalClose={() => setOpen(false)}
                   styleBody={{width: "76%"}}>
                <img className="profile__chat-svg" src={ lecturer ? chatLecturer : chatCustomer}/>
            </PopUpChat>

        <div className="full__profile">
            <div className="lecturer__background"><img src={bg} alt="Фон"/></div>
            <div className="lecturer__profile__header">
                <div className="profile-photo">
                    <img src={photo_profile} alt="Фон"/>
                    <div className="edit-photo"><img src={edit_photo} alt=""/></div>
                </div>
                <div className="additional-info">
                    <div className="edit-photo"><img src={additional} alt=""/></div>
                    Дополнительная информация
                </div>
                <div className="profile-name">
                    <span>Марк</span>
                    <span>Туллий</span>
                    <span>Цицерон</span>
                </div>
                {/*Добавляю дивы для отображения ролей профиля */}
                    <div className="profile-roles-btn lecturer-role">Лектор</div>
                    <div className="profile-roles-btn">Заказчик</div>


            </div>
            <div className="lecturer__profile"
                 onClick={() => {swapLecturer(true); activateLecturer()}} ref={l_profile}>Лектор</div>
            <div className="customer__profile"
                 onClick={() => {swapLecturer(false); activateCustomer()}} ref={c_profile}>Заказчик</div>
            {lecturer ?
            <main className="lecturer__main">
                <div className="lecturer__wrapper">
                    <section className="in-projects">
                        <div className="header">Участие в проектах</div>
                        <div className="projects">
                            <div className="project">Лидеры-доноры<span>3</span></div>
                            <div className="project">Научные субботы<span>5</span></div>
                            <div className="project">Клуб Эльбрус<span>2</span></div>
                        </div>
                    </section>
                    <section className="created-lectures">
                        <div className="header">Созданные лекции <span>?</span></div>
                        <div className="lecture__cards">
                            <div className="lecture__card__empty">
                                <img src={empty_card} alt=""/>
                            </div>
                            <LectureCard/>
                        </div>
                    </section>
                    <section className="potential-orders">
                        <div className="header">Потенциальные заказы<span>?</span></div>
                        <div className="lecture__cards">
                            <PotentialCard photo={card1}
                                           header="Лидеры-доноры"
                                           body="Лекции от создателей проекта о донорстве"/>
                            <PotentialCard photo={card2}
                                           header="Научные субботы"
                                           body="Лекции от известных учёных о самых актуальных исследованиях"/>
                            <PotentialCard photo={card3}
                                           header="Лидеры-доноры"
                                           body="Лекции от создателей проекта о донорстве"/>
                            <PotentialCard photo={card4}
                                           header="Научные субботы"
                                           body="Лекции от известных учёных о самых актуальных исследованиях"/>
                            <PotentialCard photo={card5}
                                           header="Лидеры-доноры"
                                           body="Лекции от создателей проекта о донорстве"/>
                            <PotentialCard photo={card1}
                                           header="Лидеры-доноры"
                                           body="Лекции от создателей проекта о донорстве"/>

                        </div>
                    </section>
                    <section className="confirmed-lectures">
                        <div className="header">Подтверждённые лекции<span>?</span></div>
                        <div className="lecture__cards">
                            <LectureCard/>
                        </div>
                    </section>
                    <section className="lecturer-calendar">
                        <div className="header">Календарь лектора</div>
                        <div className="calendar__wrapper">
                            <Calendar/>
                            <DateDetail date={props.store.calendar.checkedDate}/>
                        </div>
                    </section>
                    <section className="bottom">
                        <div className="header">
                            <span className="first"/>
                            Событие не подтверждено
                        </div>
                        <div className="header">
                            <span className="second"/>
                            Событие подтверждено
                        </div>
                    </section>
                </div>
            </main> :
                <Customer lecturer={lecturer}/>}
            <div className="history"><img src={history} alt=""/></div>
                    <footer className="my_footer">
            <div className="footer-wrapper">
                <div className="footer__rulesLinks">
                    <Link to=""><p className="footer__rulesLinks-text conditions">Условия использования</p></Link>
                    <Link to=""><p className="footer__rulesLinks-text">Политика конфиденциальности</p></Link>
                </div>

                <div className="footer__supportInfo">
                    <p className="footer__supportInfo-text">Техническая поддержка:<br/><span>support@lectonic.ru</span></p>
                </div>

                <div className="footer__socials">
                    <p className="footer__socials-text">Мы в соц. сетях:</p>
                    <div className="footer__socials-icons">
                        <a href="https://www.instagram.com/" target="_blank"><img src={instagram} alt="Instagram" /></a>
                        <a href="https://www.vk.com" target="_blank"><img src={vk} alt="VKontakte" /></a>
                        <a href="https://www.facebook.com" target="_blank"><img src={fb} alt="Facebook" /></a>
                    </div>
                </div>
            </div>
            <div className="footer__copyright">2022 © Сервис Lectonic</div>
        </footer>
        </div>
        </>
    )
}

export default connect(
    state => ({store: state}),
    dispatch => ({})
)(Lecturer);