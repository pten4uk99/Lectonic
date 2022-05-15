import React from "react";
import plus from "~/assets/img/icon-create-lection.svg"

function WoorkroomCard(props){
    let button = 'workroom-card__hide'; 
    let box = 'workroom-card__box '; 
    let boxDescription = "workroom-card__box-description";
    let boxImg;
    let boxName = "workroom-card__box-name";
    let createLecture = 'workroom-card__hide'; // скрыто по умолчанию
    let client = 'workroom-card__hide';

    console.log(props);
    if (props.data.lectorCard) {
        box += "workroom-card__box-lector";
        boxDescription = 'workroom-card__box-description workroom-card__box-description--padding';
    } else if (props.data.createLecture) {
        box = 'workroom-card__box workroom-card__create-lecture--background';
        boxName = "workroom-card__create-lecture-text";
        createLecture = 'workroom-card__create-lecture-btn';
        boxImg = 'workroom-card__hide';
        boxDescription = 'workroom-card__hide';
    } else if (props.data.lectureConfirm) {
        button = 'workroom-card__box-btn';
        box = 'workroom-card__box workroom-card__box--box-shadow';
        client = 'workroom-card__show';
    } else {
        button = 'workroom-card__box-btn workroom-card__box-btn--margin';
        box = 'workroom-card__box workroom-card__box--box-shadow';
        boxDescription = 'workroom-card__box-description';
        client = 'workroom-card__show';
    }

    return (
        <div className={box}>
            <div className={(props.data.createLecture) ? "workroom-card__hide" : "workroom-card__box-wrapper"}>
                <img className={boxImg} src={props.data.src} alt="photo"/>
            </div>
            <div className={createLecture}>
                <img src={plus} alt="create lection"/>
            </div>
            <h2 className={boxName}>{props.data.name}</h2>
            <p className={boxDescription}>{props.data.description}</p>
            <div className={client}>
                <h3 className="workroom-card__client">{props.client}</h3>
                <p className="workroom-card__client-name">{props.clientName}</p>
            </div>
            <button className={button}>{props.data.textBtn}</button>
        </div>
    )
}

export default WoorkroomCard;