import React, { useState } from 'react'
// import '~/styles/DropDownTest.styl'
import downArrow from '~/assets/img/down-arrow.svg'
//import upArrow from '~/assets/img/up-arrow.svg'

export default function DropDownTest(props) {
  let { selectDetails } = props
  let [options, setOptions] = useState('')
  const [isSelectOpen, setSelectOpen] = useState(false)
  let [chosenValue, setChosenValue] = useState('')

  function openSelectBottom() {
    setSelectOpen(!isSelectOpen)
  }

  function handleSelectInputChange(e) {
    setChosenValue(e.target.value)
    console.log('e.target.value: ', e.target.value)
  }

  function handleSelectChooseOption(value) {
    setChosenValue(value)
    setSelectOpen(false)
  }

  return (
    <div className='select'>
      <div className='select-top'>
        <input
          className='select-top__input'
          placeholder={props.placeholder}
          style={props.style}
          value={chosenValue}
          onChange={handleSelectInputChange}
        />
        <img
          className='select-top__arrow'
          src={downArrow}
          style={{transform: isSelectOpen ? 'rotate(180deg)' : ''}}
          onClick={openSelectBottom}
        />
      </div>

      <div
        className='select-bottom'
        style={{ display: isSelectOpen ? 'block' : 'none'}}
      >
        {selectDetails.options.map(item => {
          return (
            <div
              className='select-bottom__option'
              key={item}
              onClick={() => handleSelectChooseOption(item)}
            >
              {item}
            </div>
          )
        })}
      </div>
    </div>
  )
}
