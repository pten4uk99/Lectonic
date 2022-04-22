import React from "react";
import {connect} from "react-redux";
import {useNavigate} from "react-router-dom";

import {logout} from "../ajax";
import {ActiveProfileDropdown} from "../redux/actions/header";
import {SwapCustomer, SwapLecturer, SwapLogin, SwapPerson} from "../../Authorization/redux/actions/permissions";
import {baseURL, reverse} from "../../../ProjectConstants";


function ProfileDropDown(props) {
  let active = props.store.header.profileDropDownActive
  let profile = props.store.profile
  let navigate = useNavigate()
  
  function logoutHandler() {
    logout()
      .then(r => r.json())
      .then(() => {
        props.ActiveProfileDropdown(false)
        props.SwapLogin(false)
        props.SwapPerson(false)
        props.SwapLecturer(false)
        props.SwapCustomer(false)
        navigate(reverse('index'))
      })
  }
  
  
  // Временное удаление пользователя в таком виде для удобства разработки
  function userDeleteHandler(navigate, props) {
    fetch(`${baseURL}/api/auth/delete`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'deleted') {
          props.ActiveProfileDropdown(false)
          props.SwapLogin(false)
          props.SwapPerson(false)
          props.SwapLecturer(false)
          props.SwapCustomer(false)
          navigate(reverse('index'))
        }
      })
      .catch(error => console.log(error))
  }
  
  return active ? (
    <div className="header__profile-drop-down">
      <ul className="profile-drop-down__list">
        <li className="profile-drop-down__person">{profile.first_name} {profile.last_name}</li>
        <div className="underline"/>
        
        <li className="profile-drop-down__item" onClick={() => navigate(reverse('workroom'))}>
          Кабинет
        </li>
        <li className="profile-drop-down__item" onClick={() =>  navigate(reverse('set_profile'))}>
          Редактировать профиль
        </li>
        
        <div className="underline"/>
        <li className="profile-drop-down__item" onClick={logoutHandler}>Выйти</li>    
        
        {/*<li className="profile-drop-down__item" */}
        {/*    onClick={() => userDeleteHandler(navigate, props)}>*/}
        {/*  <span style={{color: 'red', fontWeight: 700}}>Удалить пользователя</span>*/}
        {/*</li>*/}
      </ul>
    </div>
  ) : <></>
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    ActiveProfileDropdown: (active) => dispatch(ActiveProfileDropdown(active)),
    SwapLogin: (logged) => dispatch(SwapLogin(logged)),
    SwapPerson: (is_person) => dispatch(SwapPerson(is_person)),
    SwapLecturer: (is_lecturer) => dispatch(SwapLecturer(is_lecturer)),
    SwapCustomer: (is_customer) => dispatch(SwapCustomer(is_customer)),
  })
)(ProfileDropDown)
