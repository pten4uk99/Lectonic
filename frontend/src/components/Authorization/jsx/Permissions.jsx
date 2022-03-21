import React, {useEffect} from "react";
import {connect} from "react-redux";
import {useLocation, useNavigate} from "react-router-dom";

import {baseURL} from "~/ProjectConstants";
import {SwapCustomer, SwapLecturer, SwapLogin, SwapPerson} from "../redux/actions/permissions";
import {permissions, reverse} from "../../../ProjectConstants";
import {getProfileInfo} from "../../WorkRooms/WorkRoom/ajax/workRooms";


function Permissions(props) {
  let loggedIn = props.store.permissions.logged_in
  let isPerson = props.store.permissions.is_person
  let isLecturer = props.store.permissions.is_lecturer
  let isCustomer = props.store.permissions.is_customer
  
  let navigate = useNavigate()
  let location = useLocation()
  
  function allPermissionsDefined() {
    let perms = props.store.permissions
    for (let perm in perms) {
      if (perms[perm] === undefined) return false
    }
    return true
  }
  
  function notNeedPermissions() {
    console.log(location.pathname)
    switch (location.pathname) {
      case reverse('index'):
        return true
      case "*":
        return true
    }
  }
  
  const options = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include'
  }
  
  useEffect(() => {
    console.log('ОБНОВЛЕНИЕ ПЕРМИШЕНОВ')

      fetch(`${baseURL}/api/auth/check_authentication/`, options)
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') {
            let permissions = data.data[0]
            
            props.SwapLogin(true)
            props.SwapPerson(permissions?.is_person || false)
            props.SwapLecturer(permissions?.is_lecturer || false)
            props.SwapCustomer(permissions?.is_customer || false)
            
          } else if (data.status === 'error') {
            props.SwapLogin(false)
            navigate(reverse('index'))
          }
        })
        .catch(error => console.log(error))

  }, [loggedIn])
  
  return (
    <>
      {(allPermissionsDefined() || notNeedPermissions()) && props.children}
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SwapLogin: (logged) => dispatch(SwapLogin(logged)),
    SwapPerson: (is_person) => dispatch(SwapPerson(is_person)),
    SwapLecturer: (is_lecturer) => dispatch(SwapLecturer(is_lecturer)),
    SwapCustomer: (is_customer) => dispatch(SwapCustomer(is_customer)),
  })
)(Permissions)