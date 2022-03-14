import React from "react";
import download from '~/assets/img/workrooms/profileInfo/btn_download_photo.svg';
import iconPlus from '~/assets/img/workrooms/profileInfo/btn_icon-plus.svg';
import {SwapToCustomer, SwapToLecturer} from "../redux/actions/profile";
import {connect} from "react-redux";


function ProfileInfo(props){
    const utils = props.store.profile.utils
    let btnClassName = "profile-about__btn-role"
    return (
        <div className="profile-about">
            <div className="profile-about__photo-box">
                <div className="profile-about__photo">
                  {/*<img src="" alt="photo"/>*/}
                </div>
                <button className="profile-about__btn-download">
                    <img src={download} alt="download"/>
                </button>
            </div>
            <div className="profile-about__full-name">
                <span>Иванов</span>
                <span>Иван</span>
                <span>Иванович</span>
            </div> 
            <button className="profile-about__btn-add-role">
                <img src={iconPlus} alt="icon-plus"/>
            </button>
            <button className={utils.lecturer ? btnClassName + " active" : btnClassName} 
                    onClick={props.SwapToLecturer}>Лектор</button>
            <button className={utils.customer ? btnClassName + " active" : btnClassName} 
                    onClick={props.SwapToCustomer}>Заказчик</button>
        </div>
    )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SwapToLecturer: () => dispatch(SwapToLecturer()),
    SwapToCustomer: () => dispatch(SwapToCustomer())
  })
)(ProfileInfo);