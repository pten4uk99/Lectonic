import React, {useState} from 'react'
import downArrow from '~/assets/img/down-arrow.svg'
import '../styles/DropDown.styl'

function DropDown(props) {
  let elements = props.data;
  const [isSelectOpen, setSelectOpen] = useState(false);
  let [chosenValue, setChosenValue] = useState('');
  let dropdown = 'dropdownbox';

  const filteredElements = elements.filter(element => {
    return element.toLowerCase().includes(chosenValue.toLowerCase())
  })

  //console.log(chosenValue);

  function changeValue(value){
    setChosenValue(value);
    setSelectOpen(false);
    
  }

  function openSelectBottom() {
    setSelectOpen(!isSelectOpen);
  }

  function handleSelectInputChange(e) {
    setChosenValue(e.target.value);
    if (filteredElements.length == 0){
      setSelectOpen(false);
    } else{
      setSelectOpen(true);
    }
  }

  return (
    <>
      <div className='dropdown'>
        <div className="dropdown-top">
              <input
                className='dropdown__input'
                placeholder="Выберете тематику"
                onChange={(e) => handleSelectInputChange(e)}
                value={chosenValue}
                />
              <img
                className='dropdown__arrow'
                src={downArrow}
                style={{transform: isSelectOpen ? 'rotate(180deg)' : ''}}
                onClick={openSelectBottom}/>
          </div>
          <div className={isSelectOpen ? dropdown + " show" : dropdown}>
            <div className='dropdown-box'>
                {filteredElements.length != 0 ? 
                    filteredElements.map((elem,index) => {
                      return (
                        <div 
                              className="dropdown-item" 
                              key={index}
                              onClick={() => changeValue(elem)}>
                              {elem}
                        </div>)
                    }) :
                    elements.map((elem,index) => {
                      return (
                        <div 
                              className="dropdown-item" 
                              key={index}
                              onClick={() => changeValue(elem)}>
                              {elem}
                        </div>)
                    })
                  }
            </div>
          </div>
      </div>
    </>
  )
}

export default DropDown;