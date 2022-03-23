import React from 'react'
import {connect} from "react-redux";
import {SwapAddRoleStep, SwapChooseRoleVisible, SwapIsCustomer} from "../../redux/actions/main";
import {SwapIsCompany} from "../../redux/actions/customer";
import CustomerStep1 from "./CustomerStep1";
import CustomerStep2 from "./CustomerStep2";


function CustomerSteps(props) {
  let currentStep = props.store.addRole.main.step
  let role = props.store.addRole.customer
  
  function customerChangeHandler() {
    props.SwapAddRoleStep(2)
    props.SwapIsCompany(false)
  }
  
  function companyChangeHandler() {
    props.SwapAddRoleStep(1)
    props.SwapIsCompany(true)
  }
  
  return (
    <div className='customer-steps__wrapper'>
      <div className="customer-steps__radio">
        <div className="customer-steps__choose-subrole">
          <div className="customer" onClick={customerChangeHandler}>
            <div className="customer-steps__radio-button">
              {!role.isCompany && role.isCompany !== undefined && <div className="active"/>}
            </div>
            <span>Физлицо</span>
          </div>
          <div className="company" onClick={companyChangeHandler}>
            <div className="customer-steps__radio-button active">
              {role.isCompany && <div className="active"/>}
            </div>
            <span>Юрлицо</span>
          </div>
        </div>
      </div>

      
      <div className="customer-steps__steps-block">
        <form>
          {role.isCompany ?
            <>
              Компания
            </> :
            role.isCompany !== undefined &&
              currentStep === 2 ? <CustomerStep1/> :
              currentStep === 3 && <CustomerStep2/>
          }
        </form>
      </div>
    </div>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SwapAddRoleStep: (step) => dispatch(SwapAddRoleStep(step)),
    SwapChooseRoleVisible: (visible) => dispatch(SwapChooseRoleVisible(visible)),
    SwapIsCompany: (is_company) => dispatch(SwapIsCompany(is_company)),
  })
)(CustomerSteps);