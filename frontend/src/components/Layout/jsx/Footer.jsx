import React from 'react'
import {Link, useLocation} from 'react-router-dom'
// import '~/styles/Footer.styl'
import telegram from '~/assets/img/footer-telegram.svg'

export default function Footer() {
  let location = useLocation()
  return (
    <footer style={location.pathname === '/' ? {zIndex: 9} : {}}>
      <div className="footer-wrapper">
        <div className="footer__copyright">2022 © Сервис Lectonic</div>
        <div className="footer__rules">
          <Link className="footer__rules-link" to="">
            Условия использования
          </Link>
          <Link className="footer__rules-link" to="">
            Политика конфиденциальности
          </Link>
        </div>

        <div className="footer__supportInfo is-desktop">
          Техническая поддержка:
          <br/>
          <span>support@lectonic.ru</span>
        </div>

        <div className="footer__socials">
          <p className="footer__socials-text">Мы в соц. сетях:</p>
          <div className="footer__socials-icons">
            <a href="https://www.instagram.com/" target="_blank">
              <img className="footer__insta-icon" src={telegram} alt="Telegram"/>
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
