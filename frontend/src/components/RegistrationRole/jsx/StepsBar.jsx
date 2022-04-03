import React, {useState} from 'react'
import {connect} from "react-redux";
import {SwapAddRoleStep} from "../redux/actions/main";
import {useLocation} from "react-router-dom";


function StepsBar(props) {
  let location = useLocation()
  let style = {color: "var(--main-blue)", cursor: 'pointer'}
  
  function getStyleUnderline() {
    if (props.step in [0, 1]) return {marginLeft: 0}
    else if (props.step === 2) return {marginLeft: '33%'}
    else if (props.step === 3) return {marginLeft: '67%'}
  }
  
  function handleSwapStep(step) {
    if (props.store.addRole.main.step > step) {
      props.SwapAddRoleStep(step)
    }
  }
  
  return (
    <div className='role-steps'>
      <div className="role-steps__text">
        <h2 style={props.step in [0, 1] ? style : {cursor: 'pointer'}} 
            onClick={() => handleSwapStep(1)}>Шаг 1</h2>
        <h2 style={props.step === 2 ? style : {cursor: 'pointer'}} 
            onClick={() => handleSwapStep(2)}>Шаг 2</h2>
        <h2 style={props.step === 3 ? style : {cursor: 'pointer'}} 
            onClick={() => handleSwapStep(3)}>Шаг 3</h2>
      </div>
      <div className='role-steps__bar'>
        <div className='role-steps__bar-current' style={getStyleUnderline()}/>
      </div>
    </div>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SwapAddRoleStep: (step) => dispatch(SwapAddRoleStep(step)),
  }))(StepsBar)