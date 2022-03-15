import React from "react";
import ProfileInfo from "./WorkRoom/jsx/ProfileInfo";
import background from '~/assets/img/workrooms/user-account_bg.svg';
import {connect} from "react-redux";
import Lecturer from "./WorkRoom/jsx/Lecturer/Lecturer";

function Workroom(){
    return (
        <div className="user-account">
          <div className="user-account__profile" 
               style={{backgroundImage: `url(${background})`}}>
            <ProfileInfo/>
          </div>
          <div className="user-account__wrapper">
            <div className="user-account__content">
              <Lecturer/>
            </div>
          </div>
        </div>
    )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(Workroom);