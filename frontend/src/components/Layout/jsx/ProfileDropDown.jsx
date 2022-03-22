import React from "react";
import {connect} from "react-redux";
import {useNavigate} from "react-router-dom";
import {logout} from "../ajax";
import {ActiveProfileDropdown} from "../redux/actions/header";
import {SwapLogin} from "../../Authorization/redux/actions/permissions";
import {baseURL, reverse} from "../../../ProjectConstants";


function ProfileDropDown(props) {
  let active = props.store.header.profileDropDownActive
  let navigate = useNavigate()
  
  return active ? (
    <div className="header__profile-drop-down">
      <ul className="profile-drop-down__list">
        <li className="profile-drop-down__item" 
            onClick={() => logoutHandler(navigate, props)}>
          Выйти
        </li>        
        <li className="profile-drop-down__item" 
            onClick={() => userDeleteHandler(navigate, props)}>
          <span style={{color: 'red', fontWeight: 700}}>Удалить пользователя</span>
        </li>
      </ul>
    </div>
  ) : <></>
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    ActiveProfileDropdown: (active) => dispatch(ActiveProfileDropdown(active)),
    SwapLogin: (logged) => dispatch(SwapLogin(logged)),
  })
)(ProfileDropDown)


function logoutHandler(navigate, props) {
  logout()
    .then(r => r.json())
    .then(() => {
      props.ActiveProfileDropdown(false)
      props.SwapLogin(false)
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
        navigate(reverse('index'))
      }
    })
    .catch(error => console.log(error))
}