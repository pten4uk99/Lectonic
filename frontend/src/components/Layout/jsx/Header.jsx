import React from 'react'
import { Link } from 'react-router-dom'
import logo from '~/assets/img/header_logo.svg'
import iconSearch from '~/assets/img/icon-search.svg'
import burgerMenu from "~/assets/img/burger-menu.svg";
// import '~/styles/Header.styl'

export default function Header(props) {
  console.log(logo, iconSearch);
  return (
    <header className="header">
      <Link to="/">
        <img className="header-logo" src={logo} alt="логотип" />
      </Link>

      <nav className="header__nav">
        <img className="header__nav-search is-desktop"
             src={iconSearch}
             alt="поиск" />

        <img
          className="header__nav-profile is-desktop"
          src={props.src}
          alt="меню"
          onClick={props.onOpenAuth}
        />

        {/*бургер под мобильные*/}
        <img
          className="header__nav-burger is-mobile"
          src={burgerMenu}
          alt="меню"
        />
      </nav>
    </header>
  );
}
