import React, {useEffect} from "react";
import {baseURL} from "~/ProjectConstants";
import {connect} from "react-redux";
import {SwapLogin} from "../redux/actions/permissions";
import {useNavigate} from "react-router-dom";


function Permissions(props) {
  let hasPermission = props.store.permissions[props.check]
  let navigate = useNavigate()
  
  useEffect(() => {
    const options = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    }
    fetch(`${baseURL}/api/auth/check_authentication/`, options)
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') props.SwapLogin(true)
        else if (data.status === 'error') {
          props.SwapLogin(false)
          navigate('/')
        }
      })
      .catch(error => console.log(error))
  }, [hasPermission])
  
  return (
    <>
      {hasPermission ? props.children : <></>}
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SwapLogin: (logged) => dispatch(SwapLogin(logged))
  })
)(Permissions)