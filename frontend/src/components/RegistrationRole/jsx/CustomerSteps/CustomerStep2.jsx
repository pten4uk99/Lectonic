import React, {useState} from 'react'
import {connect} from "react-redux";

import backArrow from "~/assets/img/back-arrow.svg"
import {SwapAddRoleStep} from "../../redux/actions/main";
import {UpdateCompanyDescription, UpdateCompanyName, UpdateCompanySite, UpdateCustomerType} from "../../redux/actions/customer";


function CustomerStep2(props) {
  let role = props.store.addRole.customer
  let companyName = role.company_name
  let companyDescription = role.company_description
  let companySite = role.company_site
  let [customerType, setCustomerType] = useState({
    selectedValue: null,
    selectedIndex: null,
    type: ["Юрлицо","ИП","Самозанятый"]
  });

  let headlines = {
    name: null,
    placeholderName: null,
    placeholderDescription: null,
  };

  function selectCustomerType(e, index){
    e.preventDefault();
    props.UpdateCustomerType(e.target.innerText);
    setCustomerType({
      selectedValue: e.target.innerText,
      selectedIndex: index,
      type: customerType.type
    });
  }

  switch (customerType.selectedIndex){
    case 1:
      headlines.name = 'Наименование ИП';
      headlines.placeholderName = 'Введите полное наименование ИП';
      headlines.placeholderDescription = 'Расскажите о своей деятельности';
      break;
    case 2:
      headlines.placeholderDescription = 'Расскажите о своей деятельности';
      break; 
    default:
      headlines.name = 'Название компании';
      headlines.placeholderName = 'Введите полное название';
      headlines.placeholderDescription = 'Расскажите, чем занимается компания';
      break;
  }

  console.log(props.store);
  return (
    <>
      <div className="step-block-wrapper">
        <div className='step-block margin-bottom-36 step-block__head-text step-block__align-items'>
          <h2 className='step-block__left-part'>
            О заказчике
          </h2>
          <p className="lecturer-right__header">
          Выберете форму ответственности и внесите информацию <br/> о компании, если Вы являетесь юрлицом или ИП.
          </p>
        </div>

        <div className='step-block margin-bottom-24'>
                <div className='step-block__left-part'></div>
                {customerType.type.map((typeName, index) => {
                  return (<button key={index} className={`${customerType.selectedIndex === index ? "btn-role-selected" : "btn-role"} margin-right-12`} 
                  onClick={(e) => selectCustomerType(e, index)}>{typeName}</button>)
                })}
        </div>
        {/* </div>step-block__left-part pt-0` */}
        <div className="step-block margin-bottom-24"
        style={{display: customerType.selectedIndex === 2 ? 'none' : 'flex'}}>
          <p className="step-block__left-part pt-0"
             style={{color: !customerType.selectedValue ? "var(--add-darkGrey" : ""}}>
             {headlines.name}
             <span className="required-sign step-block__required-sign">*</span>
          </p>
          <input className="step-block__input-area"
                 placeholder={headlines.placeholderName}
                 defaultValue={companyName}
                 readOnly={!customerType.selectedValue}
                 type="text" 
                 onBlur={(e) => props.UpdateCompanyName(e.target.value)}/>
        </div>
        
        <div className="step-block-with-textarea margin-bottom-24">
          <p className="step-block__left-part left-part-with-textarea"
             style={{color: !customerType.selectedValue ? "var(--add-darkGrey" : ""}}>
             Описание:
          </p>
          <textarea className="form__textarea textarea-height88"
                    placeholder={headlines.placeholderDescription}
                    defaultValue={companyDescription}
                    readOnly={!customerType.selectedValue}
                    onBlur={(e) => props.UpdateCompanyDescription(e.target.value)}>
          </textarea>
        </div>

        <div className="step-block-with-textarea margin-bottom-24">
          <p className="step-block__left-part left-part-with-textarea"
             style={{color: !customerType.selectedValue ? "var(--add-darkGrey" : ""}}>
             Сайт:
          </p>
          <input className="step-block__input-area"
                 placeholder="http://"
                 type="text" 
                 defaultValue={companySite}
                 readOnly={!customerType.selectedValue}
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
    UpdateCustomerType: (type) => dispatch(UpdateCustomerType(type)),
    UpdateCompanySite: (site) => dispatch(UpdateCompanySite(site)),
  })
)(CustomerStep2);