import React, { useState, useEffect } from "react";
import "../styles/DropdownElement.css";
import downArrow from "../img/down-arrow.svg";

export default function DropDownElement(props) {
  let { selectDetails } = props;
  let [options, setOptions] = useState("");
  let [selectIsOpen, setSelectIsOpen] = useState(false);
  let [choosenValue, setChoosenValue] = useState(selectDetails.default);
  let [filterValue, setFilterValue] = useState("");

  function toggleSelectIsOpen() {
    let value = selectIsOpen;
    setSelectIsOpen(!value);
  }

  useEffect(() => {
    document.querySelector("#root").addEventListener("click", (e) => {
      console.log(selectIsOpen);
      if (selectIsOpen) {
        if (
          e.target.classList.contains("select-top") ||
          e.target.classList.contains("select-default") ||
          e.target.classList.contains("select-choosen") ||
          e.target.classList.contains("public-close") ||
          e.target.classList.contains("public-open")
        ) {
          console.log("click is inside");
        } else {
          setSelectIsOpen(false);
        }
      }
    });
  });

  function handleChooseItem(value) {
    setChoosenValue(value);
    setSelectIsOpen(false);
    setFilterValue("");
  }

  function handleInputChange(e) {
    setChoosenValue(e.target.value);
    setFilterValue(e.target.value);
    if (filterValue) {
      console.log(filterValue, options);
      let res = selectDetails.options.filter((item) =>
        item.toLowerCase().includes(e.target.value.toLowerCase())
      );
      console.log(res);
      setOptions(res);
    }
  }

  function handleInputClick() {
    setChoosenValue("");
    setFilterValue("");
    setOptions(selectDetails.options);
  }

  return (
    <div className="select-section">
      <div className="select">
        <div className="select-top">
          <input
            className={
              choosenValue === selectDetails.default
                ? "select-default"
                : "select-choosen"
            }
            value={choosenValue}
            onChange={(e) => handleInputChange(e)}
            onFocus={() => setSelectIsOpen(true)}
            onClick={() => handleInputClick()}
          ></input>
          <img
            className={selectIsOpen ? "img-open" : "img-close"}
            src={downArrow}
            alt="select-icon"
            onClick={toggleSelectIsOpen}
          ></img>
        </div>
        {selectIsOpen && (
          <div className="sub-select">
            {choosenValue !== selectDetails.default
              ? options.map((item) => {
                  return (
                    <div
                      key={item}
                      className="select-item"
                      onClick={() => handleChooseItem(item)}
                    >
                      {item}
                    </div>
                  );
                })
              : selectDetails.options.map((item) => {
                  return (
                    <div
                      key={item}
                      className="select-item"
                      onClick={() => handleChooseItem(item)}
                    >
                      {item}
                    </div>
                  );
                })}
          </div>
        )}
      </div>
    </div>
  );
}
