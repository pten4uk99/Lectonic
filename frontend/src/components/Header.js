import React from "react";
import { Link } from "react-router-dom";
import logo from "../img/header_logo.svg";
import iconSearch from "../img/icon-search.svg";
import "../styles/Header.css";


function Header(props){

    return(
      <header className="header">
          <Link to="/">
              <img className="header-logo" src={logo} alt="логотип" />
          </Link>

          <nav className="header__nav">
              <img className="header__nav-search"
                   src={iconSearch}
                   alt="поиск" />

              <img className="header__nav-profile"
                   src={props.src}
                   alt="ваш профиль"
                   onClick={props.onOpenAuth} />
          </nav>
      </header>
    )
};

export default Header;