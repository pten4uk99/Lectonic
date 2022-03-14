import React from "react";
import ProfileInfo from "./WorkRoom/jsx/ProfileInfo";
import background from '~/assets/img/workrooms/user-account_bg.svg';
import {connect} from "react-redux";
import FullCalendar from "~@/WorkRooms/FullCalendar/FullCalendar";

function Workroom(){

    return (
        <div className="user-account">
          <div className="user-account__profile" style={{backgroundImage: `url(${background})`}}>
            <ProfileInfo/>
          </div>
          <div className="user-account__wrapper">
            <div className="user-account__content">
              <FullCalendar/>
            </div>
          </div>
        </div>
    )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(Workroom);