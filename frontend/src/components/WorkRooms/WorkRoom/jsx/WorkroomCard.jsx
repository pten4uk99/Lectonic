import React from "react";

import plus from "~/assets/img/icon-create-lection.svg"
import deleteIcon from "~/assets/img/workrooms/delete-icon.svg"
import PhotoName from "../../../Utils/jsx/PhotoName";


function WoorkroomCard(props){
    let potentialLecture = "workroom-card__img-potential-lecture";
    let lectureImg = "workroom-card__img-lecture"; 

    if (props.data.createLecture) {
        return (
            <div className="workroom-card__box">
                <div className="workroom-card__create-lecture">
                    <div>
                        <img src={plus} alt="обложка"/>
                    </div>
                    <h2>{props.data.name}</h2>
                </div>
            </div>
        )}
    if (props.data.lectorCard){
        return(
            <div className="workroom-card__box" 
                 onClick={props.onClick} style={{cursor: 'pointer'}}>
                <div className= "workroom-card__img-lector">
                  {props.data.src ? 
                    <img src={props.data.src} alt="photo"/> :
                    <PhotoName firstName={props.data.firstName} 
                               lastName={props.data.lastName} 
                               size={110}/>}
                </div>
                <h2 className="workroom-card__box-name">{props.data.name}</h2>
                <p className="workroom-card__box-lecture-name">{props.data.description}</p>
        </div>
        )}
    if (props.data){
        return(
          <div className="workroom-card__box-del-wrapper">
            {props.canDelete && 
              <img className="delete__icon" src={deleteIcon} alt="удалить" onClick={props.onDelete}/>}
            <div className="workroom-card__box box-shadow">
                <div className="workroom-card__box-wrapper">
                    <div className={(props.data.potentialLecture) ? potentialLecture : lectureImg}>
                        <img src={props.data.src} alt="photo"/>
                    </div>
                    <h2 className="workroom-card__box-name">{props.data.name}</h2>
                    <p className="workroom-card__box-description">{props.data.description}</p>
                    <div>
                        <span>{props.data.date}</span>
                        <span>{props.data.city}</span>
                    </div>
                    <div className={(props.data.createdLecture) ? "workroom-card__hide" : ""}>
                        <h3 className="workroom-card__client">{props.data.client}</h3>
                        <p className="workroom-card__client-name">{props.data.clientName}</p>
                    </div>
                    <button className="workroom-card__box-btn" 
                            onClick={props.onClick}>{props.data.textBtn}</button>
                </div>
            </div>
          </div>
        )
    }
}

export default WoorkroomCard;