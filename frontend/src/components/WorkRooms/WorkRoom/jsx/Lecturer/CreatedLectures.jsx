import React from "react";
import {connect} from "react-redux";
import tooltip from "~/assets/img/workrooms/workroom/tooltip.svg";
import WorkroomCard from "../WorkroomCard";
//import DropDown from "~@/Utils/jsx/DropDown";

function CreatedLectures(props){
  
    return (
        <section className="block__created-lectures">
          <div className="workroom__block-header">
            <span>Созданные лекции</span>
            <img src={tooltip} alt="Подсказка"/>
          </div>
          
          <div className="cards-block">
            <div className="new-lecture">
              <WorkroomCard data={{
                  name: 'Создать лекцию',
                  createLecture: true,
              }}/>
            </div>
          </div>
          
          <div className="workroom__block-underline"/>
        </section>
    )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(CreatedLectures);