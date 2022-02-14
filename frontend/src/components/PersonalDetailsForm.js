import React, { useState } from "react";
import DropDownElement from "./DropdownElement";
import Header from "./Header";
import "../styles/PersonalDetailsForm.css";
import placeIcon from "../img/location-icon.svg";
import infoIcon from "../img/Info-icon.svg";
import profileSelected from "../img/header_profile-selected.svg";


export default function PersonalDetailsForm() {
  let defaultUserDetails = {
    userSurname: "",
    userFirstName: "",
    userMiddleName: "",
    userCity: "",
    dayOfBirth: "",
    monthOfBirth: "",
    yearOfBirth: "",
    userSelfDescription: "",
  };

  let [userDetails, setUserDetails] = useState({ ...defaultUserDetails });

  function handleInputChange(event, input) {
    setUserDetails((prev) => {
      return {
        ...prev,
        [input]: event.target.value,
      };
    });
  }

  function handleAddEvent(e) {
    e.preventDefault();
    if (
      userDetails.userFirstName &&
      userDetails.userMiddleName &&
      userDetails.userSurname
    ) {
      console.log(userDetails);
      setUserDetails({ ...defaultUserDetails });
    }
  }

  let citySelect = {
    class: "city-select",
    default: "Ваш город",
    options: ["Москва", "Санкт-Петербург", "Воронеж"],
  };

  return (
    <>
      <Header src={profileSelected} />

      <div className="user-details-wrapper">
        <h2 className="submain-title">Информация профиля</h2>
        <p className="general-text">Заполните информацию профиля.<br/>Это даст Вам возможность пользоваться сервисом.</p>

        <form className="user-details-form" onSubmit={(e) => handleAddEvent(e)}>
          <div className="input-container">
            <input
              className="form__input"
              value={userDetails.userSurname}
              type="text"
              placeholder="Фамилия"
              onChange={(e) => handleInputChange(e, "userSurname")} />
            <p className="special-sign">*</p>
          </div>

          <div className="input-container">
            <input
              className="form__input"
              value={userDetails.userFirstName}
              type="text"
              placeholder="Имя"
              onChange={(e) => handleInputChange(e, "userFirstName")} />
            <p className="special-sign">*</p>
          </div>

          <div className="input-container">
            <input
              className="form__input"
              value={userDetails.userMiddleName}
              type="text"
              placeholder="Отчество"
              onChange={(e) => handleInputChange(e, "userMiddleName")} />
          </div>

          <div className="input-with-icon">
              <img
                  className="location-icon"
                  src={placeIcon} />
            <DropDownElement
              selectDetails={citySelect}
              className="select-city"
            ></DropDownElement>
            <p className="special-sign">*</p>
          </div>
          {/* <div className="input-container">
            <div className="small-container"></div>
            <DropDownElement selectDetails={citySelect}></DropDownElement>
            <DropDownElement selectDetails={citySelect}></DropDownElement>
            <DropDownElement selectDetails={citySelect}></DropDownElement>
            <p className="special-sign">*</p>
          </div> */}
          <div className="input-with-icon">
            <img
                className="info-icon"
                src={infoIcon} />
            <textarea
              value={userDetails.userSelfDescription}
              placeholder="Напишите о себе"
              onChange={(e) => handleInputChange(e, "userSelfDescription")}
            ></textarea>
          </div>
          <button className="btn"
                  onClick={(e) => handleAddEvent(e)}>Продолжить</button>
        </form>
      </div>
    </>
  );
}
