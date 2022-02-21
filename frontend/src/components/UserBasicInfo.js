import React, { useState } from "react";
import DropDownElement from "./DropdownElement";
import Header from "./Header";
import "../styles/UserBasicInfo.css";
import locationIcon from "../assets/img/location-icon.svg";
import birthdateIcon from "../assets/img/birthdate-icon.svg";
import infoIcon from "../assets/img/Info-icon.svg";
import profileSelected from "../assets/img/header_profile-selected.svg";
import DropDownTest from "./DropDownTest";


export default function UserBasicInfo() {
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

  let daySelect = {
    class: "day-select",
    default: "01",
    options: ["01", "02", "03"],
  };

  let monthSelect = {
    class: "month-select",
    default: "Января",
    options: ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа", "Сентября", "Октября", "Ноября", "Декабря"],
  };

  let yearSelect = {
    class: "year-select",
    default: "1990",
    options: ["1990", "1991", "1993"],
  };

  function click() {
    console.log("clicked yes")
  }

  return (
    <>
      <Header src={profileSelected} />

      <div className="userInfo">
        <h2 className="userInfo__text-header">Информация профиля</h2>
        <p className="userInfo__text">Заполните информацию профиля.<br/>Это даст Вам возможность пользоваться сервисом.</p>

        <form className="userInfo__form" onSubmit={(e) => handleAddEvent(e)}>
          <div className="userInfo__form__input-container">
            <input
              className="form__input"
              value={userDetails.userSurname}
              type="text"
              placeholder="Фамилия"
              onChange={(e) => handleInputChange(e, "userSurname")} />
            <span className="required-sign">*</span>
          </div>

          <div className="userInfo__form__input-container">
            <input
              className="form__input"
              value={userDetails.userFirstName}
              type="text"
              placeholder="Имя"
              onChange={(e) => handleInputChange(e, "userFirstName")} />
            <span className="required-sign">*</span>
          </div>

          <div className="userInfo__form__input-container">
            <input
              className="form__input"
              value={userDetails.userMiddleName}
              type="text"
              placeholder="Отчество"
              onChange={(e) => handleInputChange(e, "userMiddleName")} />
          </div>

          <div className="userInfo__form__inputIcon-container">
              <img className="location-icon"
                   src={locationIcon} />
              <DropDownTest selectDetails={citySelect}
                            className="city-select"
                            placeholder="Ваш город"
                            style={{width: "227px"}}/>
              <div className="required-sign required-sign-location">*</div>
          </div>

          <div className="userInfo__form__inputIcon-container">
            <img className="birthdate-icon"
                 src={birthdateIcon} />
            <div className="dropDown-wrapper">
              <DropDownTest className="day-select"
                            selectDetails={daySelect}
                            placeholder="01"
                            style={{width: "53px"}}/>
            </div>

            <div className="dropDown-wrapper">
              <DropDownTest className="month-select"
                            selectDetails={monthSelect}
                            placeholder="Января"
                            style={{width: "104px"}}/>
            </div>

            <DropDownTest className="year-select"
                          selectDetails={yearSelect}
                          placeholder="1990"
                          style={{width: "72px"}}/>
            <div className="required-sign required-sign-birthdate">*</div>

          </div>

          <div className="userInfo__form__inputIcon-container">
            <img className="info-icon"
                 src={infoIcon} />
            <textarea className="form__textarea"
                      value={userDetails.userSelfDescription}
                      placeholder="Напишите о себе"
                      onChange={(e) => handleInputChange(e, "userSelfDescription")}></textarea>
          </div>
          <button className="btn userInfo__btn"
                  onClick={(e) => handleAddEvent(e)}>Продолжить</button>
        </form>
      </div>
    </>
  );
}
