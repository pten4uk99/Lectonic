import React, {useState} from "react";
import {connect} from "react-redux";
import empty_card from "../img/empty_card.svg"
import card1 from "../img/potential1.svg"
import card2 from "../img/potential2.svg"
import card3 from "../img/potential3.svg"
import card4 from "../img/potential4.svg"
import card5 from "../img/potential5.svg"

import lecturer1 from "../img/lecturer1.svg"
import lecturer2 from "../img/lecturer2.svg"
import lecturer3 from "../img/lecturer3.svg"
import lecturer4 from "../img/lecturer4.svg"
import lecturer5 from "../img/lecturer5.svg"
import lecturer6 from "../img/lecturer6.svg"
import lecturer7 from "../img/lecturer7.svg"

import LectureCard from "./LectureCard";
import PotentialCard from "./PotentialCard";
import Calendar from "../../Calendar/components/Calendar";
import DateDetail from "../../DateDetail/components/DateDetail";
import photo1 from "../img/photo1.svg";


function Lecturer(props) {

    return !props.lecturer ? (
        <main className="lecturer__main">
            <div className="lecturer__wrapper">
                <section className="created-lectures">
                    <div className="header">Мои лекции<span>?</span></div>
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
                        <PotentialCard photo={card4}
                                       header="Научные субботы"
                                       body="Лекции от известных учёных о самых актуальных исследованиях"/>
                        <PotentialCard photo={card1}
                                       header="Лидеры-доноры"
                                       body="Лекции от создателей проекта о донорстве"/>
                        <PotentialCard photo={card2}
                                       header="Научные субботы"
                                       body="Лекции от известных учёных о самых актуальных исследованиях"/>
                        <PotentialCard photo={card1}
                                       header="Лидеры-доноры"
                                       body="Лекции от создателей проекта о донорстве"/>
                        <PotentialCard photo={card3}
                                       header="Лидеры-доноры"
                                       body="Лекции от создателей проекта о донорстве"/>
                        <PotentialCard photo={card5}
                                       header="Лидеры-доноры"
                                       body="Лекции от создателей проекта о донорстве"/>
                    </div>
                </section>
                <section className="confirmed-lectures">
                    <div className="header">Лекторы<span>?</span></div>
                    <div className="lecture__cards">
                        <div className="lecturer__card">
                            <div className="photo"><img src={lecturer1} alt=""/></div>
                            <div className="card-header">Петров Иван Иванович</div>
                            <div className="card-body">Лекции: Лидеры-доноры</div>
                        </div>
                        <div className="lecturer__card">
                            <div className="photo"><img src={lecturer2} alt=""/></div>
                            <div className="card-header">Тихомиров Сергей Игоревич</div>
                            <div className="card-body">Лекции: Научные субботы</div>
                        </div>
                        <div className="lecturer__card">
                            <div className="photo"><img src={lecturer3} alt=""/></div>
                            <div className="card-header">Калугина Людмила Прокофьевна</div>
                            <div className="card-body">Лекции: Лидеры-доноры, ...</div>
                        </div>
                        <div className="lecturer__card">
                            <div className="photo"><img src={lecturer4} alt=""/></div>
                            <div className="card-header">Петрова Анна Александровна</div>
                            <div className="card-body">Лекции: Лидеры-доноры</div>
                        </div>
                        <div className="lecturer__card">
                            <div className="photo"><img src={lecturer5} alt=""/></div>
                            <div className="card-header">Новосельцев Анатолий Ефремович</div>
                            <div className="card-body">Лекции: Научные субботы</div>
                        </div>
                        <div className="lecturer__card">
                            <div className="photo"><img src={lecturer6} alt=""/></div>
                            <div className="card-header">Иванов Семён Петрович</div>
                            <div className="card-body">Лекции: Лидеры-доноры</div>
                        </div>
                        <div className="lecturer__card">
                            <div className="photo"><img src={lecturer7} alt=""/></div>
                            <div className="card-header">Белугина Ольга Владимировна</div>
                            <div className="card-body">Лекции: Лидеры-доноры</div>
                        </div>

                    </div>
                </section>
                <section className="lecturer-calendar">
                    <div className="header">Календарь заказчика</div>
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
        </main>
    ) : <></>
}

export default connect(
    state => ({store: state}),
    dispatch => ({})
)(Lecturer);