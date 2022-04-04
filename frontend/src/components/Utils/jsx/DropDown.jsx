import React, {useState, useEffect, useRef} from 'react'
import {connect} from "react-redux";
import downArrow from '~/assets/img/down-arrow.svg'
import {SetIdDropDown} from '../redux/actions/dropdown'
import {UpdateDomain} from "../../WorkRooms/CreateEvent/redux/actions/event";

function DropDown(props) {

  // props 
  // request либо функция запрос на сервер, если нет то массив с данными
  // width (true) задает фиксированную ширину (false) dropdown подстраивается под размер переданных данных
  // input (true) можно писать в инпут (false) нельзя писать в инпут
  // placeholder 

  let [chosenValue, setChosenValue] = useState('');
  const [isSelectOpen, setSelectOpen] = useState(false);
  let [width, setWidth] = useState(0);
  let [data, setData] = useState([]);
  let dropdown = 'dropdownbox';
  let dropDownBox = useRef(0)
  
  if (typeof(props.request) === 'function')
  {
    useEffect(() =>{
      getRequest();
    }, []); 
  } else {
    useEffect(() => {
      setData(props.request)
    }, [props.request]);
  }
  
  useEffect(() => {
    setWidth(dropDownBox.current.offsetWidth)
  });
  
  useEffect(() => {
    setChosenValue(props.defaultValue)
  }, [])

  function getRequest(name) {
    props.request(name)
    .then((response) =>  {
      return response.json()
    })
    .then((data) => {
      setData(data.data)
    })
  }

  function changeValue(value, index) {
    setChosenValue(value);
    setSelectOpen(false);
    if (typeof(props.request) === 'function') {
      props.SetIdDropDown(data[0].id);
      if (props.onSelect) return props.onSelect(data[0].id)
    }
    if (props.onSelect) {
      if (props.monthArr) return props.onSelect(index + 1)
      if (props.domainArr) return props.onSelect(value, setChosenValue)
      props.onSelect(value)
    }
  }

  function openSelectBottom() {
    setSelectOpen(!isSelectOpen);
  }

  function handleSelectInputChange(e) {
    setChosenValue(e.target.value);
    getRequest(e.target.value);
    if (chosenValue){
      setSelectOpen(true);
    }
  }

  return (
    <>
      <div className='dropdown'>
        <div className="dropdown-top"
        style={{width: props.width ? '' : width + 30, zIndex: props.input ? '100' : ''}}>
              <input readOnly={!props.input} 
                     autoComplete='nope' 
                     name={props?.inputName}
                     className='dropdown__input' 
                     placeholder={props.placeholder} 
                     onClick={() => !props.input && openSelectBottom()} 
                     onChange={(e) => handleSelectInputChange(e)}
                     value={chosenValue}/>
              <img className='dropdown__arrow' 
                   src={downArrow} 
                   style={{transform: isSelectOpen ? 'rotate(180deg)' : '', display: props.input ? 'none' : 'block'}} 
                   onClick={openSelectBottom}/>
          </div>
          <div className={isSelectOpen ? dropdown + " show" : dropdown}
               style={{width: props.width ? '100%' : '', zIndex: props.input ? '99' : ''}}>
            <div ref={dropDownBox} 
                 className='dropdown-box'>
                 {data?.map((elem,index) => {
                      return (
                        <div className="dropdown-item" 
                             key={index}
                             onClick={() => changeValue(elem.name === undefined ? elem : elem.name, index)}>
                          {elem.name === undefined ? elem : elem.name}
                        </div>)
                    })
                  }
            </div>
          </div>
      </div>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SetIdDropDown: (id) => dispatch(SetIdDropDown(id)),
    UpdateDomain: (domain) => dispatch(UpdateDomain(domain)),
  })
)(DropDown);
