import React, { useState } from "react";
import "../styles/DropDownTest.css";
import downArrow from "../assets/img/down-arrow.svg";
import upArrow from "../assets/img/up-arrow.svg";

export default function DropDownTest(props) {
  let { selectDetails } = props;
  let [options, setOptions] = useState("");
  const [isSelectOpen, setSelectOpen] = useState(false);
  let [chosenValue, setChosenValue] = useState("");

  function openSelectBottom() {
    setSelectOpen(!isSelectOpen);
  }

  function handleSelectInputChange(e) {
    setChosenValue(e.target.value);
    console.log("e.target.value: ", e.target.value);
  }

  function handleSelectChooseOption(value) {
    setChosenValue(value);
    setSelectOpen(false);
  }

  return (
    <div className="select">
      <div className="select__top-wrapper">
        <input
          className="select__top__input"
          placeholder={props.placeholder}
          style={props.style}
          value={chosenValue}
          onChange={handleSelectInputChange}
        />
        <img
          className="select__top__arrow"
          src={isSelectOpen ? upArrow : downArrow}
          onClick={openSelectBottom}
        />
      </div>

      <div
        className="select__bottom-wrapper"
        style={{ display: isSelectOpen ? "block" : "none" }}
      >
        {selectDetails.options.map((item) => {
          return (
            <div
              className="select__bottom__option"
              key={item}
              onClick={() => handleSelectChooseOption(item)}
            >
              {item}
            </div>
          );
        })}
      </div>
    </div>
  );
}
