import React from "react";
import "../styles/ChooseRole.css";
import DropDownElement from "./DropdownElement";


export default function ChooseRole_Lecturer_step1(props) {


    let topicSelect = {
        class: "topic-select",
        default: "Выберете тему лекции",
        options: ["Лидеры-доноры", "Клуб Эльбрус", "Экология", "Медицина"],
    };

    return(
        <>
            <div className="chooseRole__lecturer__step1"
                 style={props.style}>
                <div className="chooseRole__content__block-wrapper">
                    <p className="choseRole-leftPart">Тематика лекций:</p>
                    <button className="btn-addedTopic">Лидеры-доноры</button>
                    <button className="btn-addedTopic">Клуб Эльбрус</button>
                    <DropDownElement  selectDetails={topicSelect}
                                      className="topic-select"/>
                </div>

                <div className="chooseRole__content__block-wrapper">
                    <p className="choseRole-leftPart">Ссылки на видео Ваших выступлений:</p>
                    <div>Вставка</div>
                </div>

                <div className="chooseRole__content__block-wrapper">
                    <p className="choseRole-leftPart">Ссылки на Ваши публикации:</p>
                    <div>Вставка</div>
                </div>
            </div>
        </>
    )
}