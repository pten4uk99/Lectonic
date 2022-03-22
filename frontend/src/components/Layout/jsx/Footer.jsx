import React from 'react'
import { Link } from 'react-router-dom'
// import '~/styles/Footer.styl'
import telegram from '~/assets/img/footer-telegram.svg'
import vk from '~/assets/img/footer-vkontakte.svg'

export default function Footer() {
  return (
    <footer>
      <div className="footer-wrapper">
        <div className="footer__supportInfo is-mobile">
          Техническая поддержка:
          <br />
          <span>support@lectonic.ru</span>
        </div>
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
          <br />
          <span>support@lectonic.ru</span>
        </div>

        <div className="footer__socials">
          <p className="footer__socials-text">Мы в соц. сетях:</p>
          <div className="footer__socials-icons">
            <a href="https://www.instagram.com/" target="_blank">
              <img className="footer__insta-icon" src={telegram} alt="Instagram" />
            </a>
            <a href="https://www.vk.com" target="_blank">
              <img className="footer__vk-icon" src={vk} alt="VKontakte" />
            </a>

          </div>
        </div>
      </div>
      <div className="footer__copyright">2022 © Сервис Lectonic</div>
    </footer>
  );
}
