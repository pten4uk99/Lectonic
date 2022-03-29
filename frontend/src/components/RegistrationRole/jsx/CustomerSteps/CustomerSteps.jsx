import React, {useEffect} from 'react'
import {connect} from "react-redux";
import {SwapAddRoleStep, SwapChooseRoleVisible, SwapIsCustomer} from "../../redux/actions/main";
import {SwapIsCompany} from "../../redux/actions/customer";
import CustomerStep1 from "./CustomerStep1";
import CustomerStep2 from "./CustomerStep2";
import CompanyStep1 from "./CompanyStep1";
import CompanyStep2 from "./CompanyStep2";
import CompanyStep3 from "./CompanyStep3";
import {createCustomer, uploadDiplomaPhotos} from "../../ajax";
import {reverse} from "../../../../ProjectConstants";
import {useNavigate} from "react-router-dom";
import {SwapCustomer} from "../../../Authorization/redux/actions/permissions";
import {SetErrorMessage} from "../../../Layout/redux/actions/header";


function CustomerSteps(props) {
  let navigate = useNavigate()
  
  useEffect(() => {
    if (props.store.permissions.is_customer) navigate(reverse('workroom'))
  }, [props.store.permissions.is_customer])
  
  let currentStep = props.store.addRole.main.step
  let role = props.store.addRole.customer
  
  useEffect(() => {
    props.SwapIsCompany(undefined)
    props.SwapAddRoleStep(1)
  }, [])
  
  useEffect(() => {
    if (currentStep === 1) props.SwapIsCompany(undefined)
  }, [currentStep])
  
  function customerChangeHandler() {
    props.SwapAddRoleStep(2)
    props.SwapIsCompany(false)
  }
  
  function companyChangeHandler() {
    // props.SwapAddRoleStep(1)
    // props.SwapIsCompany(true)
  }
  
  let domainList = props.store.event.domain
  let equipment = role.equipment
  let hallAddress = role.hall_address
  
  function companySubmitHandler(e) {
    e.preventDefault()
  }
  
  function customerSubmitHandler(e) {
    e.preventDefault()
    let formData = new FormData()
    for (let domain of domainList) formData.append('domain', domain)
    formData.set('equipment', equipment)
    formData.set('hall_address', hallAddress)

    createCustomer(formData)
      .then(response => response.json())
      .then(data => {
        if (data.status === 'created') {
          props.SwapCustomer(true)
          navigate(reverse('workroom'))
        }
      })
      .catch(() => props.SetErrorMessage('create_customer'))
  }
  
  return (
    <>      
      <div className="step-block" style={!role.isCompany && role.isCompany !== undefined && currentStep === 3 || 
        role.isCompany && currentStep > 1 ? {display: "none"} : {}}>
        <div className="step-block__left-part"/>
        <p className="step-block__right-comment lecturer">
          <div className="customer-steps__radio">
            <div className="customer-steps__choose-subrole">
              <div className="customer" onClick={customerChangeHandler}>
                <div className="customer-steps__radio-button">
                  {!role.isCompany && role.isCompany !== undefined && <div className="active"/>}
                </div>
                <span>Физлицо</span>
              </div>
              <div className="company" 
                   style={{cursor: 'not-allowed'}}
                   onClick={companyChangeHandler}>
                <div className="customer-steps__radio-button active">
                  {/*{role.isCompany && <div className="active"/>}*/}
                </div>
                <span>Юрлицо</span>
              </div>
            </div>
          </div>
        </p>
      </div>


      
      <div className="customer-steps__steps-block">
        <form onSubmit={(e) => companySubmitHandler(e)}>
          {role.isCompany ?
            currentStep === 1 ? <CompanyStep1/> :
              currentStep === 2 ? <CompanyStep2/> :
                currentStep === 3 && <CompanyStep3/> : <></>}
          </form>
        <form onSubmit={(e) => customerSubmitHandler(e)}>
          {role.isCompany !== undefined &&
              currentStep === 2 ? <CustomerStep1/> :
              currentStep === 3 ? <CustomerStep2/> : 
                <></>}
        </form>
      </div>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SwapAddRoleStep: (step) => dispatch(SwapAddRoleStep(step)),
    SwapCustomer: (is_customer) => dispatch(SwapCustomer(is_customer)),
    SetErrorMessage: (message) => dispatch(SetErrorMessage(message)),
    SwapChooseRoleVisible: (visible) => dispatch(SwapChooseRoleVisible(visible)),
    SwapIsCompany: (is_company) => dispatch(SwapIsCompany(is_company)),
  })
)(CustomerSteps);