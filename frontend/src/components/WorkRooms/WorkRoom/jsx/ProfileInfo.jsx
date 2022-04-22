import React, {useEffect, useState} from "react";
import download from '~/assets/img/workrooms/profileInfo/btn-icon-edit.svg';
import iconPlus from '~/assets/img/workrooms/profileInfo/btn_icon-plus.svg';
import {SwapToCustomer, SwapToLecturer, UpdateProfile} from "../../../Profile/redux/actions/profile";
import {connect} from "react-redux";
import {getProfileInfo} from "../ajax/workRooms";
import {useNavigate} from "react-router-dom";
import {reverse} from "../../../../ProjectConstants";
import PhotoName from "../../../Utils/jsx/PhotoName";
import Loader from "../../../Utils/jsx/Loader";


function ProfileInfo(props){
  let [isLoaded, setIsLoaded] = useState(false)
  let navigate = useNavigate()
  const profile = props.store.profile
  let btnClassName = "profile-about__btn-role"
  
  let permissions = props.store.permissions
  useEffect(() => {
    if (permissions.is_lecturer) props.SwapToLecturer()
    else if (permissions.is_customer) props.SwapToCustomer()
  }, [permissions.is_lecturer, permissions.is_customer])
  
  
  useEffect(() => {
    if (profile.first_name) setIsLoaded(true)
    else setIsLoaded(false)
  }, [profile])
  
  if (!isLoaded) return <Loader size={40} top={100} left="50%" tX="-50%"/>
  return (
    <div className="profile-about">
      <div className="profile-about__photo-box">
        <div className="profile-about__photo">
          {profile.photo ? <img src={profile.photo} alt="Фотография"/> :
          <PhotoName firstName={profile.first_name}
                     lastName={profile.last_name}
                     size={110}/>
          }
        </div>
        <button className="profile-about__btn-download" onClick={() => navigate(reverse('set_profile'))}>
          <img src={download} alt="download"/>
        </button>
      </div>
      <div className="profile-about__full-name">
        <span>{profile.last_name}</span>
        <span>{profile.first_name}</span>
        <span>{profile.middle_name}</span>
      </div>
      <div className="profile-about__btn-box">
        {!(permissions.is_lecturer || permissions.is_customer) && 
          <button className="profile-about__btn-add-role" 
                onClick={() => navigate(reverse('add_role'))}>
          <img src={iconPlus} alt="icon-plus"/>
        </button>}
        {permissions.is_lecturer && 
          <button className={profile.is_lecturer ? btnClassName + " active" : btnClassName} 
                onClick={props.SwapToLecturer}>Лектор</button>}
        {permissions.is_customer && 
          <button className={profile.is_customer ? btnClassName + " active" : btnClassName} 
                onClick={props.SwapToCustomer}>Заказчик</button>}
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