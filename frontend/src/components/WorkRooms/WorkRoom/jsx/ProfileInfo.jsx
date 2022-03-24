import React, {useEffect, useState} from "react";
import download from '~/assets/img/workrooms/profileInfo/btn-icon-edit.svg';
import iconPlus from '~/assets/img/workrooms/profileInfo/btn_icon-plus.svg';
import {SwapToCustomer, SwapToLecturer, UpdateProfile} from "../redux/actions/profile";
import {connect} from "react-redux";
import {getProfileInfo} from "../ajax/workRooms";


function ProfileInfo(props){
  const profile = props.store.profile
  const utils = props.store.profile.utils
  let btnClassName = "profile-about__btn-role"

  useEffect(() => {
    getProfileInfo()
      .then(response => response.json())
      .then(data => props.UpdateProfile(data.data[0]))
      .catch(error => console.log(error))
  }, [])
  
  return (
    <div className="profile-about">
      <div className="profile-about__photo-box">
        <div className="profile-about__photo">
          <img src={profile.photo} alt="Фотография"/>
        </div>
        <button className="profile-about__btn-download">
          <img src={download} alt="download"/>
        </button>
      </div>
      <div className="profile-about__full-name">
        <span>{profile.last_name}</span>
        <span>{profile.first_name}</span>
        <span>{profile.middle_name}</span>
      </div>
      <div className="profile-about__btn-box">
        <button className="profile-about__btn-add-role">
          <img src={iconPlus} alt="icon-plus"/>
        </button>
        <button className={utils.lecturer ? btnClassName + " active" : btnClassName} 
                onClick={props.SwapToLecturer}>Лектор</button>
        <button className={utils.customer ? btnClassName + " active" : btnClassName} 
                onClick={props.SwapToCustomer}>Заказчик</button>
      </div> 
    </div>
    )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SwapToLecturer: () => dispatch(SwapToLecturer()),
    SwapToCustomer: () => dispatch(SwapToCustomer()),
    UpdateProfile: (data) => dispatch(UpdateProfile(data))
  })
)(ProfileInfo);