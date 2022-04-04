import React, {useState} from 'react'
import {connect} from "react-redux";

import backArrow from "~/assets/img/back-arrow.svg"
import {SwapAddRoleStep} from "../../redux/actions/main";
import {UpdateCompanyDescription, UpdateCompanyName, UpdateCompanySite} from "../../redux/actions/customer";


function CustomerStep2(props) {
  let role = props.store.addRole.customer
  let companyName = role.company_name
  let companyDescription = role.company_description
  let companySite = role.company_site
  return (
    <>
      <div className="step-block-wrapper">
        <div className='step-block margin-bottom-36 step-block__head-text'>
          <h2 className='step-block__left-part'>
            О компании
          </h2>
          <p className="lecturer-right__header">
            Если Вы являетесь юрлицом, то введите данные компании.
          </p>
        </div>

        <div className="step-block margin-bottom-12">
          <p className="step-block__left-part pt-0">
            Наименование организации:
            <span className="required-sign step-block__required-sign">*</span>
          </p>
          <input className="step-block__input-area"
                 placeholder="Название компании"
                 defaultValue={companyName}
                 type="text" 
                 onBlur={(e) => props.UpdateCompanyName(e.target.value)}/>
        </div>
        
        <div className="step-block-with-textarea margin-bottom-24">
          <p className="step-block__left-part left-part-with-textarea">
            Описание:
          </p>
          <textarea className="form__textarea textarea-height88"
                    placeholder="Введите адрес помещения для лекций"
                    defaultValue={companyDescription}
                    onBlur={(e) => props.UpdateCompanyDescription(e.target.value)}>
          </textarea>
        </div>

        <div className="step-block-with-textarea margin-bottom-24">
          <p className="step-block__left-part left-part-with-textarea">Сайт:</p>
          <input className="step-block__input-area"
                 placeholder="http://"
                 type="text" 
                 defaultValue={companySite}
                 onBlur={(e) => props.UpdateCompanySite(e.target.value)}/>
        </div>
      </div>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SwapAddRoleStep: (step) => dispatch(SwapAddRoleStep(step)),
    UpdateCompanyName: (name) => dispatch(UpdateCompanyName(name)),
    UpdateCompanyDescription: (description) => dispatch(UpdateCompanyDescription(description)),
    UpdateCompanySite: (site) => dispatch(UpdateCompanySite(site)),
  })
)(CustomerStep2);