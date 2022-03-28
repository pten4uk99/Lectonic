import React, {useEffect} from "react";
import {connect} from "react-redux";
import {useNavigate} from "react-router-dom";

import ProfileInfo from "./WorkRoom/jsx/ProfileInfo";
import background from '~/assets/img/workrooms/user-account_bg.svg';
import Lecturer from "./WorkRoom/jsx/Lecturer/Lecturer";
import FullCalendar from "~@/WorkRooms/FullCalendar/FullCalendar";
import {reverse} from "../../ProjectConstants";
import CreatedLectures from "./WorkRoom/jsx/Lecturer/CreatedLectures";


function Workroom(props){
  let navigate = useNavigate()
  useEffect(() => {
    if (
      !props.store.permissions.is_lecturer && 
      !props.store.permissions.is_customer
    ) navigate(reverse('add_role'))
  }, [props.store.permissions.is_lecturer, props.store.permissions.is_customer])
  
  let isLecturer = props.store.profile.is_lecturer
  let isCustomer = props.store.profile.is_customer
  
    return (
        <div className="user-account">
          <div className="user-account__profile" 
               style={{backgroundImage: `url(${background})`}}>
            <ProfileInfo/>
          </div>
          <div className="user-account__wrapper">
            <div className="user-account__content">
              <CreatedLectures role={isLecturer ? 'lecturer' : isCustomer && 'customer'}/>
              <Lecturer/>
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